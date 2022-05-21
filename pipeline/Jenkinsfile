pipeline {
    agent any

    stages {
        stage('Run API tests using docker') {
            steps {
                echo 'There will be UI tests run'
                checkout([$class: 'GitSCM', branches: [[name: 'inside_of_docker_container']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/jujga/TestTaskEvo']]])
                bat 'docker build -t pytest_runner .'
                bat 'docker run --rm --mount type=bind,src=' + pwd() + ',target=/tests_project/ pytest_runner'
                //bat(readFile("D:/cmds/do_image_python.cmd"))

                }
            }
        }


    post {
        always {
            script {
                        allure([
                                //allure commandline: 'allure',
                                includeProperties: false,
                                jdk: '',
                                results: [[path: 'test_results']]
                        ])
                    }
                }
        }
}
    // stage('Run REST tests') {
        //     steps {
        //         bat(readFile("C:/Users/jujga/PycharmProjects/TestTaskEvo/run_rest_test.bat"))
        //     }
        // }

        // stage('reports') {
        //     steps {
        //         script {
        //                 allure([
        //                         //allure commandline: 'allure',
        //                         includeProperties: false,
        //                         jdk: '',
        //                         results: [[path: 'test_results']]
        //                 ])
        //             }
        //         }
        //     }

