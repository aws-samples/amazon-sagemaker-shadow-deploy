import json
import pytest

from aws_cdk import core
from sagemaker-shadow-deploy.sagemaker_shadow_deploy_stack import SagemakerShadowDeployStack


def get_template():
    app = core.App()
    SagemakerShadowDeployStack(app, "sagemaker-shadow-deploy")
    return json.dumps(app.synth().get_stack("sagemaker-shadow-deploy").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
