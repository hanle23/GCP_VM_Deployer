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
import googleapiclient.errors
from oauth2client.client import GoogleCredentials
from six.moves import input

# [START list_project]


def list_projects(service):
    result = service.projects().list().execute()
    return result.get('projects', [])
# [END list_project]


# [START create_firewall]


def create_firewall(compute, project):
    request = compute.firewalls().list(project=project)
    firewalls = []
    firewall_rule = "sql-mon"
    if request is not None:
        response = request.execute()
        for firewall in response['items']:
            firewalls.append(firewall.get("name"))
    if firewall_rule not in firewalls:
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
            print("Firewall have error while deployed")
        else:
            print("Firewall successfully deployed")

# [END create_firewall]


# [START choose_zone]


def choose_zone(compute):
    # TODO: Using bulk instance API
    projectID = "img-store"
    region = "us-east"
    request = compute.zones().list(project=projectID)
    if request is not None:
        response = request.execute()
        for zone in response['items']:
            return zone['name'] if zone['name'].startswith(region) and zone['status'] == 'UP' else None


# [END choose_zone]

# [START create_instance]


def create_instance(compute, project, zone):
    name = "bda-db-1"
    # Check instances in project
    request = compute.instances().aggregatedList(project=project)
    instance_list = []
    if request is not None:
        response = request.execute()
        for name, instance_scoped_list in response['items'].items():
            info = instance_scoped_list.get("instances")
            if info is not None:
                instance_list.append(info[0]['name'])
    if name not in instance_list:
        # Configure the machine
        machine_type = "zones/{}/machineTypes/n1-standard-1".format(zone)
        image = "projects/img-store/global/images/deb-sql-mongo-template-1-image-4"
        diskType = "projects/{project}/zones/{zone}/diskTypes/pd-ssd".format(
            project=project, zone=zone)

        config = {
            'name': name,
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
# [END wait_for_operation]

# [START authorize_compute]


def authorize_compute():
    credentials = GoogleCredentials.get_application_default()
    compute = googleapiclient.discovery.build(
        'compute', 'v1', credentials=credentials)
    return compute
# [END authorize_compute]

# [START authorize_service]


def authorize_service():
    credentials = GoogleCredentials.get_application_default()
    service = googleapiclient.discovery.build('cloudresourcemanager',
                                              'v1', credentials=credentials)
    return service
# [END authorize_service]

# [START run]


def main(wait=True):
    compute = authorize_compute()
    service = authorize_service()
    projects = list_projects(service)
    zone = choose_zone(compute)
    assert zone != None, "No zone start with us-east is up"
    for project in projects:
        projectID = project['projectID']
        # TODO: add function for projectID checking
        # print('Creating instance.')
        create_firewall(compute, projectID)
        operation = create_instance(
            compute, projectID, zone)
        wait_for_operation(
            compute, projectID, zone, operation['name'])
        print('Project {} successfully deployed.'.format(projectID))


if __name__ == '__main__':
    main()
# [END run]
