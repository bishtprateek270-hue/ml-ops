


pipeline {

    agent any

    environment {
        IMAGE_NAME = "house-price"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/chandranitu/mlflow-homeprice.git'
            }
        }

        stage('Python Environment') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Train Model') {
            steps {
                sh '''
                . venv/bin/activate
                python train.py
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t house-price:${BUILD_NUMBER} .
                '''
            }
        }

        stage('Push Image') {
            steps {
                sh '''
                docker tag house-price:${BUILD_NUMBER} \
                docker.io/<dockerhub-user>/house-price:${BUILD_NUMBER}

                docker push \
                docker.io/<dockerhub-user>/house-price:${BUILD_NUMBER}
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                kubectl set image deployment/house-price \
                house-price=docker.io/<dockerhub-user>/house-price:${BUILD_NUMBER}
                '''
            }
        }

        stage('Verify') {
            steps {
                sh '''
                kubectl rollout status deployment/house-price
                '''
            }
        }
    }
}
