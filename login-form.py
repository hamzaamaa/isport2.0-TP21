import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('registration-table')

def lambda_handler(event, context):
    try:
        # Parse the request body
        body = json.loads(event['body'])

        # Get email and password from request
        email = body['email']
        password = body['password']

        # Query the DynamoDB table for the user with the specified email
        response = table.query(
            IndexName='email-index',
            KeyConditionExpression=Key('email').eq(email)
        )

        if response['Count'] == 0:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'message': 'User not found'})
            }

        # Get the user item
        user = response['Items'][0]

        # Check if the password matches
        if user['password'] == password:
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'message': 'Login successful'})
            }
        else:
            return {
                'statusCode': 401,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'message': 'Invalid credentials'})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        }
