from aws_cdk import (
    Stack,
    aws_s3 as s3,
    RemovalPolicy
)
from constructs import Construct

class StorageStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Bucket para datos
        self.data_bucket = s3.Bucket(
            self, "DataBucket",
            bucket_name="cdk-data-bucket-oscar",
            versioned=False,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        # Bucket para resultados de Athena
        self.results_bucket = s3.Bucket(
            self, "AthenaResultsBucket",
            bucket_name="cdk-athena-results-oscar",
            versioned=False,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )
