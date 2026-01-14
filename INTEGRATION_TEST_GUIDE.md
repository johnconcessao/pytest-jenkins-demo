# Integration Test Guide

## Comprehensive Jenkins + JSON Config Integration Test

The test `test_jenkins_and_json_integration` demonstrates how to use both Jenkins build parameters and JSON configuration together.

## What This Test Demonstrates

### 1. Jenkins Build Parameters (Environment Variables)
- `TEST_ENV` - Environment to test (dev/staging/production)
- `BUILD_NUMBER` - Jenkins build number
- `JOB_NAME` - Jenkins job name
- `WORKSPACE` - Jenkins workspace path
- `JENKINS_URL` - Jenkins server URL

### 2. JSON Configuration File
- Environment-specific API URLs
- Timeouts and retry settings
- Database configurations
- Test data (users, expected values)
- Feature flags
- Test thresholds

### 3. Configuration Priority System
```
Highest Priority: CLI Arguments (--env=production)
                 ↓
          Environment Variables (TEST_ENV=staging)
                 ↓
          JSON Config File (config/test_config.json)
                 ↓
Lowest Priority:  Default Values
```

## Running the Test Locally

### Test with Default (Staging)
```bash
pytest tests/test_with_config.py::test_jenkins_and_json_integration -v -s
```

### Test with Dev Environment
```bash
TEST_ENV=dev pytest tests/test_with_config.py::test_jenkins_and_json_integration -v -s
```

### Test with Production Environment
```bash
TEST_ENV=production pytest tests/test_with_config.py::test_jenkins_and_json_integration -v -s
```

### Test All Environments
```bash
# Dev
TEST_ENV=dev pytest tests/test_with_config.py::test_jenkins_and_json_integration -v

# Staging
TEST_ENV=staging pytest tests/test_with_config.py::test_jenkins_and_json_integration -v

# Production
TEST_ENV=production pytest tests/test_with_config.py::test_jenkins_and_json_integration -v
```

## Running in Jenkins

### Via Jenkinsfile
The test will automatically receive Jenkins parameters:

```groovy
environment {
    TEST_ENV = "${params.TEST_ENVIRONMENT}"
    PYTHONPATH = "${WORKSPACE}"
}

stages {
    stage('Run Integration Test') {
        steps {
            sh """
                python3 -m pytest \
                  tests/test_with_config.py::test_jenkins_and_json_integration \
                  --test-config-file=config/test_config.json \
                  -v -s
            """
        }
    }
}
```

### Build Parameters in Jenkins
When you run the job, set these parameters:
- **TEST_ENVIRONMENT**: `production`
- **TEST_SUITE**: `smoke`
- **VERBOSE_OUTPUT**: ✓ (checked)

Jenkins will automatically set:
- `BUILD_NUMBER`: 42 (example)
- `JOB_NAME`: pytest-demo-job
- `WORKSPACE`: /workspace
- `JENKINS_URL`: http://localhost:8080

## Test Output Explained

### Section 1: Jenkins Build Parameters
Shows parameters received from Jenkins:
```
[1] JENKINS BUILD PARAMETERS:
    Environment:    production (from TEST_ENV)
    Job Name:       pytest-demo-job (from JOB_NAME)
    Build Number:   42 (from BUILD_NUMBER)
```

### Section 2: JSON Config for Environment
Shows configuration loaded from JSON for selected environment:
```
[2] JSON CONFIG FOR 'PRODUCTION' ENVIRONMENT:
    API URL:        https://api.example.com
    Timeout:        15s
    Retry Count:    5
```

### Section 3: Database Configuration
Shows environment-specific database settings:
```
[3] DATABASE CONFIG FOR 'PRODUCTION':
    Host:           prod-db.example.com
    Port:           5432
    Database Name:  test_db_prod
```

### Section 4: Test Data
Shows test data loaded from JSON:
```
[4] TEST DATA FROM JSON:
    Test Users:     2 users loaded
      - test_user_1 (admin)
      - test_user_2 (user)
```

### Section 5: Feature Flags
Shows feature flags that can control test behavior:
```
[5] FEATURE FLAGS:
    enable_new_feature: DISABLED
    enable_debug_mode: ENABLED
    enable_caching: ENABLED
```

### Section 6: Test Thresholds
Shows test thresholds for validation:
```
[6] TEST THRESHOLDS:
    min_success_rate: 95
    max_failure_count: 5
    performance_baseline_ms: 500
```

### Section 7: Configuration Priority
Explains where each value came from:
```
[7] CONFIGURATION PRIORITY DEMONSTRATION:
    ✓ Environment came from: TEST_ENV env var (Jenkins)
    ✓ API URL came from: JSON config (environments.production.api_url)
    ✓ Build info came from: Jenkins environment variables
```

