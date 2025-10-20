from aws_cdk import (
    Stack,
    aws_lakeformation as lf,
    aws_iam as iam,
    aws_glue as glue
)
from constructs import Construct

class LakeFormationStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, glue_role_arn: str, data_bucket, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.lf_settings = lf.CfnDataLakeSettings(
            self, "LakeFormationSettings",
            admins=[
                lf.CfnDataLakeSettings.DataLakePrincipalProperty(
                    data_lake_principal_identifier=f"arn:aws:iam::{self.account}:root"
                )
            ]
        )

        self.s3_resource = lf.CfnResource(
            self, "DataBucketResource",
            resource_arn=data_bucket.bucket_arn,
            use_service_linked_role=True
        )

        self.s3_permissions = lf.CfnPermissions(
            self, "S3DataPermissions",
            data_lake_principal=lf.CfnPermissions.DataLakePrincipalProperty(
                data_lake_principal_identifier=glue_role_arn
            ),
            resource=lf.CfnPermissions.ResourceProperty(
                data_location_resource=lf.CfnPermissions.DataLocationResourceProperty(
                    s3_resource=data_bucket.bucket_arn
                )
            ),
            permissions=["DATA_LOCATION_ACCESS"]
        )
        self.s3_permissions.add_dependency(self.s3_resource)

        self.db_permissions = lf.CfnPermissions(
            self, "GlueDatabasePermissions",
            data_lake_principal=lf.CfnPermissions.DataLakePrincipalProperty(
                data_lake_principal_identifier=glue_role_arn
            ),
            resource=lf.CfnPermissions.ResourceProperty(
                database_resource=lf.CfnPermissions.DatabaseResourceProperty(
                    catalog_id=self.account,
                    name="cdk_data_pipeline_db_users"
                )
            ),
            permissions=["ALL"]
        )
