# Jenkins Workspace Configuration Guide

## Overview

This guide explains how the Jenkins pipeline uses the **mounted workspace** at `/workspace` to run pytest tests with your project files.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Host Machine (macOS)                                    │
│  /Users/johnpradeepconcessao/CODE_BASE/pytest-jenkins-demo │
│                                                           │
│  ├── tests/                                              │
│  ├── config/                                             │
│  ├── Jenkinsfile                                         │
│  └── docker-compose.yml                                  │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ Volume Mount (./:/workspace)
                     ↓
┌─────────────────────────────────────────────────────────┐
│  Docker Container (jenkins-pytest)                       │
│  /workspace                                              │
│                                                           │
│  ├── tests/          ← Your test files                  │
│  ├── config/         ← JSON config files                │
│  ├── Jenkinsfile     ← Pipeline definition              │
│  └── test-results/   ← Generated reports (created)      │
└─────────────────────────────────────────────────────────┘
```

## Volume Mount Configuration

### docker-compose.yml
```yaml
volumes:
  - jenkins_home:/var/jenkins_home     # Jenkins data
  - ./:/workspace                       # YOUR PROJECT FILES
```

**What this means:**
- Your entire project directory is available inside the container at `/workspace`
- Changes you make on your Mac are instantly visible inside Jenkins
- Test results generated inside Jenkins are saved to your Mac

## Jenkinsfile Configuration

### Key Environment Variables

```groovy
environment {
    PYTHONPATH = "/workspace"           # Python can find your modules
    TEST_ENV = "${params.TEST_ENVIRONMENT}"  # From Jenkins parameter
    WORKSPACE_DIR = "/workspace"        # Explicit workspace location
}
```

### Test Execution

The Jenkinsfile runs tests from the mounted workspace:

```groovy
cd /workspace
python3 -m pytest \
  --test-config-file=/workspace/config/test_config.json \
  --html=/workspace/test-results/report.html \
  --json-report-file=/workspace/test-results/report.json \
  /workspace/tests/
