pipeline {
    agent any

    environment {
        DOCKER_IMAGE     = "YOUR_DOCKERHUB_USERNAME/devops-ci-cd-demo"
        DOCKER_TAG       = "${env.BUILD_NUMBER}"
        DOCKER_LATEST    = "latest"
        K8S_NAMESPACE    = "devops-demo"
        DEPLOYMENT_NAME  = "devops-demo-app"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Checking out source code..."
                checkout scm
            }
        }

        stage('Install & Test') {
            steps {
                echo "Installing dependencies and running tests..."
                sh '''
                    pip install -r app/requirements.txt
                    pytest app/tests/ -v --tb=short
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image: ${DOCKER_IMAGE}:${DOCKER_TAG}"
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:${DOCKER_LATEST}"
            }
        }

        stage('Push to DockerHub') {
            steps {
                echo "Pushing image to DockerHub..."
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                        docker push ${DOCKER_IMAGE}:${DOCKER_LATEST}
                        docker logout
                    '''
                }
            }
        }

        stage('Update K8s Deployment Image') {
            steps {
                echo "Updating deployment image to ${DOCKER_IMAGE}:${DOCKER_TAG}..."
                sh '''
                    sed -i "s|image: .*devops-ci-cd-demo.*|image: ${DOCKER_IMAGE}:${DOCKER_TAG}|g" k8s/deployment.yaml
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "Applying Kubernetes manifests..."
                sh '''
                    kubectl apply -f k8s/namespace.yaml
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
                    kubectl rollout status deployment/${DEPLOYMENT_NAME} -n ${K8S_NAMESPACE} --timeout=120s
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                echo "Verifying deployment health..."
                sh '''
                    kubectl get pods -n ${K8S_NAMESPACE}
                    kubectl get svc -n ${K8S_NAMESPACE}
                '''
            }
        }

    }

    post {
        success {
            echo "Pipeline succeeded. Build #${env.BUILD_NUMBER} deployed successfully."
        }
        failure {
            echo "Pipeline failed. Check logs for build #${env.BUILD_NUMBER}."
        }
        always {
            echo "Cleaning up local Docker images..."
            sh "docker rmi ${DOCKER_IMAGE}:${DOCKER_TAG} || true"
        }
    }
}
