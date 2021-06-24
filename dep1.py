#! /usr/bin/python3

from functions import runcommand, sys_argv
import sys
import subprocess

projectList = runcommand("gcloud project list").split(" ")[0]
valid = False
zone = "us-east1-c"
firstFirewall = "sql-mon"
firewallStatus = "had"
newInstance = "bda-db-1"
replaceInstance = "hadoop-1-base"


if len(sys.argv) != 2:
    sys.exit(2)

if sys_argv(1) == "MM" or sys_argv(1) == "HAD" or sys_argv(1) == "BTH":
    for project in projectList:
        if project == sys_argv(2):
            valid = True

    if valid:
        runcommand("gcloud config set project %s" % sys_argv(2))
        if sys_argv(1) == "MM" or sys_argv(1) == "BTH":
            firewallList = runcommand(
                "gcloud compute firewall-rules list").split(" ")[0]
            hadFirewall = False

            for firewallItem in firewallList:
                if firewallItem == firstFirewall:
                    hadFirewall = True

            if not hadFirewall:
                runcommand(
                    f'gcloud compute firewall-rules create {firstFirewall} '
                    '--allow TCP '
                    '--direction INGRESS '
                    '--network default '
                    '--priority 10000 '
                    '--source-ranges 130.63.0.0/16')
                if sys.exit() != 0:
                    sys.exit(5)
            instanceList = runcommand(
                "gcloud compute instances list").split(" ")[0]
            hadInstance = False

            for instance in instanceList:
                if instance == newInstance:
                    hadInstace = True

            if not hadInstace:
                runcommand(
                    f'gcloud compute instances create {newInstance} '
                    '--machine-type n1-standard-1 '
                    '--image "projects/img-store/global/images/deb-sql-mongo-template-1-image-4" '
                    '--image-project "img-store" '
                    '--zone {zone} '
                    '--boot-disk-type=pd-ssd')

                if sys.exit() != 0:
                    sys.exit(6)

            else:
                sys.exit(10)

        if sys_argv(1) == "HAD" or sys_argv(1) == "BTH":
            firewallList = runcommand(
                "gcloud compute firewall-rules list").split(" ")[0]
            hadFirewall = False
            for firewallItem in firewallList:
                if firewallItem == firewallStatus:
                    hadFirewall = True
            if not hadFirewall:
                runcommand(
                    f'gcloud compute firewall-rules create {firewallStatus} '
                    '--allow TCP '
                    '--direction INGRESS '
                    '--network default '
                    '--priority 10000 '
                    '--source-ranges 130.63.0.0/16')

                if sys.exit() != 0:
                    sys.exit(7)

            instanceList = runcommand(
                "gcloud compute instances list").split(" ")[0]
            hadReplaceInstace = False
            for instance in instanceList:
                if instance == replaceInstance:
                    hadReplaceInstace = True

            if not hadReplaceInstace:
                runcommand(
                    f'gcloud compute instances create {replaceInstance} '
                    '--machine-type n1-standard-1 '
                    '--image "projects/img-store/global/images/deb-sql-mongo-template-1-image-4" '
                    '--image-project "img-store" '
                    '--zone {zone} '
                    '--boot-disk-type=pd-ssd')
                if sys.exit() != 0:
                    sys.exit(8)
            else:
                sys.exit(11)
    else:
        print(" ")
        sys.exit(3)
else:
    print(" ")
    sys.exit(2)

sys.exit(0)


def deployfirewall():
    args = [
        'gcloud compute firewall-rules create sql-mon',
        '--allow TCP',
        '--direction INGRESS',
        '--network default',
        '--priority 10000',
        '--source-ranges 130.63.0.0/16'
    ]

    subprocess.run(args)


def deployinstance():
    args = [
        'gcloud compute instances create bda-db-1',
        '--machine-type n1-standard-1',
        '--image "projects/img-store/global/images/deb-sql-mongo-template-1-image-4"',
        '--image-project "img-store"',
        '--zone us-east1-c',
        '--boot-disk-type=pd-ssd'
    ]

    subprocess.run(args)
