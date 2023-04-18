<div id="top"></div>

<br />
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

An automation tools to help deploying Cloud instances for administration purposes or development with flexible configurations.

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

- [Python](https://python.org/)
- [Google Cloud Python API](https://github.com/googleapis/google-cloud-python)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

The tools will depending on the usage and services, but currently will focus on for Google Cloud Platform

### Prerequisites

- [Python](https://www.python.org/downloads/)
- [Git](https://git-scm.com/download)
- [Cloud SDK](https://cloud.google.com/sdk/docs/install)
- [google-api-python-client](https://github.com/googleapis/google-api-python-client)

### Installation

1. Clone the repo
   ```sh
   git clone [https://github.com/hanle23/Deployable](https://github.com/hanle23/Virtual-Machine-Deployer)
   ```
2. Install dependencies
   ```sh
   pip install .
   ```
3. Make default google account
   ```sh
   gcloud auth application-default login
   ```

<!-- USAGE EXAMPLES -->

## Usage

Before runing any file in this application, please make sure to set a default google account to be used by the application in step 3 of Installation.

Run file deploy_instance_test.py to test for packages import and main functions of the application. Once all the tests passed, heads to deploy_instance.py to run the main file.

The command line will shows names of the successfully deployed project_id and completion time if USER_TIMER is set to TRUE

The current repo has 2 branches, main branch is deployment and config-setup is for production.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ROADMAP -->

## Roadmap

- [x] Finish packaging config-setup branch
- [x] Re-configure the setup.py file
- [] Create Web API retriever
- [] Create Database
- [] Create Web Interface
- [] Add Auto runner

See the [open issues](https://github.com/York-University-SCS/Deployable/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>
