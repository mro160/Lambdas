import json
import os
import pymysql



def lambda_handler(event, context):
    db_host = os.getenv('db_host')
    db_user = os.getenv('db_user')
    pwd = os.getenv('password')
    db_name = os.getenv('db_name')

    conn = pymysql.connect(host=db_host, user=db_user, password=pwd, db=db_name)
    # TODO implement
    cursor = conn.cursor()
    sql = 'SELECT * FROM Guests'
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
