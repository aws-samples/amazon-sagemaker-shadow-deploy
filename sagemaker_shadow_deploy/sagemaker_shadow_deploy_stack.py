from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_apigateway as apigw,

    core
)
from aws_cdk.core import CfnParameter
from shadow_deployment_manager import ShadowDeploymentManager
from cdk_dynamo_table_viewer import TableViewer


class SagemakerShadowDeployStack(core.Stack):


    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)



        epV1 = core.CfnParameter(self, id="endpointNameV1", type="String", description="model endpoint v1",
                                            default="shadow-linear-endpoint-v1-202012300108")


        epV2 = core.CfnParameter(self, id="endpointNameV2", type="String", description="model endpoint v2",
                                 default="shadow-linear-endpoint-v2-202012300229")

        sdm = ShadowDeploymentManager(self, 'shadow_deployment_manager', epV1.value_as_string, epV2.value_as_string )


        api = apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=sdm.handler,
            proxy=True
        )









        TableViewer(
            self, 'ViewShadowDeployments',
            title='SageMaker Shadow Deployment Log',
            table=sdm._table,

        )



