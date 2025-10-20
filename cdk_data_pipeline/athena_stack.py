from aws_cdk import (
    Stack,
    aws_athena as athena
)
from constructs import Construct

class AthenaStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, results_bucket, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Configuración de resultados de Athena
        self.workgroup = athena.CfnWorkGroup(
            self, "AthenaWorkGroup",
            name="cdk_data_pipeline_wg_users",
            description="WorkGroup for CDK Data Pipeline",
            state="ENABLED",
            work_group_configuration=athena.CfnWorkGroup.WorkGroupConfigurationProperty(
                result_configuration=athena.CfnWorkGroup.ResultConfigurationProperty(
                    output_location=f"s3://{results_bucket.bucket_name}/results/"
                )
            )
        )
