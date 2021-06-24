#!/usr/bin/env python

# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import argparse
import os
import time

import googleapiclient.discovery
from oauth2client.client import GoogleCredentials
from six.moves import input

# [START list_project]


def list_projects(service):
    result = service.projects().list().execute()
    return result.get('projects', [])
# [END list_project]

# [START list_instances]


def list_instances(compute, project):
    request = compute.instances().aggregatedList(project=project).execute()
    instance_list = []
    if request is not None:
        response = request.execute()
        for name, instance_scoped_list in response['items'].items():
            info = instance_scoped_list.get("instances")
            if info is not None:
                instance_list.append(info[0]['name'])
    return instance_list
# [END list_instances]


# [START create_instance]
def create_instance(compute, project, zone, name):
    # Configure the machine
    machine_type = "zones/%s/machineTypes/n1-standard-1" % zone
    image = "projects/img-store/global/images/deb-sql-mongo-template-1-image-4"

    config = {
        'name': name,
        'machineType': machine_type,

        # Specify the boot disk and the image to use as a source.
        'disks': [
            {
                'boot': True,
                'initializeParams': {
                    'diskType': 'pd-ssd'
                }
            }
        ],

        # Metadata is readable from the instance and allows you to
        # pass configuration from deployment scripts to instances.
        'metadata': {
            'items': [{
                'key': 'image',
                'value': image
            }]
        }
    }

    return compute.instances().insert(
        project=project,
        zone=zone,
        body=config).execute()
# [END create_instance]

# [START wait_for_operation]


def wait_for_operation(compute, project, zone, operation):
    print('Waiting for operation to finish...')
    while True:
        result = compute.zoneOperations().get(
            project=project,
            zone=zone,
            operation=operation).execute()

        if result['status'] == 'DONE':
            print("done.")
            if 'error' in result:
                raise Exception(result['error'])
            return result

        time.sleep(1)
# [END wait_for_operation]


# [START run]
def main(zone, wait=True):
    credentials = GoogleCredentials.get_application_default()
    service = googleapiclient.discovery.build('cloudresourcemanager',
                                              'v1', credentials=credentials)
    compute = googleapiclient.discovery.build('compute', 'v1')
    instance_name = "bda-db-1"

    projects = list_projects(service)

    for project in projects:
        projectId = project['projectId']
        print('Creating instance.')
        instances = list_instances(compute, projectId)

        if instance_name not in instances:
            operation = create_instance(
                compute, projectId, zone, instance_name)
            wait_for_operation(
                compute, projectId, zone, operation['name'])

            print('Project %s successfully deployed.' % (project['projectId']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        '--zone',
        default='us-central1-f',
        help='Compute Engine zone to deploy to.')

    args = parser.parse_args()

    main(args.zone)
    # main()
# [END run]
