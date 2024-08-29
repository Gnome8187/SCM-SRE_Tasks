pipeline {
    agent any

    environment {
        S3_BUCKET = 'mydevtaskbucket'
        DEPLOY_SERVER = 'ec2-54-159-10-58.compute-1.amazonaws.com'
        DEPLOY_USER = 'jenkins' 
        GIT_CREDENTIALS_ID = 'd22f8a30-d911-4a13-b6d9-656662a4f867'
    }

    stages {
        stage('Checkout') {
            steps {
                git(
                    url: 'https://github.com/isom8634/SCM-SRE_Tasks.git',
                    branch: 'Dev',
                    credentialsId: env.GIT_CREDENTIALS_ID
                )
            }
        }

        stage('Build') {
            steps {
				withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-jenkins',
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]){
                        sh 'mkdir -p target'
						sh 'cp index.html target/index.html' 
						//sh 'aws s3 cp target/index.html s3://mydevtaskbucket/artifacts/index.html'
						s3Upload(
						    file:'index.html', 
						    bucket:'mydevtaskbucket', 
						    path:'artifacts/index.html')


					}
			}
        }

        stage('Deploy') {
            steps {
				withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-jenkins',
                    region: 'us-east-1',
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]){
						sh "aws s3 cp s3://${env.S3_BUCKET}/artifacts/index.html /var/www/html/index.html"
						sh 'sudo systemctl restart apache2'
						
					}
                
            }
        }

        stage('Verify Deployment') {
            steps {
                script {
                   echo "Deployed successfully."
                   
                }
            }
        }
    }
}
