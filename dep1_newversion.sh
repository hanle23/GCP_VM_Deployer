#!/bin/bash

projectList=$(gcloud projects list | cut -d' ' -f 1) #retlit = project list
status = 0 # f = status
zone = us-east1-c
firstFirewall=sql-mon # fw1 = firstFirewall
hadFirewall = had # fw2 = hadFirewall 
newInstance = bda-db-1 # in1 = newInstance
replaceInstance = hadoop-1-base #in2 = replaceInstance

if [ $# -ne 2 ]; then # -ne = "!=""
	exit 2
fi

if ([ $1 = "MM" ] || [ $1 = "HAD" ] || [ $1 = "BTH" ]); then # $1 = First argument

  for project in $projectList; do
    if [ $project = $2 ]; then # $2 = Second Argument
      status = 1
    fi
  done

  if [ $status -eq 1 ]; then # -eq = "=="
    gcloud config set project "$2"

    if ([ $1 = "MM" ] || [ $1 = "BTH" ]); then
      firewallList = $(gcloud compute firewall-rules list | cut -d' ' -f1) #fwretit = firewallList
      firewallStatus = 0
      for firewallItem in $firewallList; do
        if [ $firewallItem = $firstFirewall ]; then
          firewallStatus = 1
        fi
      done
      if [ $firewallStatus -ne 1 ]; then # -ne = "!=""
        gcloud compute firewall-rules create $firstFirewall \
	    --allow TCP \
	    --direction INGRESS \
	    --network default \
	    --priority 1000 \
	    --source-ranges 130.63.0.0/16

        if [ $? -ne 0 ]; then # -ne = "!=""
	        exit 5
        fi
      fi

      instanceList = $(gcloud compute instances list | cut -d' ' -f1) #inretlit = instanceList
      newInstanceStatus = 0
      for instance in $instanceList; do
        if [ $instance = $newInstance ]; then
          newInstanceStatus = 1
        fi
      done
      if [ $newInstanceStatus -ne 1 ]; then # -ne = "!=""
        gcloud compute instances create $newInstance \
          --machine-type n1-standard-1 \
     	  --image "projects/img-store/global/images/deb-sql-mongo-template-1-image-4" \
     	  --image-project "img-store" \
     	  --zone $zone \
     	  --boot-disk-type=pd-ssd

        if [ $? -ne 0 ]; then # -ne = "!=""
	        exit 6
        fi
      else
        exit 10
      fi

    fi
    if ([ $1 = "HAD" ] || [ $1 = "BTH" ]); then

      firewallList = $(gcloud compute firewall-rules list | cut -d' ' -f1)
      firewallStatus = 0
      for firewallItem in $firewallList; do
        if [ $firewallItem = $hadFirewall ]; then
          firewallStatus = 1
        fi
      done
      if [ $firewallStatus -ne 1 ]; then # -ne = "!=""
        gcloud compute firewall-rules create $hadFirewall  \
	  --allow TCP:80,TCP:22 \
	  --direction INGRESS \
	  --network default \
	  --priority 1000 \
	  --source-ranges 130.63.0.0/16

        if [ $? -ne 0 ]; then # -ne = "!=""
	        exit 7
        fi
      fi

      instanceList = $(gcloud compute instances list | cut -d' ' -f1)
      replaceInstanceStatus = 0
      for instance in $instanceList; do
        if [ $instance = $replaceInstance ]; then
          replaceInstanceStatus = 1
        fi
      done
      if [ $replaceInstanceStatus -ne 1 ]; then # -ne = "!=""
        gcloud compute instances create $replaceInstance \
     	  --machine-type n1-standard-2 \
     	  --image "projects/img-store/global/images/deb-hadoop-1-base" \
     	  --image-project "img-store" \
     	  --zone $zone \
     	  --boot-disk-type=pd-ssd

        if [ $? -ne 0 ]; then # -ne = "!=""
	        exit 8
        fi
      else
        exit 11
      fi
    fi

  else
    echo " "
    exit 3
  fi

else
  echo " "
  exit 2
fi

exit 0

#gcloud compute disk-types list
#gcloud projects list --filter="m"
#gcloud compute firewall-rules list
#gcloud compute instances list
