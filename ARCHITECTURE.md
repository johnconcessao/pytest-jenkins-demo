# Architecture & Flow

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         macOS Host                               │
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │                    Colima (Docker Runtime)              │    │
│  │                                                          │    │
│  │  ┌──────────────────────────────────────────────────┐  │    │
│  │  │          Jenkins Container (jenkins-pytest)      │  │    │
│  │  │                                                   │  │    │
│  │  │  ┌─────────────────┐  ┌──────────────────────┐  │  │    │
│  │  │  │  Jenkins Server │  │   Python 3 + Pytest  │  │  │    │
│  │  │  │  (Port 8080)    │  │   - pytest           │  │  │    │
│  │  │  │                 │  │   - pytest-html      │  │  │    │
│  │  │  │  - Web UI       │  │   - pytest-json      │  │  │    │
│  │  │  │  - Pipeline     │  │   - pytest-cov       │  │  │    │
│  │  │  │  - Groovy DSL   │  │                      │  │  │    │
│  │  │  └─────────────────┘  └──────────────────────┘  │  │    │
│  │  │                                                   │  │    │
│  │  │  Volume Mounts:                                  │  │    │
│  │  │  /var/jenkins_home → jenkins_home (persistent)  │  │    │
│  │  │  /workspace → ./project (shared)                │  │    │
│  │  └──────────────────────────────────────────────────┘  │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              Project Directory (Mounted)               │    │
│  │                                                          │    │
│  │  - config/test_config.json                             │    │
│  │  - tests/*.py                                           │    │
│  │  - Jenkinsfile                                          │    │
│  │  - jenkins/seed-job.groovy                             │    │
│  └────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Parameter Flow: Jenkins → Tests

```
┌──────────────────┐
│  Jenkins Web UI  │
│  Build with      │
│  Parameters      │
└────────┬─────────┘
         │
         │ User Selects:
         │ - TEST_ENVIRONMENT: staging
         │ - TEST_SUITE: smoke
         │ - VERBOSE_OUTPUT: true
         │ - USE_JSON_CONFIG: true
         │
         ▼
┌──────────────────────────┐
│  Jenkinsfile Pipeline    │
│  (Groovy Script)         │
│                          │
│  parameters {            │
│    params.TEST_ENV...    │
│  }                       │
│                          │
│  environment {           │
│    TEST_ENV = "${params. │
│      TEST_ENVIRONMENT}"  │
│  }                       │
└────────┬─────────────────┘
         │
         │ Sets Environment Variables:
         │ - TEST_ENV=staging
         │ - PYTHONPATH=/workspace
         │
         ▼
┌──────────────────────────────┐
│  Shell Command               │
│                              │
│  python3 -m pytest           │
│    -m smoke                  │
│    -v                        │
│    --config-file=config/...  │
│    tests/                    │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  Pytest (conftest.py)            │
│                                  │
│  1. Reads env vars (TEST_ENV)    │
│  2. Loads test_config.json       │
│  3. Merges configurations        │
│  4. Creates fixtures with config │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  Test Functions                  │
│                                  │
│  def test_example(config):       │
│    env = config['environment']   │
│    url = config['api_url']       │
│    build = config['build_number']│
└──────────────────────────────────┘
```

### 2. Configuration Loading Priority

```
Priority (Highest to Lowest):

1. ┌───────────────────────────┐
   │  CLI Arguments            │  --env=production
   │  (pytest command line)    │  --config-file=...
   └─────────┬─────────────────┘
             │ Overrides
             ▼
2. ┌───────────────────────────┐
   │  Environment Variables    │  TEST_ENV=staging
   │  (Set by Jenkins)         │  BUILD_NUMBER=42
   └─────────┬─────────────────┘
             │ Overrides
             ▼
3. ┌───────────────────────────┐
   │  JSON Config File         │  config/test_config.json
   │  (test_config.json)       │  - environments
   └─────────┬─────────────────┘  - test_data
             │ Overrides           - feature_flags
             ▼
4. ┌───────────────────────────┐
   │  Default Values           │  timeout=10
   │  (Hardcoded in code)      │  retry_count=3
   └───────────────────────────┘
```

## Workflow Diagram

### Complete Test Execution Flow

```
                    START
                      │
                      ▼
        ┌─────────────────────────┐
        │  User Opens Jenkins UI  │
        │  http://localhost:8080  │
        └───────────┬─────────────┘
                    │
                    ▼
        ┌─────────────────────────┐
        │  Select Job             │
        │  - pytest-demo-job      │
        │  - pytest-smoke-tests   │
        │  - pytest-regression... │
        └───────────┬─────────────┘
                    │
                    ▼
        ┌─────────────────────────┐
        │  "Build with Parameters"│
        │                         │
        │  Set:                   │
        │  ☑ TEST_ENVIRONMENT     │
        │  ☑ TEST_SUITE           │
        │  ☑ VERBOSE_OUTPUT       │
        │  ☑ GENERATE_HTML_REPORT │
        │  ☑ USE_JSON_CONFIG      │
        └───────────┬─────────────┘
                    │
                    ▼
        ┌─────────────────────────┐
        │  Jenkins Pipeline       │
        │  Executes Jenkinsfile   │
        └───────────┬─────────────┘
                    │
                    ├──► Stage 1: Show Parameters
                    │    └─ Print all build params
                    │
                    ├──► Stage 2: Setup
                    │    └─ Check Python version
                    │
                    ├──► Stage 3: Install Dependencies
                    │    └─ pip install pytest...
                    │
                    ├──► Stage 4: Run Tests
                    │    │
                    │    ├─► Build pytest command
                    │    │   - Add markers (-m smoke)
                    │    │   - Add verbosity (-v)
                    │    │   - Add config file path
                    │    │   - Add report options
                    │    │
                    │    ├─► Execute: python3 -m pytest
                    │    │
                    │    └─► Pytest Process:
                    │        │
                    │        ├─► conftest.py loads
                    │        │   - Read --config-file arg
                    │        │   - Read TEST_ENV var
                    │        │   - Load JSON config
                    │        │   - Merge configs
                    │        │   - Create fixtures
                    │        │
                    │        ├─► Test Discovery
                    │        │   - Find test_*.py files
                    │        │   - Filter by markers
                    │        │   - Collect tests
                    │        │
                    │        ├─► Test Execution
                    │        │   - Run each test
                    │        │   - Inject fixtures
                    │        │   - Capture results
                    │        │
                    │        └─► Generate Reports
                    │            - HTML report
                    │            - JSON report
                    │
                    ├──► Stage 5: Publish Reports
                    │    └─ Archive artifacts
                    │       - report.html
                    │       - report.json
                    │
                    ▼
        ┌─────────────────────────┐
        │  Post Actions           │
        │  - Display summary      │
        │  - Send notifications   │
        │  - Update status        │
        └───────────┬─────────────┘
                    │
                    ▼
                   END
```

## Configuration Merge Example

### Input Sources

**1. Jenkins Parameters:**
```groovy
TEST_ENVIRONMENT = "staging"
TEST_SUITE = "smoke"
VERBOSE_OUTPUT = true
```

**2. JSON Config (config/test_config.json):**
```json
{
  "environments": {
    "staging": {
      "api_url": "https://staging-api.example.com",
      "timeout": 10,
      "retry_count": 5,
      "database": {
        "host": "staging-db.example.com",
        "port": 5432
      }
    }
  },
  "test_data": {
    "users": [...]
  }
}
```

**3. Environment Variables (set by Jenkins):**
```bash
TEST_ENV=staging
BUILD_NUMBER=42
JOB_NAME=pytest-demo-job
WORKSPACE=/workspace
```

### Output: Final Config Object

```python
config = {
    # From CLI/env (highest priority)
    'environment': 'staging',  # From TEST_ENV

    # From JSON config for staging environment
    'api_url': 'https://staging-api.example.com',
    'timeout': 10,
    'retry_count': 5,
    'database': {
        'host': 'staging-db.example.com',
        'port': 5432,
        'name': 'test_db_staging'
    },

    # From JSON config (global)
    'test_data': {
        'users': [...],
        ...
    },

    # From Jenkins environment variables
    'build_number': '42',
    'job_name': 'pytest-demo-job',
    'workspace': '/workspace',
    'jenkins_url': 'http://localhost:8080',

    # Computed/derived
    'verbose': True  # From VERBOSE_OUTPUT param
}
```

## Test Execution Example

### Test File: tests/test_with_config.py

```python
@pytest.mark.smoke
def test_api_call(config, api_config):
    """
    This test receives merged configuration
    """
    # Access environment from Jenkins parameter
    env = config['environment']  # 'staging'

    # Access API URL from JSON config
    url = api_config['url']  # 'https://staging-api.example.com'

    # Access Jenkins build info
    build = config['build_number']  # '42'

    # Access timeouts from JSON config
    timeout = api_config['timeout']  # 10

    print(f"Testing {url} in {env} (Build #{build})")
    print(f"Timeout: {timeout}s")

    # Your test logic here...
    assert True
```

### Execution in Jenkins

```
Console Output:
===============

[CONFIG] Loaded configuration from: config/test_config.json
[CONFIG] Using environment: staging
[CONFIG] Final configuration loaded successfully

====================================================================
                    PYTEST TEST SESSION
====================================================================
Environment:      staging
API URL:          https://staging-api.example.com
Timeout:          10s
Retry Count:      5
Jenkins Job:      pytest-demo-job
Build Number:     42
Workspace:        /workspace
====================================================================

tests/test_with_config.py::test_api_call
============================================================
Test: test_api_call
Environment: staging
Build: pytest-demo-job #42
============================================================
Testing https://staging-api.example.com in staging (Build #42)
Timeout: 10s
PASSED
```

## File Responsibilities

| File | Purpose |
|------|---------|
| [docker-compose.yml](docker-compose.yml) | Defines Jenkins container, ports, volumes |
| [Dockerfile](Dockerfile) | Jenkins image with Python and pytest pre-installed |
| [Jenkinsfile](Jenkinsfile) | Pipeline definition, stages, parameter handling |
| [jenkins/seed-job.groovy](jenkins/seed-job.groovy) | Groovy DSL to create jobs programmatically |
| [config/test_config.json](config/test_config.json) | Environment configs, test data, feature flags |
| [tests/conftest.py](tests/conftest.py) | Config loading, fixtures, pytest setup |
| [tests/test_*.py](tests/) | Actual test cases using config fixtures |
| [pytest.ini](pytest.ini) | Pytest configuration, markers, options |
| [requirements.txt](requirements.txt) | Python dependencies |
| [setup-jenkins.sh](setup-jenkins.sh) | Automated setup script |

---

This architecture provides a flexible, scalable way to run parameterized tests in Jenkins with configuration management!
