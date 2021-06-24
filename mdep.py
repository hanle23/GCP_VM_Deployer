#! /usr/bin/python3

from functions import open_file, create_file, remake_file, run_os_command
import sys

undeployed = open_file('undeployed')
deployedHistory = open_file('deployedHistory')
currentDeployed = open_file('currentDeployed')
noProject = open_file('np')
error = open_file('error')
# if open_file deployedHistory return false, create new file
if not deployedHistory:
    deployedHistory = create_file("deployedHistory")
# If currentDeployed exist, make a new file
if currentDeployed:
    currentDeployed = remake_file("currentDeployed")
# if noProject exist, make a new file
if noProject:
    noProject = remake_file("noProject")
# If error exist, make a new file
if error:
    error = remake_file("error")
# Return project list, cut everything separated by " " and take the first field
projectList = run_os_command("gcloud project list").split(" ")[0]

# loop through undeployed
for student in undeployed:
    # Set default status as 0 for noProject
    status = 0
    for project in projectList:
        status = 1
        print_project = project.split('-')[1]
        if print_project == student:
            project_count = 0
            for project in deployedHistory:
                if print_project == project:
                    project_count += 1
            # If student has project in deployedHistory, add to currentDeployed
            if project_count >= 1:
                currentDeployed.write(student + "\n")
            else:
                sys.argv[1]

        run_os_command(f'python dep1.py MM {project}')  # need to change
        exit_status = sys.exit()
        if exit_status >= 1:
            error.write(f"{student} {exit_status}" + "\n")
        else:
            deployedHistory.write(f"{student}" + "\n")
            print(project)
    if status == 0:
        noProject.write(f"{student} + \n")
