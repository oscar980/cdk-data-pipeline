#!/usr/bin/env python3
import aws_cdk as cdk
from cdk_data_pipeline.storage_stack import StorageStack
from cdk_data_pipeline.ingestion_stack import IngestionStack
from cdk_data_pipeline.glue_stack import GlueStack
from cdk_data_pipeline.athena_stack import AthenaStack

app = cdk.App()

storage_stack = StorageStack(app, "StorageStack")

ingestion_stack = IngestionStack(app, "IngestionStack",
    data_bucket=storage_stack.data_bucket)

glue_stack = GlueStack(app, "GlueStack",
    data_bucket=storage_stack.data_bucket)

athena_stack = AthenaStack(app, "AthenaStack",
    results_bucket=storage_stack.results_bucket)

app.synth()