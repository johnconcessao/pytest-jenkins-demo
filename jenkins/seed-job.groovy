/**
 * Jenkins Job DSL Seed Job
 * This Groovy script creates a parameterized Jenkins pipeline job
 * that reads from both Jenkins parameters and JSON config files
 */

pipelineJob('pytest-demo-job') {
    description('Automated Pytest Job with Parameters from Jenkins and JSON Config')

    // Configure parameters
    parameters {
        // Environment selection
        choiceParam('TEST_ENVIRONMENT', ['staging', 'dev', 'production'],
            'Select the test environment')

        // Test suite selection
        choiceParam('TEST_SUITE', ['all', 'smoke', 'unit', 'regression'],
            'Select which test suite to run')

        // Boolean parameters
        booleanParam('VERBOSE_OUTPUT', true,
            'Enable verbose test output (-v flag)')

        booleanParam('GENERATE_HTML_REPORT', true,
            'Generate HTML test report')

        booleanParam('USE_JSON_CONFIG', true,
            'Load additional parameters from config/test_config.json')

        booleanParam('PARALLEL_EXECUTION', false,
            'Run tests in parallel using pytest-xdist')

        // String parameters
        stringParam('PYTEST_WORKERS', '4',
            'Number of parallel workers (if parallel execution enabled)')

        stringParam('MAX_FAILURES', '10',
            'Stop after N failures (0 = no limit)')

        // Text parameter for custom arguments
        textParam('CUSTOM_PYTEST_ARGS', '',
            'Additional pytest arguments (optional)')

        // File parameter placeholder
        stringParam('CONFIG_FILE_PATH', 'config/test_config.json',
            'Path to JSON config file')
    }

    // Pipeline definition
    definition {
        cpsScm {
            scm {
                git {
                    remote {
                        url('file:///workspace')
                    }
                    branch('*/main')
                }
            }
            scriptPath('Jenkinsfile')
        }
    }

    // Build triggers (optional)
    triggers {
        // Poll SCM every 5 minutes (can be customized)
        // scm('H/5 * * * *')
    }

    // Keep only last 10 builds
    logRotator {
        numToKeep(10)
        artifactNumToKeep(10)
    }
}

// Create additional sample jobs
pipelineJob('pytest-smoke-tests') {
    description('Quick smoke test suite - runs frequently')

    parameters {
        choiceParam('TEST_ENVIRONMENT', ['staging', 'dev'],
            'Select the test environment')
        booleanParam('USE_JSON_CONFIG', true,
            'Load parameters from JSON config')
    }

    definition {
        cps {
            script('''
                pipeline {
                    agent any

                    environment {
                        TEST_ENV = "${params.TEST_ENVIRONMENT}"
                        PYTHONPATH = "${WORKSPACE}"
                    }

                    stages {
                        stage('Run Smoke Tests') {
                            steps {
                                script {
                                    def configArg = params.USE_JSON_CONFIG ?
                                        "--test-config-file=config/test_config.json" : ""

                                    sh """
                                        python3 -m pytest -m smoke -v \
                                        --html=smoke-report.html --self-contained-html \
                                        ${configArg} tests/
                                    """
                                }
                            }
                        }
                    }

                    post {
                        always {
                            archiveArtifacts artifacts: '*.html', allowEmptyArchive: true
                        }
                    }
                }
            '''.stripIndent())
            sandbox(true)
        }
    }
}

// Create a job for regression tests
pipelineJob('pytest-regression-tests') {
    description('Full regression test suite - runs nightly')

    parameters {
        choiceParam('TEST_ENVIRONMENT', ['staging', 'production'],
            'Select the test environment')
        booleanParam('GENERATE_COVERAGE', true,
            'Generate code coverage report')
    }

    definition {
        cps {
            script('''
                pipeline {
                    agent any

                    environment {
                        TEST_ENV = "${params.TEST_ENVIRONMENT}"
                        PYTHONPATH = "${WORKSPACE}"
                    }

                    stages {
                        stage('Run Regression Tests') {
                            steps {
                                script {
                                    def coverageArg = params.GENERATE_COVERAGE ?
                                        "--cov=. --cov-report=html --cov-report=term" : ""

                                    sh """
                                        python3 -m pytest -m regression -v \
                                        ${coverageArg} \
                                        --html=regression-report.html --self-contained-html \
                                        --test-config-file=config/test_config.json \
                                        tests/
                                    """
                                }
                            }
                        }
                    }

                    post {
                        always {
                            archiveArtifacts artifacts: '*.html,htmlcov/**', allowEmptyArchive: true
                        }
                    }
                }
            '''.stripIndent())
            sandbox(true)
        }
    }
}

println "Jenkins DSL jobs created successfully!"
