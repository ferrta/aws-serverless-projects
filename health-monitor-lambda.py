import json
import pymysql
from datetime import datetime

# RDS database configuration
rds_host = "database-endpoint.region.rds.amazonaws.com"
username = "admin"
password = "yourpassword"  # Note: In production, use AWS Secrets Manager
db_name = "testdb"

def lambda_handler(event, context):
    """
    Automated database health monitoring system.
    Scheduled to run every 5 minutes via EventBridge.
    Checks database connectivity and logs health metrics.
    """
    
    try:
        print(f"Health check started at {datetime.now()}")
        
        # Connect to RDS
        connection = pymysql.connect(
            host=rds_host,
            user=username,
            password=password,
            database=db_name,
            connect_timeout=10
        )
        
        with connection.cursor() as cursor:
            # Count total records
            cursor.execute("SELECT COUNT(*) FROM test_data")
            count = cursor.fetchone()[0]
            
            # Get database size
            cursor.execute("""
                SELECT table_schema, 
                       SUM(data_length + index_length) / 1024 / 1024 AS size_mb
                FROM information_schema.tables 
                WHERE table_schema = %s
                GROUP BY table_schema
            """, (db_name,))
            size_result = cursor.fetchone()
            size_mb = float(size_result[1]) if size_result else 0.0
        
        connection.close()
        
        # Log results
        print(f"✅ Database Health Check:")
        print(f"   - Total records: {count}")
        print(f"   - Database size: {size_mb:.2f} MB")
        print(f"   - Status: HEALTHY")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'status': 'healthy',
                'record_count': count,
                'size_mb': round(size_mb, 2),
                'timestamp': str(datetime.now())
            })
        }
        
    except Exception as e:
        print(f"❌ Database Health Check FAILED: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'status': 'unhealthy',
                'error': str(e)
            })
        }
