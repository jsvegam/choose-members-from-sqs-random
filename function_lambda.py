import json
import random
import boto3
from datetime import date
import calendar

# Create SQS client
sqs = boto3.client('sqs')
queue_url = 'https://sqs.us-east-1.amazonaws.com/806175290270/DayliMembers'



def lambda_handler(event, context):
    # TODO implement
    
    # Receive message from SQS queue
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )
    
    existMsg = is_json_key_present(response, 'Messages')
    message_body = "" 
    
    
    if existMsg:
        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']

        # Delete received message from queue
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        print('Received and deleted message: %s' % message)
        message_body = message["Body"]
    else:
        message_body = "Ruleta finalizada"
    

    return {
        'statusCode': 200,
        'body': json.dumps(f"Message body: " + message_body)
    }

def is_json_key_present(json, key):
    try:
        buf = json[key]
    except KeyError:
        return False

    return True
