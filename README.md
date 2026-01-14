# Jenkins Pytest Demo with Colima Docker

Complete setup for running Jenkins in Docker on macOS using Colima, with parameterized Groovy scripts, JSON configuration, and pytest integration.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Jenkins Setup](#jenkins-setup)
- [Running Tests](#running-tests)
- [Jenkins Parameters](#jenkins-parameters)
- [Groovy Scripts](#groovy-scripts)
- [Troubleshooting](#troubleshooting)

## 🔧 Prerequisites

- macOS (Intel or Apple Silicon)
- Homebrew installed
- 4GB+ free RAM
- 20GB+ free disk space

## 🚀 Quick Start

### 1. Automated Setup

Run the automated setup script:

```bash
./setup-jenkins.sh
```

This script will:
- Install Colima and Docker CLI (if not present)
- Start Colima with appropriate resources
- Build and start Jenkins in Docker
- Display access credentials

### 2. Manual Setup

If you prefer manual setup:

```bash
# Install dependencies
brew install colima docker docker-compose

# Start Colima
colima start --cpu 2 --memory 4 --disk 20

# Build and start Jenkins
docker-compose up -d

# View logs
docker-compose logs -f
```

### 3. Access Jenkins

Open your browser to: **http://localhost:8080**

**Default Credentials:**
- Username: `admin`
- Password: `admin123` (or retrieve with: `docker exec jenkins-pytest cat /var/jenkins_home/secrets/initialAdminPassword`)

## 📁 Project Structure

```
pytest-jenkins-demo/
├── config/
│   └── test_config.json          # JSON configuration for tests
├── jenkins/
│   └── seed-job.groovy           # Groovy DSL for creating jobs
├── tests/
│   ├── conftest.py               # Pytest fixtures and config loader
│   ├── test_sample.py            # Sample tests with markers
│   └── test_with_config.py       # Tests using JSON config
├── docker-compose.yml            # Docker Compose configuration
├── Dockerfile                    # Jenkins with Python
├── Jenkinsfile                   # Pipeline definition
├── requirements.txt              # Python dependencies
├── pytest.ini                    # Pytest configuration
├── setup-jenkins.sh              # Automated setup script
└── README.md                     # This file
```

## ⚙️ Configuration

### JSON Configuration File

The [config/test_config.json](config/test_config.json) file contains environment-specific settings:

```json
{
  "environments": {
    "dev": {
      "api_url": "https://dev-api.example.com",
      "timeout": 5,
      "retry_count": 3,
      "database": { ... }
    },
    "staging": { ... },
    "production": { ... }
  },
  "test_data": { ... },
  "feature_flags": { ... },
  "test_thresholds": { ... }
}
```

### Pytest Configuration

The tests automatically load configuration from:
1. **Jenkins Build Parameters** (highest priority)
2. **JSON Config File** (medium priority)
3. **Default Values** (fallback)

## 🔨 Jenkins Setup

### Method 1: Create Pipeline Job Manually

1. Go to Jenkins: http://localhost:8080
2. Click "New Item"
3. Enter name: `pytest-demo`
4. Select "Pipeline"
5. Under "Pipeline" section:
   - Definition: "Pipeline script from SCM"
   - SCM: "Git"
   - Repository URL: `file:///workspace`
   - Script Path: `Jenkinsfile`
6. Click "Save"

### Method 2: Use Groovy Seed Job

1. Create a new "Pipeline" job named `seed-job`
2. In the Pipeline script section, paste contents of [jenkins/seed-job.groovy](jenkins/seed-job.groovy)
3. Run the job - it will create multiple pre-configured jobs:
   - `pytest-demo-job` - Full parameterized test suite
   - `pytest-smoke-tests` - Quick smoke tests
   - `pytest-regression-tests` - Full regression suite

## 🧪 Running Tests

### Locally (without Jenkins)

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/

# Run with specific marker
pytest -m smoke tests/

# Run with JSON config
pytest --config-file=config/test_config.json tests/

# Run with environment override
pytest --env=production tests/

# Set environment variable
TEST_ENV=staging pytest tests/

# Generate HTML report
pytest --html=report.html --self-contained-html tests/

# Run with coverage
pytest --cov=. --cov-report=html tests/
```

### In Jenkins

1. Navigate to your pipeline job
2. Click "Build with Parameters"
3. Configure parameters:
   - **TEST_ENVIRONMENT**: Select environment (dev/staging/production)
   - **TEST_SUITE**: Select test suite (all/smoke/unit/regression)
   - **VERBOSE_OUTPUT**: Enable verbose output
   - **GENERATE_HTML_REPORT**: Generate HTML report
   - **USE_JSON_CONFIG**: Load from JSON config
4. Click "Build"
5. View results in the build page
6. Download reports from "Build Artifacts"

## 📊 Jenkins Parameters

### Available Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `TEST_ENVIRONMENT` | Choice | Environment to test (dev/staging/production) | staging |
| `TEST_SUITE` | Choice | Test suite to run (all/smoke/unit/regression) | all |
| `VERBOSE_OUTPUT` | Boolean | Enable verbose pytest output | true |
| `GENERATE_HTML_REPORT` | Boolean | Generate HTML test report | true |
| `USE_JSON_CONFIG` | Boolean | Load config from JSON file | true |
| `PARALLEL_EXECUTION` | Boolean | Run tests in parallel | false |
| `PYTEST_WORKERS` | String | Number of parallel workers | 4 |
| `MAX_FAILURES` | String | Stop after N failures | 10 |
| `CUSTOM_PYTEST_ARGS` | Text | Additional pytest arguments | - |
| `CONFIG_FILE_PATH` | String | Path to JSON config | config/test_config.json |

### How Parameters Work

**Jenkins Build Parameters → Environment Variables:**
```groovy
environment {
    TEST_ENV = "${params.TEST_ENVIRONMENT}"
    PYTHONPATH = "${WORKSPACE}"
}
```

**Tests Access Parameters:**
```python
# Via environment variable
env = os.environ.get('TEST_ENV', 'staging')

# Via pytest fixture
def test_example(config):
    print(f"Environment: {config['environment']}")
    print(f"Build: {config['build_number']}")
```

## 🔧 Groovy Scripts

### Seed Job DSL

The [jenkins/seed-job.groovy](jenkins/seed-job.groovy) creates parameterized pipeline jobs:

```groovy
pipelineJob('pytest-demo-job') {
    parameters {
        choiceParam('TEST_ENVIRONMENT', ['staging', 'dev', 'production'])
        choiceParam('TEST_SUITE', ['all', 'smoke', 'unit', 'regression'])
        booleanParam('VERBOSE_OUTPUT', true)
        // ... more parameters
    }

    definition {
        cpsScm {
            scm {
                git {
                    remote { url('file:///workspace') }
                    branch('*/main')
                }
            }
            scriptPath('Jenkinsfile')
        }
    }
}
```

### Jenkinsfile Pipeline

The [Jenkinsfile](Jenkinsfile) defines the build pipeline:

```groovy
pipeline {
    agent any

    parameters { /* ... */ }

    stages {
        stage('Show Parameters') { /* ... */ }
        stage('Install Dependencies') { /* ... */ }
        stage('Run Tests') {
            steps {
                script {
                    def pytestCmd = 'python3 -m pytest'

                    if (params.TEST_SUITE != 'all') {
                        pytestCmd += " -m ${params.TEST_SUITE}"
                    }

                    if (params.VERBOSE_OUTPUT) {
                        pytestCmd += ' -v'
                    }

                    sh pytestCmd
                }
            }
        }
        stage('Publish Reports') { /* ... */ }
    }
}
```

## 🧪 Test Examples

### Using Config Fixture

```python
@pytest.mark.smoke
def test_with_config(config):
    """Test using configuration from JSON and Jenkins"""
    print(f"Environment: {config['environment']}")
    print(f"API URL: {config['api_url']}")
    print(f"Build Number: {config['build_number']}")
    assert config['timeout'] > 0
```

### Using Environment Fixture

```python
@pytest.mark.unit
def test_environment(environment):
    """Test current environment"""
    assert environment in ['dev', 'staging', 'production']
```

### Using API Config

```python
@pytest.mark.regression
def test_api_call(api_config):
    """Test with API configuration"""
    url = api_config['url']
    timeout = api_config['timeout']
    # Make API call with config
```

## 🔍 Useful Commands

### Docker & Colima

```bash
# Check Colima status
colima status

# View Jenkins logs
docker-compose logs -f jenkins

# Restart Jenkins
docker-compose restart

# Stop everything
docker-compose down
colima stop

# Start fresh
colima delete
./setup-jenkins.sh
```

### Jenkins CLI

```bash
# Access Jenkins container
docker exec -it jenkins-pytest bash

# View Jenkins logs inside container
docker exec jenkins-pytest tail -f /var/jenkins_home/logs/jenkins.log

# Check Python version
docker exec jenkins-pytest python3 --version

# Run pytest in container
docker exec jenkins-pytest pytest /workspace/tests/
```

## 🐛 Troubleshooting

### Issue: Jenkins not accessible

```bash
# Check if container is running
docker ps

# Check logs
docker-compose logs jenkins

# Restart
docker-compose restart
```

### Issue: Colima won't start

```bash
# Stop and delete Colima
colima stop
colima delete

# Start fresh with more resources
colima start --cpu 4 --memory 8 --disk 30
```

### Issue: Tests fail to find config

```bash
# Ensure config file exists
ls -la config/test_config.json

# Run with explicit path
pytest --config-file=config/test_config.json tests/
```

### Issue: Permission denied

```bash
# Make scripts executable
chmod +x setup-jenkins.sh

# Fix file permissions
sudo chown -R $(whoami) .
```

### Issue: Port 8080 already in use

```bash
# Find process using port 8080
lsof -i :8080

# Kill the process or change Jenkins port in docker-compose.yml
# Change "8080:8080" to "8081:8080"
```

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Jenkins Pipeline](https://www.jenkins.io/doc/book/pipeline/)
- [Jenkins Job DSL](https://plugins.jenkins.io/job-dsl/)
- [Colima Documentation](https://github.com/abiosoft/colima)
- [Docker Compose](https://docs.docker.com/compose/)

## 🎯 Next Steps

1. ✅ Customize [config/test_config.json](config/test_config.json) for your environments
2. ✅ Add more tests in the `tests/` directory
3. ✅ Modify [Jenkinsfile](Jenkinsfile) for your CI/CD needs
4. ✅ Create additional Groovy scripts in `jenkins/` directory
5. ✅ Set up webhooks for automatic builds
6. ✅ Configure email notifications in Jenkins
7. ✅ Add more pytest markers for test categorization

## 📝 License

MIT License - Feel free to use this setup for your projects!

---

**Happy Testing! 🚀**
