pipeline {
    agent any

    stages {
        stage('SCM') {
            steps {
                echo 'Checking out from SCM'
                git url: 'https://bitbucket.org/Lewatw/ticronem.git'
            }
        }
        stage('SonarQube') {
            environment {
            scannerHome = tool 'Sonar1'
            }
            steps {
            echo 'Starting Sonar scan'
            withSonarQubeEnv('sonarqube') {
                bat "${scannerHome}/bin/sonar-scanner"
            }


            }
        }
        stage('Test') {
            steps {
                echo 'Testing'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying'
            }
        }
    }
    post {
        always {
            echo 'This will always run'
        }
        success {
            echo 'This will run only if successful'
        }
        failure {
            echo 'This will run only if failed'
        }
        unstable {
            echo 'This will run only if the run was marked as unstable'
        }
        changed {
            echo 'This will run only if the state of the Pipeline has changed'
            echo 'For example, if the Pipeline was previously failing but is now successful'
        }
    }
}