import json
import boto3
import uuid
from datetime import datetime
from zoneinfo import ZoneInfo


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('registration-table')

def lambda_handler(event, context):
    # Get request body
    print(event)


    user_id = str(uuid.uuid4())


    # Get current time in UTC
    utc_time = datetime.utcnow()

    # Convert to local time (e.g., Europe/Berlin)
    local_tz = ZoneInfo('Europe/Berlin')
    local_time = utc_time.replace(tzinfo=ZoneInfo('UTC')).astimezone(local_tz)

    # Format the local time as an ISO string
    registrierungszeit = local_time.isoformat()
    

    # Create new item in DynamoDB table
    response = table.put_item(
        Item={
            'user_id': user_id,
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
            'registrierungszeit': registrierungszeit
        }
    )

    # Return response
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'message': 'Registrierung ist erfolgreich!', 'user_id': user_id})
    }