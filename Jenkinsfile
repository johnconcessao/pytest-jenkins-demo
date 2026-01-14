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
        PYTHONPATH = "/workspace"
        TEST_ENV = "${params.TEST_ENVIRONMENT}"
        WORKSPACE_DIR = "/workspace"
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
                    echo ""
                    echo "=== Environment Info ==="
                    echo "Jenkins Workspace: ${WORKSPACE}"
                    echo "Mounted Workspace: /workspace"
                    echo "PYTHONPATH: ${PYTHONPATH}"
                    echo "TEST_ENV: ${TEST_ENV}"
                    echo "Build Number: ${BUILD_NUMBER}"
                    echo "Job Name: ${JOB_NAME}"
                    echo "======================="
                }
            }
        }

        stage('Verify Workspace') {
            steps {
                echo 'Verifying mounted workspace...'
                sh '''
                    echo "Current directory: $(pwd)"
                    echo "Workspace contents:"
                    ls -la /workspace/
                    echo ""
                    echo "Test directory:"
                    ls -la /workspace/tests/ || echo "Tests directory not found!"
                    echo ""
                    echo "Config directory:"
                    ls -la /workspace/config/ || echo "Config directory not found!"
                '''
            }
        }

        stage('Setup') {
            steps {
                echo 'Setting up test environment...'
                sh '''
                    python3 --version
                    pip3 --version
                    pytest --version
                '''
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    echo "Running ${params.TEST_SUITE} tests from mounted workspace..."

                    // Change to workspace directory and run tests
                    def pytestCmd = '''
                        cd /workspace
                        python3 -m pytest'''

                    // Add test suite marker if not 'all'
                    if (params.TEST_SUITE != 'all') {
                        pytestCmd += " -m ${params.TEST_SUITE}"
                    }

                    // Add verbose flag and show output
                    if (params.VERBOSE_OUTPUT) {
                        pytestCmd += ' -v -s'
                    }

                    // Add test config file
                    pytestCmd += ' --test-config-file=/workspace/config/test_config.json'

                    // Add HTML report
                    if (params.GENERATE_HTML_REPORT) {
                        pytestCmd += ' --html=/workspace/test-results/report.html --self-contained-html'
                    }

                    // Add JSON report for Jenkins parsing
                    pytestCmd += ' --json-report --json-report-file=/workspace/test-results/report.json'

                    // Add custom arguments if provided
                    if (params.CUSTOM_PYTEST_ARGS?.trim()) {
                        pytestCmd += " ${params.CUSTOM_PYTEST_ARGS}"
                    }

                    // Add test directory
                    pytestCmd += ' /workspace/tests/'

                    echo "Executing: ${pytestCmd}"

                    // Create test-results directory
                    sh 'mkdir -p /workspace/test-results'

                    // Run pytest (continue even if tests fail to publish reports)
                    sh(script: pytestCmd, returnStatus: true)
                }
            }
        }

        stage('Publish Reports') {
            steps {
                echo 'Publishing test reports...'

                script {
                    // List test results directory
                    sh 'ls -la /workspace/test-results/ || echo "No test results directory"'

                    // Archive HTML report if generated
                    if (params.GENERATE_HTML_REPORT && fileExists('/workspace/test-results/report.html')) {
                        archiveArtifacts artifacts: 'test-results/report.html', fingerprint: true
                        echo 'HTML report archived: test-results/report.html'
                    }

                    // Archive JSON report
                    if (fileExists('/workspace/test-results/report.json')) {
                        archiveArtifacts artifacts: 'test-results/report.json', fingerprint: true
                        echo 'JSON report archived: test-results/report.json'
                    }

                    // Also archive any pytest cache or logs
                    sh '''
                        if [ -d /workspace/.pytest_cache ]; then
                            echo "Pytest cache exists"
                        fi
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed!'

            script {
                // Read and display summary from JSON report
                if (fileExists('/workspace/test-results/report.json')) {
                    def reportJson = readJSON file: '/workspace/test-results/report.json'
                    def summary = reportJson.summary

                    echo """
                    ╔════════════════════════════════════════╗
                    ║         TEST SUMMARY REPORT            ║
                    ╠════════════════════════════════════════╣
                    ║  Total Tests:    ${summary.total ?: 0}
                    ║  Passed:         ${summary.passed ?: 0}
                    ║  Failed:         ${summary.failed ?: 0}
                    ║  Skipped:        ${summary.skipped ?: 0}
                    ║  Duration:       ${reportJson.duration ?: 0}s
                    ╠════════════════════════════════════════╣
                    ║  Environment:    ${params.TEST_ENVIRONMENT}
                    ║  Test Suite:     ${params.TEST_SUITE}
                    ║  Build:          #${BUILD_NUMBER}
                    ╚════════════════════════════════════════╝
                    """

                    // Show report location
                    echo ""
                    echo "📊 View detailed report: /workspace/test-results/report.html"
                    echo "📁 Test results saved in: /workspace/test-results/"
                } else {
                    echo "⚠️  No test report found at /workspace/test-results/report.json"
                }
            }
        }

        success {
            echo '✅ Pipeline completed successfully!'
        }

        failure {
            echo '❌ Pipeline failed - check logs above'
        }
    }
}
