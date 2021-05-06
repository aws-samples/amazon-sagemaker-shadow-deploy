#!/usr/bin/env python3

from aws_cdk import core

from sagemaker_shadow_deploy.sagemaker_shadow_deploy_stack import SagemakerShadowDeployStack


app = core.App()


SagemakerShadowDeployStack(app, "sagemaker-shadow-deploy", env={'region': 'us-west-2'})

app.synth()
