from constructs import Construct
from aws_cdk import (
    aws_lambda as _lambda,
    aws_dynamodb as ddb,
    RemovalPolicy
)

from os import path

class HitCounter(Construct):

    @property
    def handler(self):
        return self._handler

    @property
    def table(self):
        return self._table

    def __init__(self, scope: Construct, id: str, downstream: _lambda.IFunction, **kwargs):
        super().__init__(scope, id, **kwargs)

        self._table = ddb.Table(
            self, 'Hits',
            partition_key={'name': 'path', 'type': ddb.AttributeType.STRING},
            removal_policy=RemovalPolicy.DESTROY
        )

#        #layer for external dependencies
#        my_layer = _lambda.LayerVersion(self, "MyLayer",
#            #removal_policy=RemovalPolicy.RETAIN,
#            code=_lambda.Code.from_asset(path.join(path.abspath('/Users/rajesh.kaushik/projects/python_cdk_workshop'), ".venv/lib/python3.10/site-packages")),
#            compatible_runtimes=[_lambda.Runtime.PYTHON_3_10],
#            compatible_architectures=[_lambda.Architecture.X86_64, _lambda.Architecture.ARM_64]
#        )

        self._handler = _lambda.Function(
            self, 'HitCountHandler',
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler='hitcount.handler',
            code=_lambda.Code.from_asset('lambda'),
#            layers=[my_layer],
            environment={
                'DOWNSTREAM_FUNCTION_NAME': downstream.function_name,
                'HITS_TABLE_NAME': self._table.table_name,
            }
        )

        self._table.grant_read_write_data(self._handler)
        downstream.grant_invoke(self._handler)
