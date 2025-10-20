# from aws_cdk import (
#     Stack,
#     aws_glue as glue,
#     aws_iam as iam
# )
# from constructs import Construct

# class GlueWithoutCrawlerStack(Stack):
#     def __init__(self, scope: Construct, construct_id: str, data_bucket, **kwargs) -> None:
#         super().__init__(scope, construct_id, **kwargs)

#         # Base de datos en Glue Catalog
#         self.database = glue.CfnDatabase(
#             self, "GlueDatabase",
#             catalog_id=self.account,
#             database_input=glue.CfnDatabase.DatabaseInputProperty(
#                 name="cdk_data_pipeline_db_users"
#             )
#         )

#         # Tabla Glue que apunta al bucket
#         self.table = glue.CfnTable(
#             self, "GlueTable",
#             catalog_id=self.account,
#             database_name=self.database.ref,
#             table_input=glue.CfnTable.TableInputProperty(
#                 name="users",
#                 table_type="EXTERNAL_TABLE",
#                 storage_descriptor=glue.CfnTable.StorageDescriptorProperty(
#                     location=f"s3://{data_bucket.bucket_name}/users/",
#                     input_format="org.apache.hadoop.mapred.TextInputFormat",
#                     output_format="org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat",
#                     serde_info=glue.CfnTable.SerdeInfoProperty(
#                         serialization_library="org.openx.data.jsonserde.JsonSerDe"
#                     ),
#                     columns=[
#                         glue.CfnTable.ColumnProperty(name="id", type="int"),
#                         glue.CfnTable.ColumnProperty(name="name", type="string"),
#                         glue.CfnTable.ColumnProperty(name="username", type="string"),
#                         glue.CfnTable.ColumnProperty(name="email", type="string"),
#                         glue.CfnTable.ColumnProperty(name="phone", type="string"),
#                         glue.CfnTable.ColumnProperty(name="website", type="string")
#                     ]
#                 )
#             )
#         )
