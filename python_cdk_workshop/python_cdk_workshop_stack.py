from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_apigateway as apigw,
    aws_lambda as _lambda
)

from constructs import Construct
from cdk_dynamo_table_view import TableViewer
from .hitcounter import HitCounter

class PythonCdkWorkshopStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # define an AWS Lambda resource
        my_lambda = _lambda.Function(
                self, "hello_handler",
                runtime=_lambda.Runtime.PYTHON_3_10,
                code=_lambda.Code.from_asset('lambda'),
                handler="hello.handler",
                )

        hello_with_counter = HitCounter(
            self, 'HelloHitCounter',
            downstream=my_lambda,
        )

        apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=hello_with_counter.handler,
        )

        TableViewer(
            self, 'ViewHitCounter',
            title='Hello Hits',
            table=hello_with_counter.table,
            sort_by='-hits'
        )
