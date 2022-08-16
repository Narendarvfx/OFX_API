pipeline{
    agent any
    stages{
        stage('Setup Python Virtual Environment')
        {
            sh '''
            chmod +x envsetup.sh
            ./envsetup.sh
            '''
        }
        stage('Gunicorn Setup'){
            steps{
                sh '''
                chmod +x gunicorn.sh
                ./gunicorn.sh
                '''
            }
        }
        stage('Nginx Setup'){
            steps{
                sh '''
                chmod +x nginx.sh
                ./nginx.sh
                '''
            }
        }
    }
}