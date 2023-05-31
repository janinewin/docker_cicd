# Terraform Demo

🎯 The goal of this demo is to provide a **basic** template for you to expand on if you want to use **terraform**

<img src=https://wagon-public-datasets.s3.amazonaws.com/data-engineering/0502-IAC/terraform.png width=400>

## Setup

1. First you need to install terraform following the instructions for your os https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli

2. Make sure you are authenticated to google cloud platform!

## Testing the project

1. Navigate to the production folder inside here are a few important files:

- `variables.tf` Where the required variables are defined for the  project
- `main.tf` Where the infrastructure is defined
- `provider.tf` Define the gcloud (or other cloud provider) to use
- `terraform.tfvars` A file to define values for the variables defined in `variables.tf`

**Make sure to update** `provider.tf` and `terraform.tfvars` before moving onto creation

2. To create the infrastructure run the below commands:

```bash
terraform init
terraform plan
```

Checkout the plan and if the resources look good:

```bash
terraform apply
```

🚀 You've now created some cloud resources just using code

3. At the moment the state of the cloud resources is tracked by the local .tfstate file lets change that:

Rename `backend.tf.example` and **manually fill it** with the name of the bucket you have just created!

❗️ It is not possible to use variables in the backend that is why here we have to manually fill.

💡 At this point you have a working setup and **can add and remove infrastructure as you need it**!

4. **Cleanup** will be just one command:

```bash
terraform destroy
```

The ease of this along with state matching our code means we never leave unwanted and costly cloud resources running!

## Going further

If you want to automate even further checkout this [tutorial](https://cloud.google.com/docs/terraform/resource-management/managing-infrastructure-as-code)
