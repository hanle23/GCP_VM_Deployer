from googleapiclient import discovery
from access import authorize
import googleapiclient.errors
import student_data as dataSource
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
    '''
    Return a list of project associate with Default account as "Editor"

    Service : Service object from Google Cloud Web API

    Return the list of project-id that has the default Google account as editor
    '''

    result = service.projects().list().execute()
    return result.get('projects', [])


def create_firewall(compute: discovery.Resource, project: str, firewall_rule: str = "sql-mon") -> bool:
    '''
    Generating Firewall Rules based on the config values

    Compute : Compute object from Google Cloud Web API

    project : name of the project-id that will be inserted the firewall rule

    firewall_rule : name of the rule if not default

    config : Please check the document for the config field at https://cloud.google.com/compute/docs/reference/rest/v1/firewalls/insert

    Return : True if successfully added, False if otherwise
    '''
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
    '''
    Choosing an available zone that is currently UP as a string to deploy project into

    compute : compute object retrieved from Google Web API

    region : general region that the user wish to deploy the instance into

    project_id : a fixed project_id that already set-up from user to access available zone

    Return a String that contains the specific zone that is available and running
    '''
    request = compute.zones().list(project=project_id)
    if request is not None:
        response = request.execute()
        for zone in response['items']:
            return zone['name'] if zone['name'].startswith(region) and zone['status'] == 'UP' else None


def get_instances(compute: discovery.Resource, project_id: str) -> list:
    '''
    Retrieving a list of instances in a specific project for information or checking

    compute : compute object retrieved from Google Web API

    project_id : a fixed project_id that already set-up from user to access available zone

    Return a list of instances
    '''
    instances = []
    try:
        response = compute.instances().aggregatedList(project=project_id).execute()
    except googleapiclient.errors.HttpError:
        return instances
    else:
        for _, instance_scoped_list in response['items'].items():
            instance = instance_scoped_list.get("instances")
            if instance is None:
                continue
            instances.append(instance)
        return instances


def namevalid(project_id: str, criteria: str = "bda-") -> bool:
    '''
    A string checking function for specific criteria

    project_id : the name that will be checking

    name : The beginning of the name that fits criteria

    Return True if name fits the criteria, False if otherwise
    '''
    if not project_id.startswith(criteria):
        return False
    return True


def get_zone(compute: discovery.Resource, project_id: str, instance: str = "bda-db-1") -> str:
    '''
    Retrieving zone of a specific project_id and specific instance

    compute : compute object retrieved from Google Web API

    project_id : project that contains instance

    instance : Name of the instance to search zone detail

    return a String of Zone, empty String if not found
    '''
    zone = ""
    instances = get_instances(compute, project_id)
    for current_instance in instances:
        name = current_instance[0]['name']
        if name == instance:
            zone = current_instance[0]['zone'].split("/")[-1]
            return zone
        return zone


def get_instance_names(compute: discovery.Resource, project_id: str) -> list:
    '''
    An instances' name retriever for a specific project

    compute : compute object retrieved from Google Web API

    project_id : name of the project that will be searching

    Return a list of instances in String
    '''
    instance_names = []
    instances = get_instances(compute, project_id)
    if instances is None:
        return instance_names
    for instance in instances:
        name = instance[0]['name']
        instance_names.append(name)
    return instance_names


def create_instance(compute: discovery.Resource, project_id: str, zone: str, instance_name: str = "bda-db-1") -> bool:
    '''
    An instance generator that deploy instance following the criteria in config

    compute : compute object retrieved from Google Web API

    project_id : name of the project that the instance will be deployed into

    zone : name of a specific zone 

    instance_name : the name of the instance that will be deployed

    config : for details, please visit https://cloud.google.com/compute/docs/reference/rest/v1/instances/insert

    Return True if successfully deployed, False if otherwise
    '''
    machine_type = "zones/{}/machineTypes/n1-standard-1".format(zone)
    image = "projects/img-store/global/images/deb-sql-mongo-template-1-image-4"
    diskType = "projects/{project}/zones/{zone}/diskTypes/pd-ssd".format(
        project=project_id, zone=zone)

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
            project=project_id,
            zone=zone,
            body=config).execute()
    except googleapiclient.errors.HttpError:
        return False  # Currently using False as a place holder, expect retrieving error as String for database update
    else:
        return True


def delete_instance(compute: discovery.Resource, project_id: str, zone: str, name: str = "bda-db-1") -> None:
    '''
    Delete the specific instance in the given project

    compute : compute object retrieved from Google Web API

    project_id : name of the project that contains the instance

    zone : the zone that the project was deployed into

    name : name of the instance that will be deleted

    Return None
    '''
    return compute.instances().delete(
        project=project_id,
        zone=zone,
        instance=name).execute()


def delete_firewall(compute: discovery.Resource, project_id: str, firewall: str = "sql-mon") -> None:
    '''
    Delete the specific firewall rules in the given project

    compute : compute object retrieved from Google Web API

    project_id : name of the project that contains the firewall rules

    firewall : name of the firewall rules that will be deleted

    Return None
    '''
    return compute.firewalls().delete(
        project=project_id,
        firewall=firewall).execute()


def main(wait=True):
    print("Application starting")
    start = time.time()
    compute, service = authorize()
    projects = list_projects(service)
    student_list = dataSource.get_student_id_txt("student_list.txt")
    if len(student_list) == 0:
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
    time_result = time.time() - start
    if USE_TIMER:
        print("The total time taken is: {:.2f} s".format(time_result))


if __name__ == '__main__':
    main()
