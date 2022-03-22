import json
import urllib.parse
import boto3

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('sample_table')

def csv_dump_to_dynamodb(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    bucket = event['Records'][0]['s3']['bucket']['name']
    csv_file_name = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        csv_object = s3.get_object(Bucket=bucket, Key=csv_file_name)
        file_reader = csv_object['Body'].read().decode("utf-8")
        print("File reader: ",file_reader)
        items = file_reader.split("\n")
        items = list(filter(None, items))
        print("Items: ",items)
        #Traverse throught the list pick elements one by one and push it to dynamodb table
        for item in items[1:]:
            temp = item.split(",")
            table.put_item(Item = {
                "id" : int(temp[0]),
                "name" : temp[1],
                "state" : temp[2],
                "update_date" : temp[3]
            })
        return 'success'
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(csv_file_name, bucket))
        raise e

