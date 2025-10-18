import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_data_pipeline.cdk_data_pipeline_stack import CdkDataPipelineStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_data_pipeline/cdk_data_pipeline_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkDataPipelineStack(app, "cdk-data-pipeline")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
