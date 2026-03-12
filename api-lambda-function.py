import json
import pymysql

# RDS settings
rds_host = "your-endpoint.us-east-1.rds.amazonaws.com"
username = "admin"
password = "yourpassword"
db_name = "testdb"

def lambda_handler(event, context):
    method = event.get('httpMethod', '')
    path = event.get('path', '')
    
    # CORS headers (used in all responses)
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    try:
        if method == 'GET' and path == '/health':
            connection = pymysql.connect(
                host=rds_host,
                user=username,
                password=password,
                database=db_name,
                connect_timeout=10
            )
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM test_data")
                count = cursor.fetchone()[0]
            
            connection.close()
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'status': 'healthy',
                    'record_count': count
                })
            }
        
        elif method == 'GET' and path == '/records':
            connection = pymysql.connect(
                host=rds_host,
                user=username,
                password=password,
                database=db_name,
                connect_timeout=10
            )
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, message, created_at FROM test_data ORDER BY id")
                results = cursor.fetchall()
                
                records = []
                for row in results:
                    records.append({
                        'id': row[0],
                        'message': row[1],
                        'created_at': str(row[2])
                    })
            
            connection.close()
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'records': records})
            }
        
        elif method == 'POST' and path == '/records':
            body = json.loads(event.get('body', '{}'))
            message = body.get('message', '')
            
            if not message:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({'error': 'Message is required'})
                }
            
            connection = pymysql.connect(
                host=rds_host,
                user=username,
                password=password,
                database=db_name,
                connect_timeout=10
            )
            
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO test_data (message) VALUES (%s)",
                    (message,)
                )
                connection.commit()
                new_id = cursor.lastrowid
            
            connection.close()
            
            return {
                'statusCode': 201,
                'headers': headers,
                'body': json.dumps({
                    'message': 'Record created',
                    'id': new_id
                })
            }
        
        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'Not found'})
            }
    
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }
