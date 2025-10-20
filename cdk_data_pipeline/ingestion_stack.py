from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    Duration
)
from constructs import Construct
import os

class IngestionStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, data_bucket, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_path = os.path.join(os.getcwd(), "cdk_data_pipeline", "lambda_src")

        self.ingestion_lambda = _lambda.Function(
            self, "IngestionLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="data_ingestion.lambda_handler",
            code=_lambda.Code.from_asset(lambda_path),
            timeout=Duration.seconds(30),
            environment={
                "BUCKET_NAME": data_bucket.bucket_name
            }
        )

        data_bucket.grant_put(self.ingestion_lambda)
