#!/usr/bin/env python

import googleapiclient.errors
from access import authorize
import re
from datetime import datetime

USE_DATABASE = True

if USE_DATABASE:
    import database

# region list_project


def list_projects(service):
    result = service.projects().list().execute()
    return result.get('projects', [])
# endregion list_project


# region create_firewall
def create_firewall(compute, project):
    firewall_exist = False
    firewall_rule = "sql-mon"
    request = compute.firewalls().list(project=project)
    try:
        response = request.execute()
    except googleapiclient.errors.HttpError:
        # TODO add status to database
        print("Firewall have error while deploying")
        return None
    else:
        for firewall in response['items']:
            name = firewall.get("name")
            if firewall_rule == name:
                firewall_exist = True

    if not firewall_exist:
        try:
            config = {
                "name": "sql-mon",
                "priority": 10000,
                "network": "global/networks/default",
                "allowed": [{
                    "IPProtocol": "tcp",
                }],
                "sourceRanges": [
                    "130.63.0.0/16"
                ],
            }
            compute.firewalls().insert(
                project=project,
                body=config).execute()
        except googleapiclient.errors.HttpError:
            print("Firewall have error while deploying")
        else:
            print("Firewall successfully deployed")
# endregion create_firewall

# region get_date


def get_date(compute, project):
    instance = "bda-db-1"
    response = get_response(compute, project)
    for name, instance_scoped_list in response['items'].items():
        info = instance_scoped_list.get("instances")
        if info is None:
            continue
        instance_name = info[0].get("name")
        if instance_name == instance:
            time = info[0].get("creationTimestamp")
            match = re.search(r'\d{4}-\d{2}-\d{2}', time)
            date = datetime.strptime(match.group(), '%Y-%m-%d').date()
            return date


# region choose_zone
def choose_zone(compute):
    # TODO: Using bulk instance API
    project_id = "img-store"
    region = "us-east"
    request = compute.zones().list(project=project_id)
    if request is not None:
        response = request.execute()
        for zone in response['items']:
            return zone['name'] if zone['name'].startswith(region) and zone['status'] == 'UP' else None
# endregion choose_zone

# region get_response


def get_response(compute, project):
    request = compute.instances().aggregatedList(project=project)
    try:
        response = request.execute()
    except googleapiclient.errors.HttpError:
        print("Project {} is not enabled API".format(project))
        return None
    else:
        return response
# endregion get_response

# region namevalid


def namevalid(project_id):
    if not project_id.startswith("bda-"):
        return False
    return True
# endregion namevalid

# region get_date


def get_instance_date(compute, project):
    instance = "bda-db-1"
    response = get_response(compute, project)
    if response is None:
        return None
    for name, instance_scoped_list in response['items'].items():
        info = instance_scoped_list.get("instances")
        if info is not None:
            name = info[0]['name']
            if name == instance:
                date = info[0]["creationTimestamp"]
                match = re.search(r'\d{4}-\d{2}-\d{2}', date)
                date = datetime.strftime(
                    match.group(), '%Y-%m-%d').date()
                return date
# endregion get_date

# region get_zone


def get_zone(compute, project):
    instance = "bda-db-1"
    response = get_response(compute, project)
    if response is None:
        return None
    for name, instance_scoped_list in response['items'].items():
        info = instance_scoped_list.get("instances")
        if info is not None:
            name = info[0]['name']
            if name == instance:
                zone = info[0]['zone'].split("/")[-1]
                return zone
        else:
            return None
# endregion get_zone

# region create_instance


def create_instance(compute, project, zone):
    instance_name = "bda-db-1"
    instance_exist = False
    # Check instances in project
    response = get_response(compute, project)
    if response is not None:
        for name, instance_scoped_list in response['items'].items():
            instance = instance_scoped_list.get("instances")
            if instance is None:
                continue
            name = instance[0]['name']
            if instance_name == name:
                instance_exist = True
    else:
        return None

    if not instance_exist:
        # Configure the machine
        machine_type = "zones/{}/machineTypes/n1-standard-1".format(zone)
        image = "projects/img-store/global/images/deb-sql-mongo-template-1-image-4"
        diskType = "projects/{project}/zones/{zone}/diskTypes/pd-ssd".format(
            project=project, zone=zone)

        config = {
            'name': instance_name,
            'machineType': machine_type,

            # Specify the boot disk and the image to use as a source.
            'disks': [
                {
                    'boot': True,
                    'autoDelete': True,
                    'initializeParams': {
                        'diskType': diskType,
                        'sourceImage': image,
                    }
                }
            ],

            'networkInterfaces': [{
                'network': 'global/networks/default'
            }]
        }
        return compute.instances().insert(
            project=project,
            zone=zone,
            body=config).execute()
    else:
        return True
# endregion create_instance

# region wait_for_operation


def wait_for_operation(compute, project, zone, operation):
    while True:
        result = compute.zoneOperations().get(
            project=project,
            zone=zone,
            operation=operation).execute()

        if result['status'] == 'DONE':
            if 'error' in result:
                raise result['error']
            return result
# endregion wait_for_operation


# [START run]


def main(wait=True):
    compute, service = authorize()
    projects = list_projects(service)
    zone = choose_zone(compute)
    assert zone != None, "No zone start with us-east is up"
    for project in projects:
        project_id = project['project_id']
        changelog = ""
        if not namevalid(project_id):
            continue
        firewall = create_firewall(compute, project_id)
        if firewall is None:
            # TODO Deal with error from create firewall
            if USE_DATABASE:
                changelog = "Deploy Firewall...Failed\n\nDeploy Virtual Machine...Failed"
                database.add(
                    project_id, project_id[4:], 0, None, None, changelog)
            continue
        if USE_DATABASE:
            changelog += "Deploy Firewall...Success\n\n"
        operation = create_instance(
            compute, project_id, zone)
        if operation is None:
            # TODO deal with error from deploy_instance
            if USE_DATABASE:
                changelog += "Deploy Virtual Machine...Failed"
                database.add(
                    project_id, project_id[4:], 0, None, None, changelog)
            continue
        wait_for_operation(
            compute, project_id, zone, operation['name'])
        if USE_DATABASE:
            date = get_date(compute, project_id)
            changelog += "Deploy Virtual Machine...Success"
            database.add(project_id, project_id[4:], 1, zone, date, changelog)
        print('Project {} successfully deployed.'.format(project_id))


if __name__ == '__main__':
    main()
# [END run]
