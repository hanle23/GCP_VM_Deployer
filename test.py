from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from deploy_instance import list_instances


# Uncomment to use Application Default Credentials (ADC)
credentials = GoogleCredentials.get_application_default()
service = discovery.build('compute', 'v1', credentials=credentials)


# service = discovery.build('cloudresourcemanager',
#                           'v1', credentials=credentials)

# request = service.projects().list()


# response = request.execute()

# for project in response.get('projects', []):
#     projectId = project['projectId']
#     print(projectId + "   {}".format(len(projectId)))

# compute = discovery.build('compute', 'v1')

# instances = list_instances(compute, 'bda-210009173')
# for instance in instances:
#     print(instance)
project = 'bda-219073451'
request = service.instances().aggregatedList(project=project)


response = request.execute()
instance_list = []
instance_name = "bda-db-1"
for name in response['items'].items():
    # TODO: Change code below to process each (name, instances_scoped_list) item:
    item = name[1].get("instances")
    if item is not None:
        instance_list.append(item[0]['name'])

if instance_name in instance_list:
    print("True")


# item - string - instances - name
