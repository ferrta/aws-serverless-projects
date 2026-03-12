import json
import pymysql

# RDS database configuration
# Note: In production, credentials should be stored in AWS Secrets Manager
rds_host = "database-endpoint.region.rds.amazonaws.com"  # Replace with actual endpoint
username = "admin"
password = "your-database-password"  # Replace with actual password
db_name = "testdb"

def lambda_handler(event, context):
    """
    REST API handler for database CRUD operations.
    Supports three endpoints:
    - GET /health: Database health check
    - GET /records: Retrieve all records
    - POST /records: Create new record
    
    Triggered via API Gateway with Lambda proxy integration.
    """
    
    method = event.get('httpMethod', '')
    path = event.get('path', '')
    
    # CORS headers for browser access
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    try:
        # GET /health - Database health check
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
        
        # GET /records - Retrieve all records
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
                
                # Format results as JSON-serializable list
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
        
        # POST /records - Create new record
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
        
        # Route not found
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
