from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

credentials = GoogleCredentials.get_application_default()

# region authorize_compute


def authorize():
    compute = discovery.build(
        'compute', 'v1', credentials=credentials)
    service = discovery.build('cloudresourcemanager',
                              'v1', credentials=credentials)
    return compute, service
# endregion authorize_compute
