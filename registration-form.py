import json
import boto3
import uuid
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('registration-table')
ses_client = boto3.client('ses', region_name='eu-central-1')

def send_verification_email(email, token):
    SENDER = "isport2.0@outlook.de"
    RECIPIENT = email
    SUBJECT = "Please verify your email address"
    VERIFICATION_LINK = f"https://yb8ev7e9hh.execute-api.eu-central-1.amazonaws.com/prod/verify?token={token}"
    BODY_TEXT = f"Please verify your email by clicking on the following link: {VERIFICATION_LINK}"
    BODY_HTML = f"""<html>
    <head></head>
    <body>
      <h1>Please verify your email address</h1>
      <p>Please verify your email by clicking on the following link: <a href='{VERIFICATION_LINK}'>Verify Email</a></p>
    </body>
    </html>"""

    CHARSET = "UTF-8"

    try:
        response = ses_client.send_email(
            Destination={
                'ToAddresses': [RECIPIENT],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
        print("Email sent! Message ID:", response['MessageId'])
    except ClientError as e:
        print("Error sending email:", e.response['Error']['Message'])
        raise

def lambda_handler(event, context):
    try:
        # Get request body
        print("Event: ", event)

        # Generate a unique token for email verification
        token = str(uuid.uuid4())

        # Create new item in DynamoDB table
        response = table.put_item(
            Item={
                'vorname': event['vorname'],
                'nachname': event['nachname'],
                'email': event['email'],
                'geburtsdatum': event['geburtsdatum'],
                'strasse': event['strasse'],
                'hausnummer': event['hausnummer'],
                'plz': event['plz'],
                'stadt': event['stadt'],
                'sicherheitsfrage': event['sicherheitsfrage'],
                'sicherheitsantwort': event['sicherheitsantwort'],
                'phone': event['phone'],
                'password': event['password'],
                'confirm_password': event['confirm_password'],
                'verification_token': token,
                'verified': False
            }
        )
        print("DynamoDB put_item response:", response)

        # Send verification email
        send_verification_email(event['email'], token)

        # Return response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'Registration successful. Please check your email to verify your account.'})
        }
    except Exception as e:
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'Registration failed. Please try again later.'})
        }
