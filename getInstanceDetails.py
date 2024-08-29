import boto3
import io
import csv

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')  #creating client object
    s3 = boto3.client('s3')
    response = ec2.describe_instances()  #getting instance details

    reportfile = []

    for values in response ['Reservations']: #Reservations comes from boto3(describe_instance) 
        for value in values['Instances']: #Instances aslso have it's value set.
            instance_id = value['InstanceId']
            instance_name = ''

            for tagValue in value.get('Tags',[]): # a list of tag objects and from there get the name
                if tagValue['Key'] == 'Name':
                    instance_name = tagValue['Value']

            security_groups = value['SecurityGroups']
            sg_ids = [sg['GroupId'] for sg in security_groups]
            
            if sg_ids:
                # Describe security groups with correct IDs
                sg_details = ec2.describe_security_groups(GroupIds=sg_ids)
                for data in sg_details['SecurityGroups']:
                    for permission_values in data.get('IpPermissions', []):
                        ports = [] #To keep port numbers

                        if 'FromPort' in permission_values and 'ToPort' in permission_values:
                            ports.append(str(permission_values['FromPort']))
                            if permission_values['FromPort'] != permission_values['ToPort']:
                                ports.append(str(permission_values['ToPort']))
                        else:
                            ports.append('ALL')

                        for ip_address in permission_values.get('IpRanges',[]):
                            print(ip_address)
                            reportfile.append({
                                'Instance Name' : instance_name,
                                'Port/Port Range' : ','.join(ports),
                                'Source' : ip_address['CidrIp']
                            })
    
    #csv_report = 'Instance Name, Port/Port Range, Source \n'
    #for entry in reportfile:
    #    csv_report += f"{entry['Instance Name']},{entry['Port/Port Range']},{entry['Source']}\n"

    #s3.put_object(Bucket='mydevtaskbucket', Key=csv_report,  ContentType='text/csv')
    # Create a CSV string using StringIO
    csv_buffer = io.StringIO()
    csv_writer = csv.DictWriter(csv_buffer, fieldnames=['Instance Name', 'Port/Port Range', 'Source'])
    csv_writer.writeheader()
    csv_writer.writerows(reportfile)
    
    # Upload CSV to S3
    s3.put_object(
        Bucket='mydevtaskbucket',
        Key='ec2_security_group_report.csv',
        Body=csv_buffer.getvalue(),
        ContentType='text/csv'
    )

    return {
        'statusCode' : 200,
        'body' : 'CSV file uploaded successfully',
        'headers' : {
            'Content-Type': 'text/csv',
            'Content-Disposition' : 'attachment; filename="ec2_security_group_report.csv"'
        }
    }
