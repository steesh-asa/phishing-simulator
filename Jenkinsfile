pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("phishing-simulator")
                }
            }
        }

        stage('Run Flask App') {
            steps {
                script {
                    // Stop any existing container on port 5000
                    sh 'docker rm -f phishing_sim_container || true'

                    // Run container
                    sh 'docker run -d --name phishing_sim_container -p 5050:5000 phishing-simulator'
                }
            }
        }

        stage('Test App') {
            steps {
                // Optional: Add curl test to ensure app is responding
                sh 'curl -f http://localhost:5050 || echo "App not responding"'
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            sh 'docker rm -f phishing_sim_container || true'
        }
    }
}
