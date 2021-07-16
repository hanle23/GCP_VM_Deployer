import os
# from deploy_instance import get_instance_date, get_response
# from access import authorize
# from datetime import date

# # Uncomment to use Application Default Credentials (ADC)
# compute, service = authorize()


# # service = discovery.build('cloudresourcemanager',
# #                           'v1', credentials=credentials)

# # request = service.projects().list()


# # response = request.execute()

# # for project in response.get('projects', []):
# #     projectId = project['projectId']
# #     print(projectId + "   {}".format(len(projectId)))

# # compute = discovery.build('compute', 'v1')

# # instances = list_instances(compute, 'bda-210009173')
# # for instance in instances:
# #     print(instance)
# project = 'bda-218333997'

# # response = get_response(compute, project)
# # for name, instance_scoped_list in response['items'].items():
# #     info = instance_scoped_list.get("instances")
# #     if info is not None:
# #         print(info[0]['zone'].split("/")[-1])

# today = date.today()
# print(today)

# # item - string - instances - name

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

with open(os.path.join(__location__, 'text.txt'), 'r') as f:
    s = f.read()
    print(s[1])

f.close()
