import os
import json
import boto3
import datetime
def get_messages_from_queue(queue_url):
    aws_mg_con=boto3.session.Session(profile_name=input("Please enter your AWS Prod environment Username"))
    sqs_client=aws_mg_con.client(service_name='sqs',region_name='us-west-2')
    sqs_re=aws_mg_con.resource(service_name='sqs',region_name='us-west-2')
    #sqs_client=boto3.client(service_name='sqs',region_name='us-west-2')
    #sqs_re=boto3.resource(service_name='sqs',region_name='us-west-2')
    folder_path=r"C:\download\python\script"
    os.chdir(folder_path)
    os.mkdir(datetime.datetime.now().strftime('%Y-%m-%d'),0o777)
    while True:
        sqs_ms= sqs_client.receive_message(
            QueueUrl=queue_url,
            AttributeNames=['All'],
            MaxNumberOfMessages=10
        )
        try:
                for msg_id in sqs_ms['Messages']:
                    message_id=msg_id['MessageId']
                    receipt_handle=msg_id['ReceiptHandle']
                    convert_json=json.loads(msg_id['Body'])
                    for message in convert_json['Records']:
                        msg_body=message['Sns']['Message']
                        for root_,dir_,files_ in os.walk(folder_path):
                            if root_==os.path.join(folder_path,f"{datetime.datetime.now().strftime('%Y-%m-%d')}"):
                                date_folder_path=os.path.join(folder_path,f"{datetime.datetime.now().strftime('%Y-%m-%d')}")
                                path_save=os.path.join(date_folder_path,f"{message_id}")
                                file1=open(path_save,'wt')
                                file1.write(str(msg_body))
                                file1.close()
                yield from sqs_ms['Messages']
        except KeyError:
            return
        entries = [
            {'Id': msg['MessageId'], 'ReceiptHandle': msg['ReceiptHandle']}
            for msg in sqs_ms['Messages']
        ]
        sqs_ms = sqs_client.delete_message_batch(
            QueueUrl=queue_url, Entries=entries
        )
sqs_msg_output=get_messages_from_queue('https://sqs.us-west-2.amazonaws.com/123456789012/orders-status')
for msg_output in sqs_msg_output:
    print(msg_output)
