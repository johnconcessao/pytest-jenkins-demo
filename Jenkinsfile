pipeline {
    agent any

    parameters {
        // String parameter
        string(
            name: 'TEST_ENVIRONMENT',
            defaultValue: 'staging',
            description: 'Environment to run tests (staging/production/dev)'
        )

        // Choice parameter
        choice(
            name: 'TEST_SUITE',
            choices: ['all', 'smoke', 'regression', 'unit'],
            description: 'Select test suite to run'
        )

        // Boolean parameter
        booleanParam(
            name: 'VERBOSE_OUTPUT',
            defaultValue: true,
            description: 'Enable verbose test output'
        )

        // Multi-line text parameter
        text(
            name: 'CUSTOM_PYTEST_ARGS',
            defaultValue: '',
            description: 'Additional pytest arguments (optional)'
        )

        // File parameter
        booleanParam(
            name: 'GENERATE_HTML_REPORT',
            defaultValue: true,
            description: 'Generate HTML test report'
        )
    }

    environment {
        // Set environment variables
        PYTHONPATH = "${WORKSPACE}"
        TEST_ENV = "${params.TEST_ENVIRONMENT}"
    }

    stages {
        stage('Show Parameters') {
            steps {
                script {
                    echo "=== Build Parameters ==="
                    echo "Environment: ${params.TEST_ENVIRONMENT}"
                    echo "Test Suite: ${params.TEST_SUITE}"
                    echo "Verbose Output: ${params.VERBOSE_OUTPUT}"
                    echo "Generate HTML Report: ${params.GENERATE_HTML_REPORT}"
                    echo "Custom Args: ${params.CUSTOM_PYTEST_ARGS}"
                    echo "======================="
                }
            }
        }

        stage('Setup') {
            steps {
                echo 'Setting up test environment...'
                sh '''
                    python3 --version
                    pip3 --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                sh '''
                    pip3 install --user pytest pytest-html pytest-json-report
                '''
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    echo "Running ${params.TEST_SUITE} tests..."

                    // Build pytest command based on parameters
                    def pytestCmd = 'python3 -m pytest'

                    // Add test suite marker if not 'all'
                    if (params.TEST_SUITE != 'all') {
                        pytestCmd += " -m ${params.TEST_SUITE}"
                    }

                    // Add verbose flag
                    if (params.VERBOSE_OUTPUT) {
                        pytestCmd += ' -v'
                    }

                    // Add HTML report
                    if (params.GENERATE_HTML_REPORT) {
                        pytestCmd += ' --html=report.html --self-contained-html'
                    }

                    // Add JSON report for Jenkins parsing
                    pytestCmd += ' --json-report --json-report-file=report.json'

                    // Add custom arguments if provided
                    if (params.CUSTOM_PYTEST_ARGS?.trim()) {
                        pytestCmd += " ${params.CUSTOM_PYTEST_ARGS}"
                    }

                    // Add test directory
                    pytestCmd += ' tests/'

                    echo "Executing: ${pytestCmd}"

                    // Run pytest (continue even if tests fail to publish reports)
                    sh(script: pytestCmd, returnStatus: true)
                }
            }
        }

        stage('Publish Reports') {
            steps {
                echo 'Publishing test reports...'

                script {
                    // Archive HTML report if generated
                    if (params.GENERATE_HTML_REPORT && fileExists('report.html')) {
                        archiveArtifacts artifacts: 'report.html', fingerprint: true
                        echo 'HTML report archived'
                    }

                    // Archive JSON report
                    if (fileExists('report.json')) {
                        archiveArtifacts artifacts: 'report.json', fingerprint: true
                        echo 'JSON report archived'
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed!'

            script {
                // Read and display summary from JSON report
                if (fileExists('report.json')) {
                    def reportJson = readJSON file: 'report.json'
                    def summary = reportJson.summary

                    echo """
                    === Test Summary ===
                    Total: ${summary.total}
                    Passed: ${summary.passed ?: 0}
                    Failed: ${summary.failed ?: 0}
                    Skipped: ${summary.skipped ?: 0}
                    ====================
                    """
                }
            }
        }

        success {
            echo 'All tests passed! ✓'
        }

        failure {
            echo 'Some tests failed! ✗'
        }
    }
}
