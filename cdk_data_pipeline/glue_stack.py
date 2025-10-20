from aws_cdk import (
    Stack,
    aws_glue as glue,
    aws_iam as iam
)
from constructs import Construct

class GlueStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, data_bucket, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1. Base de datos Glue
        self.database = glue.CfnDatabase(
            self, "GlueDatabase",
            catalog_id=self.account,
            database_input=glue.CfnDatabase.DatabaseInputProperty(
                name="cdk_data_pipeline_db_users"
            )
        )

        # 2. Rol de ejecución para el Crawler
        self.crawler_role = iam.Role(
            self, "CrawlerRole",
            assumed_by=iam.ServicePrincipal("glue.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSGlueServiceRole")
            ]
        )

        # Permitir que el Crawler lea el bucket
        data_bucket.grant_read(self.crawler_role)

        # 3. Crawler que escanea solo
        self.crawler = glue.CfnCrawler(
            self, "GlueCrawler",
            role=self.crawler_role.role_arn,
            database_name=self.database.ref,
            targets=glue.CfnCrawler.TargetsProperty(
                s3_targets=[glue.CfnCrawler.S3TargetProperty(
                    path=f"s3://{data_bucket.bucket_name}/users/"  
                )]
            ),
            schema_change_policy=glue.CfnCrawler.SchemaChangePolicyProperty(
                delete_behavior="LOG",
                update_behavior="UPDATE_IN_DATABASE"
            ),
            name="cdk_data_pipeline_crawler"
        )
