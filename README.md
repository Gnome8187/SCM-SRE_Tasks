# SCM-SRE_Tasks
This repository is related to the Task which given by the team

Goal of the assignments
* Get familiarized with CI/CD and Jenkins
* Hands on experience with Windows and PowerShell
* Improve knowledge on python with AWS
 
CI/CD
-------
 Create a fully automated build pipeline to build and deploy code
Example scenario :
 
You can use default Apache installation and its index.html to demo the pipeline. Task is to modify the index.html publish to "dev" branch, which should trigger the build job which should put files into an artifact repository or s3 bucket. Once its success, trigger the deploy job to get the latest files into app server and restart Apache. And publish the status code of Apache web page as the outcome of the deploy job.
 
Optional: Integrate with SonarQube to run a static code analysis to get the code coverage and pass the build based on that to trigger the deploy job
 
Windows/PowerShell
---------------------------
 
Create a scheduled task using PowerShell to do the below task
- Create a log directory and put some sample log files into it.
- Write a logic to remove log files older than x days and output the list of deleted files into a file. Also get the total size of deleted files and show it as a percentage from the total Disk storage in the same file as freed storage percent.
- And publish this file into a s3 bucket
- Save this script as logCleanup.ps1
- And another script to provision the scheduled task using PowerShell
 
 
Python/AWS
-----------------
 
Create a lambda function using python to cater below requirement
 
Create a report to list all the ec2 instances and its security group rules as a summary. You can display the report in any format.
Ex:
Instance Name, Port/Port range, Source
 
i-xxxxx, 80, 10.0.0.0/8
i-xxxxx, 8080, 10.0.0.0/8
i-yyyy, 8090, 10.0.0.0/8
 
Optional: Send an email with the report created

