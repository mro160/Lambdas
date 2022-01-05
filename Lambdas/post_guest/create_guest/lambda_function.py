import json
import phonenumbers
import boto3
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

s3 = boto3.client('s3')
##get request
##save xml to s3 bucket
##check if response body, if not, send to dlq


def lambda_handler(event, context):
    xml_string = event['body-json']
    print('XML Type', type(xml_string))
    
    xml = BeautifulSoup(xml_string, "html.parser")
    print(xml)
    
    tag = xml.find("newprofilerequest")
    print('TAG VALUE ', tag)
    if not tag:
        return {
            'statusCode': 400,
            'Error': 'Missing NewProfileRequest tag'
        }
        
    
    guestInfo = {}
    guestInfo["uniqueId"] = int(xml.uniqueid.string.strip())
    guestInfo["fullName"] = xml.firstname.string.strip() + ' ' + xml.lastname.string.strip()
    guestInfo["countryCode"] = xml.countrycode.string.strip()
    guestInfo["email"] = xml.find(phonerole='EMAIL').phonenumber.string.strip()
    guestInfo["resortId"] = xml.resortid.string.strip()
    
    try:
        number = xml.find(phonerole='PHONE').phonenumber.string.strip()
        parsed_number = phonenumbers.parse(number, guestInfo['countryCode'])
        number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        guestInfo["phoneNumber"] = number.replace('+', '')
    except phonenumbers.NumberParseException:
        print("Not a Valid number")
        return {
            'statusCode': 400,
            'body': json.dumps('Bad XML')
        }
        
    filename = guestInfo['fullName'] + str(guestInfo['uniqueId']) + '.xml'
    filename = filename.replace(" ", "")
    
    with open('/tmp/' + filename, 'w') as data:
        data.write(xml_string)
    
    bucket = 'guestprofilesxml'
    response = s3.upload_file('/tmp/' + filename, bucket, filename)
    
    
    sqs = boto3.resource('sqs')

    # Get the queue
    queue = sqs.get_queue_by_name(QueueName='CreateGuestQueue')
    
    # Create a new message
    response = queue.send_message(MessageBody=json.dumps(guestInfo))
    
    # print(response)
    # print(guestInfo)
    return {
        'statusCode': 200,
        'body': json.dumps('Success'),
        'url': 'https://fqqhvx2e0d.execute-api.us-east-1.amazonaws.com/Dev/guests'
    }
