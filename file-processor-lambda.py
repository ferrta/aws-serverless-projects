import json
import boto3

# S3 client
s3 = boto3.client('s3')

def lambda_handler(event, context):
    """
    S3-triggered Lambda function for automated file processing.
    Analyzes uploaded text files (word count, line count, character count).
    Generates analysis report and saves it back to S3 in 'analysis/' folder.
    
    Triggered automatically when files are uploaded to S3 bucket.
    """
    
    print("Event received:", json.dumps(event))
    
    # Get bucket and file info from the S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    print(f"Processing file: {key} from bucket: {bucket}")
    
    try:
        # Read the file from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        file_content = response['Body'].read().decode('utf-8')
        
        print(f"File content length: {len(file_content)} characters")
        
        # Analyze the text
        char_count = len(file_content)
        line_count = len(file_content.splitlines())
        word_count = len(file_content.split())
        
        # Create analysis report
        analysis = f"""
File Analysis Report
====================
File: {key}
Bucket: {bucket}

Statistics:
- Characters: {char_count}
- Lines: {line_count}
- Words: {word_count}
        """
        
        print(analysis)
        
        # Save analysis to S3 (in 'analysis' folder)
        analysis_key = f"analysis/{key.split('/')[-1]}_analysis.txt"
        
        s3.put_object(
            Bucket=bucket,
            Key=analysis_key,
            Body=analysis,
            ContentType='text/plain'
        )
        
        print(f"Analysis saved to: {analysis_key}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'File processed successfully',
                'analysis_file': analysis_key,
                'stats': {
                    'characters': char_count,
                    'lines': line_count,
                    'words': word_count
                }
            })
        }
        
    except Exception as e:
        print(f"Error processing file: {e}")
        raise e
