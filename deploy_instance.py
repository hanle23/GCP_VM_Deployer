from datetime import datetime
import re
from access import authorize
import googleapiclient.errors


USE_DATABASE = False

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
            return None
        else:
            return True
    else:
        return True
# endregion create_firewall

# region get_date


def get_date(compute, project):
    instance = "bda-db-1"
    response = get_response(compute, project)
    instances = get_instances(compute, project)
    for instance in instances:
        instance_name = instance[0].get("name")
        if instance_name == instance:
            time = instance[0].get("creationTimestamp")
            match = re.search(r'\d{4}-\d{2}-\d{2}', time)
            date = datetime.strptime(match.group(), '%Y-%m-%d').date()
            return date


# region choose_zone
def choose_zone(compute, region="us-east"):
    # TODO: Using bulk instance API
    project_id = "img-store"
    request = compute.zones().list(project=project_id)
    if request is not None:
        response = request.execute()
        for zone in response['items']:
            return zone['name'] if zone['name'].startswith(region) and zone['status'] == 'UP' else None
# endregion choose_zone

# region get_instances


def get_instances(compute, project):
    instances = []
    response = get_response(compute, project)
    for _, instance_scoped_list in response['items'].items():
        instance = instance_scoped_list.get("instances")
        if instance is None:
            continue
        instances.append(instance)
    if len(instances) == 0:
        return None
    return instances
# endregion get_instances

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


def namevalid(project_id, name="bda-"):
    if not project_id.startswith(name):
        return False
    return True
# endregion namevalid

# region get_zone


def get_zone(compute, project):
    instance = "bda-db-1"
    response = get_response(compute, project)
    instances = get_instances(compute, project)
    for instance in instances:
        name = instance[0]['name']
        if name == instance:
            zone = instance[0]['zone'].split("/")[-1]
            return zone

# endregion get_zone

# region get_instance_name


def get_instance_names(compute, project):
    instance_names = []
    instances = get_instances(compute, project)
    if instances is None:
        return None
    for instance in instances:
        name = instance[0]['name']
        instance_names.append(name)
    return instance_names
# endregion get_name

# region create_instance


def create_instance(compute, project, zone):
    instance_name = "bda-db-1"
    instance_exist = False
    instance_names = get_instance_names(compute, project)
    if instance_names is not None:
        if instance_name in instance_names:
            instance_exist = True

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
                'network': 'global/networks/default',
                'accessConfigs': [
                    {
                        "type": "ONE_TO_ONE_NAT",
                        "name": "External NAT",
                        "networkTier": "PREMIUM"
                    }
                ]
            }]
        }
        try:
            compute.instances().insert(
                project=project,
                zone=zone,
                body=config).execute()
        except googleapiclient.errors.HttpError:
            return None
        else:
            return True
    else:
        return None
# endregion create_instance

# region delete_instance


def delete_instance(compute, project, zone):
    name = "bda-db-1"  # name can be change if not default
    return compute.instances().delete(
        project=project,
        zone=zone,
        instance=name).execute()
# endregion delete_instance

# region delete_firewall


def delete_firewall(compute, project, firewall="sql-mon"):
    return compute.firewalls().delete(
        project=project,
        firewall=firewall).execute()

# region main


def main(wait=True):
    print("Application starting")
    compute, service = authorize()
    projects = list_projects(service)
    zone = choose_zone(compute)
    assert zone != None, "No zone start with us-east is up"
    for project in projects:
        project_id = project['projectId']
        if not namevalid(project_id):
            continue
        firewall = create_firewall(compute, project_id)
        if firewall is None:
            continue
        operation = create_instance(compute, project_id, zone)
        if operation is None:
            continue
        print('Project {} successfully deployed.'.format(project_id))


if __name__ == '__main__':
    main()
# endregion main
