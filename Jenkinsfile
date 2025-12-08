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
                sh 'docker build -t flask-app:latest .'
            }
        }

        stage('Deploy Using Docker Compose') {
            steps {
                sh 'docker-compose down || true'
                sh 'docker-compose up -d --build'
            }
        }
    }
}

