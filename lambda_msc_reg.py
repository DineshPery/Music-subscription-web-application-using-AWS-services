import boto3
from botocore.exceptions import ClientError
import json

"""code adapted from amazonaws:
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html
"""

def lambda_handler(event, context):
    email = event['email']
    username = event['username']
    password = event['password']

    try:
        dynamodb = boto3.resource('dynamodb')
        table_login = dynamodb.Table('login')

        response_email = table_login.query(KeyConditionExpression=boto3.dynamodb.conditions.Key('email').eq(email))

        if response_email['Items']:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': "The email already exists"})
            }
        else:
            table_login.put_item(Item={'email': email, 'user_name': username, 'password': password})
            return {
                'statusCode': 200,
                'body': json.dumps({'message': "User registered successfully"})
            }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"Error: {e}"})
        }
