import json
import pymysql

rds_host = "testdb.csre00c88oj9.us-east-1.rds.amazonaws.com"
username = "admin"
password = "yourpassword"  # Note: In production, use AWS Secrets Manager
db_name = "testdb"

def lambda_handler(event, context):
    try:
        print(f"Connecting to {rds_host}...")
        
        connection = pymysql.connect(
            host=rds_host,
            user=username,
            password=password,
            database=db_name,
            connect_timeout=10
        )
        
        print("✅ Connected to RDS!")
        
        with connection.cursor() as cursor:
            # Create a test table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS test_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Insert data from Lambda
            cursor.execute(
                "INSERT INTO test_data (message) VALUES (%s)",
                ("Hello from Lambda! This worked!",)
            )
            connection.commit()
            
            # Read it back
            cursor.execute("SELECT * FROM test_data ORDER BY id DESC LIMIT 5")
            results = cursor.fetchall()
            print(f"Database records: {results}")
        
        connection.close()
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Success! Lambda wrote to RDS!',
                'records': str(results)
            })
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
