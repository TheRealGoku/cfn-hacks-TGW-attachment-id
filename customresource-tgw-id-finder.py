import urllib3
import json
import boto3
http = urllib3.PoolManager()
SUCCESS = "SUCCESS"
FAILED = "FAILED"


def send(event, context, responseStatus, responseData, physicalResourceId=None, noEcho=False):
    responseUrl = event['ResponseURL']
    print(responseUrl)
    responseBody = {}
    responseBody['Status'] = responseStatus
    responseBody['Reason'] = 'See the details in CloudWatch Log Stream: ' + \
        context.log_stream_name
    responseBody['PhysicalResourceId'] = physicalResourceId or context.log_stream_name
    responseBody['StackId'] = event['StackId']
    responseBody['RequestId'] = event['RequestId']
    responseBody['LogicalResourceId'] = event['LogicalResourceId']
    responseBody['NoEcho'] = noEcho
    responseBody['Data'] = responseData
    json_responseBody = json.dumps(responseBody)
    print("Response body:\n" + json_responseBody)
    headers = {
        'content-type': '',
        'content-length': str(len(json_responseBody))
    }
    try:
        response = http.request(
            'PUT', responseUrl, body=json_responseBody.encode('utf-8'), headers=headers)
        print("Status code: " + response.reason)
    except Exception as e:
        print("send(..) failed executing requests.put(..): " + str(e))


def lambda_handler(event, context):
    try:
        if(event['RequestType'] == 'Create' or 'Update'):
            vpnID = event['ResourceProperties']['vpnID']
            client = boto3.client('ec2')
            response = client.describe_transit_gateway_attachments(
                Filters=[
                    {
                        'Name': 'resource-id',
                        'Values': [
                            vpnID
                        ]
                    },
                ],
            )
            responseData = {}
            responseData['TransitGatewayAttachmentId'] = response['TransitGatewayAttachments'][0]['TransitGatewayAttachmentId']
            send(event, context, SUCCESS, responseData)
        else:
            print("No action required")
        if(event['RequestType'] == 'Delete'):
            responseData = {}
            send(event, context, SUCCESS, responseData)
    except Exception as e:
        print('Failed to process:', e)
        responseData = {}
        send(event, context, FAILED, responseData)
