import json
import boto3
import sys
import os
import pymysql



def lambda_handler(event, context):
    db_host = os.getenv('db_host')
    db_user = os.getenv('db_user')
    pwd = os.getenv('password')
    db_name = os.getenv('db_name')
        
    conn = pymysql.connect(host=db_host, user=db_user, password=pwd, db=db_name)
    print(event)
    
    for message in event['Records']:
        newGuest = json.loads(message['body'])
        print('ID: ', message['messageId'])
        print(newGuest)
    # print('GUEST TYPE', type(newGuest))
    # sqs = boto3.resource('sqs')

    # Get the queue
    # queue = sqs.get_queue_by_name(QueueName='CreateGuestQueue')
    # print('Queue: ', queue)
    # for message in queue.receive_messages():
    #     print('MESSAGE: ', message)
        try:
            cursor = conn.cursor()
            sql = 'INSERT INTO `Guests` VALUES (%s, %s, %s, %s, %s)'
            print(sql)
            print(conn)
            cursor.execute(sql, (newGuest['uniqueId'], newGuest['fullName'], newGuest['countryCode'], newGuest['phoneNumber'], newGuest['email'])) 
            #('55555555', 'Carlos De la Ossa', 'CO', '5055055555', 'cdelaossa@mynuvola.com')
            print(cursor)
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
    # rows = cursor.fetchall()
    
    #process messages from sqs queue
    #write payload to rds
    
    
