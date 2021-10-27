# edde-platform-deployment

[![CircleCI](https://circleci.com/gh/greyshore/edde-platform-deployment/tree/main.svg?style=svg&circle-token=85775bb783716e1b8d8d47d865bd315d1079b80e)](https://circleci.com/gh/greyshore/edde-platform-deployment/tree/main)

This repo is used as a "seed" repo for the management of a delivery platform for the EDDE product. The intention is for this repo to be a template/seed that can be used by a scaffolding program to spin up a delivery platform specific to a cohort of students. Each cohort would have a unique copy of this repo and unique resources would be deployed from those repos.

<br>

# prerequisites
- Terraform
- terraform-compliance
- CircleCI

<br>

# customization
The pipeline in this repo can be customized to deploy different EDDE environments by changing the following in .circleci/config.yml

pipeline parameters:
- cohort_repo_base:
  - This is the string of the base cohort name and is used in generated repos to define some variables for scripting.
- static_web_storage_account_name:
  - The unique name of the web storage account for the cohort environment.
- resource_group_name:
  - The name of the Azure Resource Group for the cohort environment.
- backend_resource_group_name:
  - The parent resource group hosting the Terraform state storage account.
- backend_storage_account_name:
  - The storage account name used for hosting the Terraform state.
- backend_container_name:
  - The container name used for hosting the Terraform state.
- circleci_vcs_type:
  - This specifies the version control system type that is connected with CircleCI. This will be where the code is stored for the cohort.
- circleci_organization:
  - This is the organization name within CircleCI for where the cohort code is being stored.
- cohort_context_name:
  - This will be the name of the CircleCI context that will store environment variables used by the cohort's pipelines.

executor environment variables:
- environment:
  - ARM_CLIENT_ID: The client ID of service principal with the permissions to manage resources within the cohort environment.
  - ARM_SUBSCRIPTION_ID: The parent subscription ID that will host the cohort environment resources.
  - ARM_TENANT_ID: The parent Azure AD tenant ID for the overall cohort environment resources.

<br>

# terraform files
The terraform files are currently broken out into separate files defining the following groups of resources:
- backend.tf - defines the location of the terraform remote state 
- main.tf - defines the provider and current context settings
- resource_groups.tf - defines the creation of the parent resource groups
- storage.tf - defines the storage account resources and any output token data
- terraform.tfvars - defines any custom configuration specific to the resources managed in this pipeline
- variables.tf - defines the variable structure and descriptive definitions of their use

<br>

# circleci api key for context creation
There is a GS pipeline service account called "svc-gs-pipeline". Its email address and mailbox are hosted on Ionos and its email address is "svc_gs_pipeline@paulsoftware.com".
This information, along with the circleci api key for the service account are vaulted in the AKV-DE-Keyvault in Azure.
<br>
<br>
This service account is used for the following:
- CircleCI access in order to create and manage contexts.

<br>

# decommissioning
The current decommissioning process is automated in a destruction pipeline that is already configured within CircleCI. The pipeline/workflow sits in a "hold" status until it is approved twice.
Once approved twice, it proceeds in the following order:
- Runs "Terraform Destroy" to remove all deployed Azure infrastructure resources.
- Removes the Terraform state file from the Azure backend storage account.
- Removes the associated CircleCI context and environment variables.
- Archives the generated app and infrastructure Github repositories.