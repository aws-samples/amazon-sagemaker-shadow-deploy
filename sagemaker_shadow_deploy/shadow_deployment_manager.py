from aws_cdk import (
    aws_lambda as _lambda,
    aws_dynamodb as ddb,
    aws_iam as iam,
    core,
)


class ShadowDeploymentManager(core.Construct):

    @property
    def handler(self):
        return self._handler

    @property
    def table(self):
        return self._table

    def __init__(self, scope: core.Construct, id: str, ep1: str, ep2: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        self._table = ddb.Table(
            self, 'ShadowDeploymentLog',
            partition_key={'name': 'endpointName', 'type': ddb.AttributeType.STRING}
        )

        self._handler = _lambda.Function(
            self, 'ShadowDeploymentHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler='shadowDeployment.handler',
            code=_lambda.Code.asset('lambda'),
            environment={
                'ENDPOINT_NAME_V1': ep1,
                'ENDPOINT_NAME_V2': ep2,
                'SHADOW_DEPLOYMENT_LOG': self._table.table_name
            }
        )

        self._handler.add_to_role_policy(iam.PolicyStatement(actions=['sagemaker:InvokeEndpoint', ],
                                                             resources=['*']))

        self._table.grant_read_write_data(self.handler)
