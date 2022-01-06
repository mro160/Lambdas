import json
import sys
import os
import pymysql


db_host = os.getenv('db_host')
db_user = os.getenv('db_user')
pwd = os.getenv('password')
db_name = os.getenv('db_name')

def lambda_handler(event, context):
    conn = pymysql.connect(host=db_host, user=db_user, password=pwd, db=db_name)
    for message in event['Records']:
        newGuest = json.loads(message['body'])
        cursor = conn.cursor()
        try:
            sql = 'INSERT INTO `Guests` VALUES (%s, %s, %s, %s, %s)'
            cursor.execute(sql, (newGuest['uniqueId'], newGuest['fullName'], newGuest['countryCode'], newGuest['phoneNumber'], newGuest['email'])) 
            conn.commit()
        except pymysql.Error as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))
            return {
                'statusCode': 409,
                'body': json.dumps(str(e))
            }
    return {
        'statusCode': 201,
    }
    #process messages from sqs queue
    #write payload to rds
    
    