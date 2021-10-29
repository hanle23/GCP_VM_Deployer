from googleapiclient import discovery
from deployable.access import authorize
import googleapiclient.errors
import deployable.student_data as dataSource
import time

__all__ = ["list_projects",
           "create_firewall",
           "choose_zone",
           "get_instances",
           "namevalid", "get_zone",
           "get_instance_names",
           "create_instance",
           "delete_instance",
           "delete_firewall"]

# Parameter for usage of USE_DATABASE and USE_TIMER
USE_DATABASE = False
USE_TIMER = True

# Uncomment after config databases to store deployment status
# if USE_DATABASE:
#     import database


def list_projects(service: discovery.Resource) -> list:
    # Return a list of project associate with Default account as "Editor"
    result = service.projects().list().execute()
    return result.get('projects', [])


def create_firewall(compute: discovery.Resource, project: str, firewall_rule: str = "sql-mon") -> bool:
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
        return False
    else:
        return True


# Choose a stable deployed project to check for available zone
def choose_zone(compute: discovery.Resource, region: str = "us-east", project_id: str = "img-store") -> str:
    request = compute.zones().list(project=project_id)
    if request is not None:
        response = request.execute()
        for zone in response['items']:
            return zone['name'] if zone['name'].startswith(region) and zone['status'] == 'UP' else None


def get_instances(compute: discovery.Resource, project: str) -> list:
    instances = []
    try:
        response = compute.instances().aggregatedList(project=project).execute()
    except googleapiclient.errors.HttpError:
        return instances
    else:
        for _, instance_scoped_list in response['items'].items():
            instance = instance_scoped_list.get("instances")
            if instance is None:
                continue
            instances.append(instance)
        return instances


def namevalid(project_id: str, name: str = "bda-") -> bool:
    if not project_id.startswith(name):
        return False
    return True


def get_zone(compute: discovery.Resource, project: str) -> str:
    instance = "bda-db-1"
    instances = get_instances(compute, project)
    for current_instance in instances:
        name = current_instance[0]['name']
        if name == instance:
            zone = current_instance[0]['zone'].split("/")[-1]
            return zone


def get_instance_names(compute: discovery.Resource, project: str) -> list:
    instance_names = []
    instances = get_instances(compute, project)
    if instances is None:
        return instance_names
    for instance in instances:
        name = instance[0]['name']
        instance_names.append(name)
    return instance_names


def create_instance(compute: discovery.Resource, project: str, zone: str, instance_name: str = "bda-db-1") -> bool:
    machine_type = "zones/{}/machineTypes/n1-standard-1".format(zone)
    image = "projects/img-store/global/images/deb-sql-mongo-template-1-image-4"
    diskType = "projects/{project}/zones/{zone}/diskTypes/pd-ssd".format(
        project=project, zone=zone)

    config = {
        'name': instance_name,
        'machineType': machine_type,
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
        return False  # Currently using False as a place holder, expect retrieving error as String for database update
    else:
        return True


def delete_instance(compute: discovery.Resource, project: str, zone: str, name: str = "bda-db-1") -> None:
    return compute.instances().delete(
        project=project,
        zone=zone,
        instance=name).execute()


def delete_firewall(compute: discovery.Resource, project: str, firewall: str = "sql-mon") -> None:
    return compute.firewalls().delete(
        project=project,
        firewall=firewall).execute()


def main(wait=True):
    print("Application starting")
    start = time.process_time()
    compute, service = authorize()
    projects = list_projects(service)
    student_list = dataSource.get_student_id_txt("student_list.txt")
    if not student_list:
        print("Data has error while opening, application will be close now")
        exit()
    zone = choose_zone(compute)
    assert zone != None, "No zone start with us-east is up"
    for project in projects:
        project_id = project['projectId']
        if not namevalid(project_id):
            continue
        if project_id not in student_list:
            continue
        firewall = create_firewall(compute, project_id)
        if not firewall:
            continue
        operation = create_instance(compute, project_id, zone)
        if not operation:
            continue
        print('Project {} successfully deployed.'.format(project_id))
    print("Successfully complete application")
    time_result = time.process_time() - start
    if USE_TIMER:
        print("The total time taken is: {} ms".format(time_result))


if __name__ == '__main__':
    main()
