def sns_publish():
    import boto3
    import os,datetime
    # Once you execute this script it will ask your username which you update in your credential file. 
    aws_mg_con=boto3.session.Session(profile_name=input("Please enter your AWS Prod environment Username"))
    # service name is 'sns' and region is 'us-west-2'
    sns_client=aws_mg_con.client(service_name='sns',region_name='us-west-2')
    sns_r=aws_mg_con.resource(service_name='sns',region_name='us-west-2')
    #sns_client=boto3.client(service_name='sns',region_name='us-west-2')
    #sns_resources=boto3.resource(service_name='sns',region_name='us-west-2')
    # joining path with current date  and time folder
    path_join=os.path.join(r'C:\download\python\script',f"{datetime.datetime.now().strftime('%Y-%m-%d')}")

    
    
    directory_path=os.listdir(path_join)
    Message_count=0
    for files in directory_path:
            files_=os.path.join(path_join,f"{files}")
            read_file=open(files_,'r')
            file_data=read_file.read()
            read_file.close()
            # print(data)
            response=sns_client.publish(Message=file_data,TopicArn='arn:aws:sns:us-west-2:123456789012:Order-Status-sns-topic')
            print(response['MessageId'])
            Message_count +=1
    print("Total number of messages published through SNS is",Message_count)
sns_publish()
