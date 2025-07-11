import boto3
import os

def lambda_handler(event, context):
    """Lambda entry point. Connects to AWS Glue, checks the crawler state, and
    starts the crawler if it's in the READY state."""
    
    glue = boto3.client('glue')

    crawler_name = os.environ.get('CRAWLER_NAME')

    try:
        response = glue.get_crawler(Name=crawler_name)
        print(f"✅ Lambda can reach the crawler '{crawler_name}'.")
        crawler_state = response['Crawler']['State']
        print(f"Crawler state:", crawler_state)

        if crawler_state == 'READY':
            glue.start_crawler(Name=crawler_name)
            print(f"✅ Started Glue Crawler: {crawler_name}")
        else:
            print(f"❌ Error starting crawler: {str(e)}")
        
    except glue.exceptions.EntityNotFoundException:
        print(f"❌ Crawler '{crawler_name}' does not exist.")
    except Exception as e:
        print(f"❌ Error accessing crawler: {str(e)}")
        raise

    return { 
        'statusCode': 200,
        'body': f'Lambda function and ${crawler_name} crawler executed successfully'
    }
