pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                deleteDir()
                git branch: 'main', url: 'https://github.com/skfarid45/Flask-SQL-App.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker-compose build'
            }
        }

        stage('Deploy on EC2') {
            steps {
                sh 'docker-compose down || true'
                sh 'docker-compose up -d --build'
            }
        }
    }

    post {
        success {
            echo "Deployment Successful! Access app via EC2 Public IP :5000"
        }
        failure {
            echo "Deployment Failed!"
        }
    }
}

