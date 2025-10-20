import aws_cdk as core
import aws_cdk.assertions as assertions
import pytest

from cdk_data_pipeline.storage_stack import StorageStack
from cdk_data_pipeline.ingestion_stack import IngestionStack
from cdk_data_pipeline.glue_stack import GlueStack
from cdk_data_pipeline.athena_stack import AthenaStack

def test_storage_stack():
    """Test que StorageStack crea los buckets correctos"""
    app = core.App()
    storage_stack = StorageStack(app, "StorageStack")
    template = assertions.Template.from_stack(storage_stack)
    
    # Verificar que se crea el bucket de datos
    template.has_resource_properties("AWS::S3::Bucket", {
        "BucketName": "cdk-data-bucket-oscar"
    })
    
    # Verificar que se crea el bucket de resultados de Athena
    template.has_resource_properties("AWS::S3::Bucket", {
        "BucketName": "cdk-athena-results-oscar"
    })

def test_glue_stack():
    """Test que GlueStack crea la base de datos y crawler"""
    app = core.App()
    storage_stack = StorageStack(app, "StorageStack")
    glue_stack = GlueStack(app, "GlueStack", data_bucket=storage_stack.data_bucket)
    template = assertions.Template.from_stack(glue_stack)
    
    # Verificar que se crea la base de datos Glue
    template.has_resource_properties("AWS::Glue::Database", {
        "DatabaseInput": {
            "Name": "cdk_data_pipeline_db_users"
        }
    })
    
    # Verificar que se crea el crawler
    template.has_resource_properties("AWS::Glue::Crawler", {
        "DatabaseName": {"Ref": "GlueDatabase"},
        "Name": "cdk_data_pipeline_crawler"
    })

def test_athena_stack():
    """Test que AthenaStack crea el WorkGroup"""
    app = core.App()
    storage_stack = StorageStack(app, "StorageStack")
    athena_stack = AthenaStack(app, "AthenaStack", results_bucket=storage_stack.results_bucket)
    template = assertions.Template.from_stack(athena_stack)
    
    # Verificar que se crea el WorkGroup de Athena
    template.has_resource_properties("AWS::Athena::WorkGroup", {
        "Name": "cdk_data_pipeline_wg_users",
        "State": "ENABLED"
    })