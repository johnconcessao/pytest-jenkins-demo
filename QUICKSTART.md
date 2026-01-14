# Quick Start Guide

## Setup Jenkins in 5 Minutes

### Step 1: Run Setup Script

```bash
cd /Users/johnpradeepconcessao/CODE_BASE/pytest-jenkins-demo
./setup-jenkins.sh
```

Wait for the script to complete. It will display the Jenkins URL and credentials.

### Step 2: Access Jenkins

Open your browser to: **http://localhost:8080**

Login with:
- Username: `admin`
- Password: `admin123` (or check terminal output)

### Step 3: Create Your First Job

**Option A: Manual Job Creation**

1. Click "New Item"
2. Name: `my-pytest-job`
3. Select "Pipeline"
4. Under Pipeline section:
   - Definition: "Pipeline script from SCM"
   - SCM: "Git"
   - Repository URL: `file:///workspace`
   - Script Path: `Jenkinsfile`
5. Save

**Option B: Use Seed Job (Recommended)**

1. Click "New Item"
2. Name: `seed-job`
3. Select "Pipeline"
4. Under Pipeline section, paste the contents of `jenkins/seed-job.groovy`
5. Save and click "Build Now"
6. This creates 3 pre-configured jobs for you!

### Step 4: Run Tests

1. Go to the job you created
2. Click "Build with Parameters"
3. Select options:
   - **Environment**: staging (or dev/production)
   - **Test Suite**: smoke (or all/unit/regression)
   - **Verbose**: checked
   - **HTML Report**: checked
   - **Use JSON Config**: checked
4. Click "Build"

### Step 5: View Results

- **Console Output**: Click the build number → "Console Output"
- **Test Reports**: Click build number → "Build Artifacts" → Download `report.html`
- **JSON Report**: Download `report.json` for detailed results

## Test Locally First

Before running in Jenkins, test locally:

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run all tests
pytest tests/ -v

# Run smoke tests
pytest -m smoke tests/

# Run with JSON config
pytest --config-file=config/test_config.json tests/

# Set environment
TEST_ENV=production pytest tests/

# Generate HTML report
pytest --html=report.html --self-contained-html tests/
```

## Understanding Parameters

### Jenkins Parameters → Tests

When you set parameters in Jenkins:

1. **TEST_ENVIRONMENT** → Sets `TEST_ENV` environment variable
2. **TEST_SUITE** → Adds `-m <suite>` to pytest command
3. **VERBOSE_OUTPUT** → Adds `-v` flag
4. **GENERATE_HTML_REPORT** → Generates `report.html`

### JSON Config → Tests

The [config/test_config.json](config/test_config.json) provides:

- Environment-specific URLs and timeouts
- Database configurations
- Test data (users, expected values)
- Feature flags
- Test thresholds

Tests access config via fixtures:

```python
def test_example(config, api_config, environment):
    print(f"Environment: {environment}")
    print(f"API URL: {api_config['url']}")
    print(f"Timeout: {api_config['timeout']}")
    print(f"Build: {config['build_number']}")
```

## Customize Configuration

### Edit JSON Config

```bash
vim config/test_config.json
```

Add your own environments, test data, or feature flags:

```json
{
  "environments": {
    "my-env": {
      "api_url": "https://my-api.com",
      "timeout": 10,
      "retry_count": 3
    }
  }
}
```

### Add New Tests

Create a new test file in [tests/](tests/):

```python
# tests/test_my_feature.py
import pytest

@pytest.mark.smoke
def test_my_feature(config):
    """My new test using config"""
    print(f"Testing in: {config['environment']}")
    assert True
```

### Update Jenkinsfile

Edit [Jenkinsfile](Jenkinsfile) to add new stages or modify behavior:

```groovy
stage('My Custom Stage') {
    steps {
        echo 'Running custom commands...'
        sh 'python3 my_script.py'
    }
}
```

## Common Commands

```bash
# View Jenkins logs
docker-compose logs -f

# Restart Jenkins
docker-compose restart

# Stop Jenkins
docker-compose stop

# Start Jenkins
docker-compose start

# Stop everything (including Colima)
docker-compose down
colima stop

# Access Jenkins container
docker exec -it jenkins-pytest bash

# Run tests inside container
docker exec jenkins-pytest pytest /workspace/tests/
```

## Troubleshooting

**Jenkins not loading?**
```bash
docker-compose logs jenkins
```

**Tests failing?**
```bash
# Run locally first
pytest tests/ -v

# Check config file exists
ls -la config/test_config.json
```

**Port 8080 in use?**
```bash
# Change port in docker-compose.yml
# Change "8080:8080" to "8081:8080"
```

**Start fresh?**
```bash
docker-compose down
colima delete
./setup-jenkins.sh
```

## Next Steps

1. ✅ Customize [config/test_config.json](config/test_config.json)
2. ✅ Add your own tests in [tests/](tests/)
3. ✅ Modify [Jenkinsfile](Jenkinsfile) for your needs
4. ✅ Create more jobs using Groovy DSL
5. ✅ Set up webhooks for auto-builds
6. ✅ Configure notifications

## Resources

- Full documentation: [README.md](README.md)
- Jenkins: http://localhost:8080
- Config file: [config/test_config.json](config/test_config.json)
- Pipeline: [Jenkinsfile](Jenkinsfile)
- Groovy scripts: [jenkins/seed-job.groovy](jenkins/seed-job.groovy)

---

**Need help? Check the full [README.md](README.md) for detailed documentation!**
