# sagemaker-shadow-deploy

## Prereqs

1. Install CDK on your device using these instructions: https://docs.aws.amazon.com/cdk/latest/guide/work-with-cdk-python.html



## Setup Instructions

#### For Option 1 - Deploy models with an offline approach using Amazon SageMaker Model Monitor

1. Clone this project to your Jyputer Lab/SageMaker Studio: git clone https://github.com/aws-samples/amazon-sagemaker-shadow-deploy.git
2. Spin up a SageMaker Notebook with kernel set to `conda_python3`
3. Execute the notebook present here resources/Shadow-deployment-async-process-demo-breast-cancer.ipynb

#### For Option 2  - Deploy models with a synchronous approach 

1. Clone this project to your device: git clone https://github.com/aws-samples/amazon-sagemaker-shadow-deploy.git
2. Navigate to project root directory and create virtualenv: python3 -m venv .venv
3. Activate virtualenv: source .venv/bin/activate
4. Install dependent packages: pip install -r requirements.txt
5. Verify setup: cdk synth  (should generate cloudformation template)
6. Upload resources/breast_cancer_shadow_deployment.ipynb to your sagemaker notebook instance
7. Execute the above notebook to build/train/deploy your model versions
8. Deploy Stack after changing the parameters to your deployed model versions  
    - cdk deploy sagemaker-shadow-deploy --parameters endpointNameV1=shadow-linear-endpoint-v1-202012300108 --parameters endpointNameV2=shadow-linear-endpoint-v2-202012300229

## Testing

1. Stack output display two endpoint urls 
     1. sagemaker-shadow-deploy.Endpointxxx -  use this url in postman and send the following data:
     {"data": "13.49,22.3,86.91,561.0,0.08752,0.07697999999999999,0.047510000000000004,0.033839999999999995,0.1809,0.057179999999999995,0.2338,1.3530000000000002,1.735,20.2,0.004455,0.013819999999999999,0.02095,0.01184,0.01641,0.001956,15.15,31.82,99.0,698.8,0.1162,0.1711,0.2282,0.1282,0.2871,0.06917000000000001"}
     2. sagemaker-shadow-deploy.ViewShadowDeploymentsViewerEndpointxxx - use this url on your browser to see the model inference results 