```

**Key Paths:**
- Tests: `/workspace/tests/`
- Config: `/workspace/config/test_config.json`
- Reports: `/workspace/test-results/`

## Jenkins Job Configuration

### Option 1: Using Local Workspace (Current Setup)

```
┌──────────────────────────────────────────────────┐
│ Pipeline                                          │
├──────────────────────────────────────────────────┤
│ Definition: [Pipeline script from SCM ▼]         │
│                                                   │
│ SCM: [Git ▼]                                     │
│                                                   │
│ Repository URL:                                  │
│ [file:///workspace___________________________]   │
│                                                   │
│ Credentials: [- none - ▼]                       │
│                                                   │
│ Branch Specifier: [*/*______________]           │
│                                                   │
│ Script Path: [Jenkinsfile___________]           │
└──────────────────────────────────────────────────┘
```

**Advantages:**
- ✅ No need to commit/push for testing
- ✅ Instant feedback on changes
- ✅ Perfect for development
- ✅ Works offline

### Option 2: Using GitHub (Production)

```
┌──────────────────────────────────────────────────────────────┐
│ Pipeline                                                      │
├──────────────────────────────────────────────────────────────┤
│ Definition: [Pipeline script from SCM ▼]                     │
│                                                               │
│ SCM: [Git ▼]                                                 │
│                                                               │
│ Repository URL:                                              │
│ [https://github.com/johnconcessao/pytest-jenkins-demo.git] │
│                                                               │
│ Credentials: [- none - ▼]                                   │
│                                                               │
│ Branch Specifier: [*/main______________]                    │
│                                                               │
│ Script Path: [Jenkinsfile___________]                       │
└──────────────────────────────────────────────────────────────┘
```

**Advantages:**
- ✅ Version controlled
- ✅ Team collaboration
- ✅ Webhook support (auto-builds)
- ✅ Production ready

## Test Results Location

After running tests, results are saved in:

### Inside Container
```
/workspace/test-results/
├── report.html      # HTML test report
└── report.json      # JSON test results
```

### On Your Mac
```
/Users/johnpradeepconcessao/CODE_BASE/pytest-jenkins-demo/test-results/
├── report.html      # Same HTML report
└── report.json      # Same JSON results
```

**View reports:**
```bash
# Open HTML report in browser
open test-results/report.html

# View JSON results
cat test-results/report.json | python3 -m json.tool
```

## Build Parameters

When you click **"Build with Parameters"** in Jenkins:

### TEST_ENVIRONMENT
- **Default:** `staging`
- **Options:** `dev`, `staging`, `production`
- **Effect:** Sets `TEST_ENV` environment variable
- **Usage:** Loads corresponding config from `config/test_config.json`

### TEST_SUITE
- **Default:** `all`
- **Options:** `all`, `smoke`, `regression`, `unit`
- **Effect:** Filters tests by pytest marker
- **Usage:** `pytest -m smoke` or `pytest -m regression`

### VERBOSE_OUTPUT
- **Default:** `true`
- **Effect:** Adds `-v -s` flags to pytest
- **Usage:** Shows detailed test output

### GENERATE_HTML_REPORT
- **Default:** `true`
- **Effect:** Creates `/workspace/test-results/report.html`
- **Usage:** Visual test results

### CUSTOM_PYTEST_ARGS
- **Default:** *(empty)*
- **Example:** `--maxfail=1 -x`
- **Usage:** Additional pytest arguments

## Pipeline Stages

### 1. Show Parameters
Shows all build parameters and environment info
```
=== Build Parameters ===
Environment: staging
Test Suite: smoke
...
=== Environment Info ===
Jenkins Workspace: /var/jenkins_home/workspace/pytest-demo-job
Mounted Workspace: /workspace
PYTHONPATH: /workspace
```

### 2. Verify Workspace
Checks that mounted files are accessible
```
Workspace contents:
drwxr-xr-x  tests/
drwxr-xr-x  config/
-rw-r--r--  Jenkinsfile
```

### 3. Setup
Verifies Python and pytest are available
```
Python 3.11.2
pip 23.0.1
pytest 7.4.3
```

### 4. Run Tests
Executes pytest with your parameters
```
cd /workspace
python3 -m pytest -m smoke -v -s \
  --test-config-file=/workspace/config/test_config.json \
  /workspace/tests/
```

### 5. Publish Reports
Archives test results for download
```
HTML report archived: test-results/report.html
JSON report archived: test-results/report.json
```

## Development Workflow

### Quick Iteration (Local Workspace)

1. **Edit tests** on your Mac:
   ```bash
   vim tests/test_real_api.py
   ```

2. **Run in Jenkins** (no commit needed):
   - Open http://localhost:8080
   - Click "Build with Parameters"
   - Select options
   - Click "Build"

3. **View results** on your Mac:
   ```bash
   open test-results/report.html
   ```

### Production Deployment (GitHub)

1. **Commit changes:**
   ```bash
   git add .
   git commit -m "Add new test"
   git push origin main
   ```

2. **Jenkins auto-builds** (if webhook configured)
   - Or manually trigger build
   - Uses code from GitHub

3. **View results** in Jenkins UI

## Troubleshooting

### Problem: Tests not found

**Error:**
```
ERROR: file or directory not found: /workspace/tests/
```

**Solution:**
```bash
# Check volume mount is correct
docker exec -it jenkins-pytest ls -la /workspace/

# Should show your project files
```

### Problem: Config file not found

**Error:**
```
FileNotFoundError: config/test_config.json
```

**Solution:**
```bash
# Check file exists in container
docker exec -it jenkins-pytest cat /workspace/config/test_config.json

# Check path in Jenkinsfile is absolute
--test-config-file=/workspace/config/test_config.json
```

### Problem: Reports not generated

**Error:**
```
No test report found
```

**Solution:**
```bash
# Check test-results directory
ls -la test-results/

# If doesn't exist, create it
mkdir -p test-results

# Rebuild container if needed
docker-compose down
docker-compose up -d
```

### Problem: Permission denied

**Error:**
```
PermissionError: [Errno 13] Permission denied: '/workspace/test-results/'
```

**Solution:**
```bash
# Fix permissions on Mac
chmod -R 777 test-results/

# Or run in Jenkinsfile:
sh 'mkdir -p /workspace/test-results && chmod 777 /workspace/test-results'
```

## Best Practices

### 1. Use Local Workspace for Development
```
Repository URL: file:///workspace
```
- Fast iteration
- No git commits needed
- Instant feedback

### 2. Use GitHub for Production
```
Repository URL: https://github.com/johnconcessao/pytest-jenkins-demo.git
```
- Version control
- Team collaboration
- Audit trail

### 3. Keep Test Results Gitignored
```gitignore
test-results/
*.html
*.json
```
- Don't commit generated reports
- Keep repo clean

### 4. Use Environment-Specific Configs
```json
{
  "environments": {
    "dev": { "timeout": 5 },
    "staging": { "timeout": 10 },
    "production": { "timeout": 15 }
  }
}
```

### 5. Monitor Test Duration
```groovy
echo "Duration: ${reportJson.duration}s"
```
- Track performance
- Identify slow tests

## Quick Reference

### Start Jenkins
```bash
cd /Users/johnpradeepconcessao/CODE_BASE/pytest-jenkins-demo
docker-compose up -d
```

### View Logs
```bash
docker logs -f jenkins-pytest
```

### Access Jenkins UI
```
http://localhost:8080
Username: admin
Password: admin123
```

### Run Tests Manually (in container)
```bash
docker exec -it jenkins-pytest bash
cd /workspace
pytest -v tests/
```

### View Test Results
```bash
# On Mac
open test-results/report.html

# Or via HTTP (if served)
http://localhost:8080/job/pytest-demo-job/lastBuild/artifact/test-results/report.html
```

### Stop Jenkins
```bash
docker-compose down
```

## Summary

✅ **Mounted Workspace:** `/workspace` contains your project files
✅ **Jenkinsfile Updated:** Uses absolute paths to `/workspace`
✅ **Test Results:** Saved to `/workspace/test-results/`
✅ **Two Options:** Local workspace (dev) or GitHub (production)
✅ **Instant Sync:** Changes on Mac visible in container
✅ **No Commits Needed:** For local development workflow

You're all set! 🚀