### Section 8: Simulated Test Scenario
Shows how the test would use these configurations:
```
[8] SIMULATED API TEST SCENARIO:
    Step 1: Connect to https://api.example.com
    Step 2: Set timeout to 15s
    Step 3: Configure 5 retries
    Step 4: Execute test for Jenkins Job: pytest-demo-job Build #42
```

## Environment-Specific Behavior

### Dev Environment
- **API URL**: `https://dev-api.example.com`
- **Timeout**: 5 seconds (fast)
- **Database**: `dev-db.example.com`
- **Use Case**: Quick smoke tests during development

### Staging Environment
- **API URL**: `https://staging-api.example.com`
- **Timeout**: 10 seconds (moderate)
- **Database**: `staging-db.example.com`
- **Use Case**: Pre-production testing

### Production Environment
- **API URL**: `https://api.example.com`
- **Timeout**: 15 seconds (longer for safety)
- **Database**: `prod-db.example.com`
- **Use Case**: Production validation tests

## Customizing for Your Project

### 1. Update JSON Config
Edit `config/test_config.json` with your actual:
- API endpoints
- Database connections
- Test users
- Feature flags

### 2. Add Custom Assertions
In the test, add your specific validations:
```python
# Example: Validate API is reachable
import requests
response = requests.get(api_config['url'], timeout=api_config['timeout'])
assert response.status_code == 200
```

### 3. Use Feature Flags
Conditionally run tests based on flags:
```python
if config['feature_flags'].get('enable_new_feature'):
    # Test new feature
    test_new_feature_endpoint()
else:
    pytest.skip("New feature not enabled")
```

### 4. Apply Test Thresholds
Use thresholds to validate performance:
```python
import time
start = time.time()
# ... run test ...
duration_ms = (time.time() - start) * 1000

assert duration_ms < config['thresholds']['performance_baseline_ms'], \
    f"Test took {duration_ms}ms, exceeds baseline"
```

## Integration with CI/CD

### Jenkins Pipeline Example
```groovy
pipeline {
    agent any

    parameters {
        choice(name: 'TEST_ENVIRONMENT',
               choices: ['dev', 'staging', 'production'])
    }

    environment {
        TEST_ENV = "${params.TEST_ENVIRONMENT}"
    }

    stages {
        stage('Integration Test') {
            steps {
                sh '''
                    pytest tests/test_with_config.py::test_jenkins_and_json_integration \
                      --test-config-file=config/test_config.json \
                      --html=integration-report.html \
                      --self-contained-html \
                      -v -s
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'integration-report.html'
        }
    }
}
```

## Best Practices

1. **Keep JSON Config Updated**: Ensure environment configs match your actual environments

2. **Use Appropriate Environment**:
   - Dev for quick iterations
   - Staging for pre-release testing
   - Production for validation only

3. **Monitor Test Duration**: Use thresholds to catch performance regressions

4. **Leverage Feature Flags**: Enable/disable tests without code changes

5. **Document Environment Differences**: Keep track of what differs between environments

6. **Version Control Config**: Commit `test_config.json` to git for reproducibility

7. **Secure Sensitive Data**: Don't put passwords in JSON config - use Jenkins credentials

## Troubleshooting

### Config File Not Found
```bash
# Make sure path is correct relative to workspace
pytest --test-config-file=config/test_config.json tests/
```

### Environment Variable Not Set
```bash
# Set explicitly before running
export TEST_ENV=production
pytest tests/
```

### Wrong Environment Used
```bash
# Check what's set
echo $TEST_ENV

# Override with CLI
pytest --env=staging tests/
```

### Test Fails on Assertions
- Check JSON config has all required fields for the environment
- Verify environment name matches (dev/staging/production)
- Ensure timeouts and URLs are correct for environment

## Example Output

When run in Jenkins with BUILD_NUMBER=42, JOB_NAME=pytest-demo-job:

```
COMPREHENSIVE JENKINS + JSON CONFIG INTEGRATION TEST
======================================================================

[1] JENKINS BUILD PARAMETERS:
    Environment:    production (from TEST_ENV)
    Job Name:       pytest-demo-job (from JOB_NAME)
    Build Number:   42 (from BUILD_NUMBER)
    Workspace:      /workspace (from WORKSPACE)
    Jenkins URL:    http://localhost:8080 (from JENKINS_URL)

[2] JSON CONFIG FOR 'PRODUCTION' ENVIRONMENT:
    API URL:        https://api.example.com
    Timeout:        15s
    Retry Count:    5

... (full output with all sections) ...

======================================================================
✓ ALL INTEGRATION CHECKS PASSED!
======================================================================
```

## Summary

This integration test provides:
- ✅ Complete example of Jenkins + JSON config integration
- ✅ Environment-specific configuration management
- ✅ Priority system for configuration sources
- ✅ Comprehensive output for debugging
- ✅ Template for real-world test scenarios
- ✅ Best practices for CI/CD integration

Use this test as a foundation for your own integration tests!
