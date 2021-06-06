Feature Enhancement - https://github.com/aws-cloudformation/aws-cloudformation-coverage-roadmap/issues/308

Workaround:
--------------
Functionalities which are not natively supported by the cloudformation could be solved with the help of custom resource cloudformation where you could specify a lambda function ARN to invoke any logic and get back results to cloudformation state objects.

**Steps:**
1. Download the attached lambda-function python code and deploy it in same region as cloudformation stack.
The lambda function takes VPN Resource ID as a input argument from cloudformation and gives back the TransitGateway attachment id as response.

2. Download the attached sample cloudformation and use it as a base or use similar approach to reference the TransitGateway Attachment ID from the custom resource.
Please have a look at the comments in the cloudformation manifest for the use-case of each resources.

  *Notes:* <br />
  A) Make sure the lambda execution role have enough permissions to invoke EC2 endpoint describe calls.<br />
  B) Any further enhancement on code logic customization could be done within the scope of 'def lambda_handler()'. In contrast, 'def send()' takes care of constructing cfnresponse to signal back the cloudformation stack with results whenever it gets invoked by cloudformation stack.


**Things to Consider:** <br />
In the above steps, we have deployed the custom lambda function outside of the respective cloudformation stack, As I consider this function as a general purpose use by other future stacks. However please feel free to create the function on the same stack if you like to have the same.

**References:** <br />
1. Cloudformation custom resources - https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html <br />
2. Boto core Describe call - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_transit_gateway_attachments <br />
