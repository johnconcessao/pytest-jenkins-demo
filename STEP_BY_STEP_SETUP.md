# Step-by-Step Setup Guide for macOS

## Complete End-to-End Setup and Execution

Follow these steps in order. Each step includes the command to run and what to expect.

---

## Phase 1: Prerequisites Check

### Step 1: Check if Homebrew is installed
```bash
brew --version
```

**Expected Output:** `Homebrew 4.x.x` or similar

**If not installed:**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

---

### Step 2: Install Colima (if not present)
```bash
# Check if Colima is installed
colima version

# If not installed, install it
brew install colima
```

**Expected Output:** `colima version x.x.x` or Colima gets installed

---

### Step 3: Install Docker CLI (if not present)
```bash
# Check if Docker is installed
docker --version

# If not installed, install it
brew install docker docker-compose
```

**Expected Output:** `Docker version xx.x.x` and `docker-compose version x.xx.x`

---

## Phase 2: Start Colima and Docker

### Step 4: Start Colima with appropriate resources
```bash
# Start Colima with 2 CPUs, 4GB RAM, 20GB disk
colima start --cpu 2 --memory 4 --disk 20
```

**Expected Output:**
```
INFO[0000] starting colima
INFO[0000] runtime: docker
INFO[xxxx] creating and starting...
INFO[xxxx] done
```

**This may take 2-3 minutes on first run**

---

### Step 5: Verify Colima is running
```bash
colima status
```

**Expected Output:**
```
INFO[0000] colima is running
```

---

### Step 6: Verify Docker is working
```bash
docker ps
```

**Expected Output:**
```
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```
(Empty list is fine - means Docker is working)

---

## Phase 3: Build and Start Jenkins

### Step 7: Navigate to project directory
```bash
cd /Users/johnpradeepconcessao/CODE_BASE/pytest-jenkins-demo
```

---

### Step 8: Build Jenkins Docker image
```bash
docker-compose build
```

**Expected Output:**
```
[+] Building xxx.xs (x/x) FINISHED
=> [internal] load build definition
=> => transferring dockerfile
...
=> => naming to docker.io/library/pytest-jenkins-demo-jenkins
```

**This will take 3-5 minutes on first build** (downloads Jenkins image and installs Python packages)

---

### Step 9: Start Jenkins container
```bash
docker-compose up -d
```

**Expected Output:**
```
[+] Running 2/2
✔ Network pytest-jenkins-demo_jenkins-network  Created
✔ Container jenkins-pytest                     Started
```

---

### Step 10: Verify Jenkins container is running
```bash
docker ps
```

**Expected Output:**
```
CONTAINER ID   IMAGE                            COMMAND                  CREATED          STATUS          PORTS                                              NAMES
xxxxxxxxxxxx   pytest-jenkins-demo-jenkins      "/usr/bin/tini -- /u…"   X seconds ago    Up X seconds    0.0.0.0:8080->8080/tcp, 0.0.0.0:50000->50000/tcp   jenkins-pytest
```

---

### Step 11: Watch Jenkins startup logs
```bash
docker-compose logs -f jenkins
```

**Wait until you see:**
```
*************************************************************
Jenkins initial setup is required...
*************************************************************

Jenkins is fully up and running
```

**Press Ctrl+C to exit log viewing**

---

### Step 12: Get Jenkins admin password
```bash
docker exec jenkins-pytest cat /var/jenkins_home/secrets/initialAdminPassword 2>/dev/null || echo "Using default: admin123"
```

**Expected Output:** A password string or "Using default: admin123"

**Save this password - you'll need it to login!**

---

## Phase 4: Access and Configure Jenkins

### Step 13: Open Jenkins in browser

**Manual action:** Open your web browser and go to:
```
http://localhost:8080
```

**Expected:** Jenkins login page appears

---

### Step 14: Login to Jenkins

**Manual action in browser:**
- Username: `admin`
- Password: (from Step 12, or `admin123`)

**Expected:** Jenkins dashboard appears

---

### Step 15: Skip initial setup wizard (if it appears)

**Manual action:**
- If you see "Getting Started" wizard, click "Skip" or "Continue"
- If asked to install plugins, select "Install suggested plugins" (optional)

---

## Phase 5: Test Pytest Locally First

### Step 16: Install Python dependencies locally
```bash
pip3 install -r requirements.txt
```

**Expected Output:**
```
Successfully installed pytest-x.x.x pytest-html-x.x.x ...
```

---

### Step 17: Run all tests locally
```bash
pytest tests/ -v
```

**Expected Output:**
```
================================ test session starts =================================
platform darwin -- Python 3.x.x
collected XX items

tests/test_sample.py::test_basic_addition PASSED
tests/test_sample.py::test_basic_subtraction PASSED
...
================================ XX passed in X.XXs ==================================
```

---

### Step 18: Run tests with JSON config
```bash
pytest --config-file=config/test_config.json tests/ -v
```

**Expected Output:**
```
[CONFIG] Loaded configuration from: config/test_config.json
[CONFIG] Using environment: staging
...
PASSED
```

---

### Step 19: Run smoke tests only
```bash
pytest -m smoke tests/ -v
```

**Expected Output:** Only tests marked with `@pytest.mark.smoke` run

---

### Step 20: Run with environment variable
```bash
TEST_ENV=production pytest --config-file=config/test_config.json tests/test_with_config.py -v
```

**Expected Output:**
```
[CONFIG] Using environment: production
...
Environment: production
API URL: https://api.example.com
```

---

### Step 21: Generate HTML report locally
```bash
pytest --html=report.html --self-contained-html tests/
```

**Expected Output:**
```
================================ XX passed in X.XXs ==================================
--- generated html file: file:///path/to/report.html ---
```

**Manual action:** Open `report.html` in browser to view

---

## Phase 6: Create Jenkins Job

### Step 22: Create new Pipeline job

**Manual action in Jenkins:**
1. Click "New Item" (top left)
2. Enter item name: `pytest-demo-job`
3. Select "Pipeline"
4. Click "OK"

---

### Step 23: Configure the job

**Manual action:**
1. Scroll to "Pipeline" section at bottom
2. Definition: Select "Pipeline script from SCM"
3. SCM: Select "Git"
4. Repository URL: Enter `file:///workspace`
5. Branch: Leave as `*/main` or change to `*/master` or `*/*`
6. Script Path: Enter `Jenkinsfile`
7. Click "Save"

---

### Step 24: View job configuration

**Manual action:**
- You should now be on the job page
- Notice the "Build with Parameters" option on left sidebar
- This means the Jenkinsfile parameters are loaded!

---

## Phase 7: Run Tests in Jenkins

### Step 25: Start first build

**Manual action:**
1. Click "Build with Parameters" (left sidebar)
2. You'll see parameter options:
   - **TEST_ENVIRONMENT**: Select `staging`
   - **TEST_SUITE**: Select `smoke`
   - **VERBOSE_OUTPUT**: Check (enable)
   - **GENERATE_HTML_REPORT**: Check (enable)
   - **CUSTOM_PYTEST_ARGS**: Leave empty
3. Click "Build" at bottom

---

### Step 26: Watch build progress

**Manual action:**
1. You'll see a new build appear in "Build History" (left sidebar)
2. Click on the build number (e.g., "#1")
3. Click "Console Output" to watch live logs

**Expected:** You'll see:
```
=== Build Parameters ===
Environment: staging
Test Suite: smoke
...
Running smoke tests...
collected XX items
...
PASSED
```

---

### Step 27: View build results

**Manual action:**
1. Go back to the build page (click build number)
2. Look for "Build Artifacts" section
3. Click on `report.html` to download
4. Open downloaded file in browser

**Expected:** Beautiful HTML test report with results

---

## Phase 8: Create Jobs Using Groovy Seed Job

### Step 28: Create seed job

**Manual action in Jenkins:**
1. Click "Jenkins" (top left) to go to dashboard
2. Click "New Item"
3. Name: `seed-job`
4. Select "Pipeline"
5. Click "OK"

---

### Step 29: Configure seed job with Groovy script

**Manual action:**
1. Scroll to "Pipeline" section
2. Definition: Select "Pipeline script" (not SCM!)
3. In the Script text area, we need to paste the Groovy content

**We'll get the content in next step**

---

### Step 30: Copy Groovy script content
```bash
cat jenkins/seed-job.groovy
```

**Manual action:**
1. Copy the entire output from terminal
2. Paste it into Jenkins Pipeline Script text area
3. Click "Save"

---

### Step 31: Run seed job

**Manual action:**
1. Click "Build Now" (left sidebar)
2. Wait for build to complete (should be quick)
3. Click on build number, then "Console Output"

**Expected Output:**
```
...
Processing DSL script seed-job.groovy
...
Jenkins DSL jobs created successfully!
Finished: SUCCESS
```

---

### Step 32: Verify new jobs were created

**Manual action:**
1. Click "Jenkins" (top left) to go to dashboard
2. You should now see 3 new jobs:
   - `pytest-demo-job`
   - `pytest-smoke-tests`
   - `pytest-regression-tests`

---

## Phase 9: Test Different Scenarios

### Step 33: Run regression tests

**Manual action:**
1. Click on `pytest-regression-tests` job
2. Click "Build with Parameters"
3. Select:
   - **TEST_ENVIRONMENT**: `production`
   - **GENERATE_COVERAGE**: Check
4. Click "Build"
5. View results

---

### Step 34: Run tests with different environment

**Manual action:**
1. Go back to `pytest-demo-job`
2. Click "Build with Parameters"
3. Select:
   - **TEST_ENVIRONMENT**: `dev`
   - **TEST_SUITE**: `unit`
   - **VERBOSE_OUTPUT**: Check
4. Click "Build"
5. Watch console output

**Expected:** Tests run with dev environment configuration from JSON

---

### Step 35: Run all tests

**Manual action:**
1. Click "Build with Parameters"
2. Select:
   - **TEST_ENVIRONMENT**: `staging`
   - **TEST_SUITE**: `all`
3. Click "Build"

**Expected:** All tests from all markers run

---

## Phase 10: Verify Everything Works

### Step 36: Check Docker container is healthy
```bash
docker exec jenkins-pytest python3 --version
docker exec jenkins-pytest pytest --version
```

**Expected Output:**
```
Python 3.x.x
pytest 7.x.x
```

---

### Step 37: Run pytest inside container manually
```bash
docker exec jenkins-pytest pytest /workspace/tests/test_sample.py -v
```

**Expected:** Tests run successfully inside container

---

### Step 38: Check Jenkins logs for errors
```bash
docker-compose logs jenkins | grep -i error
```

**Expected:** No critical errors (some warnings are normal)

---

### Step 39: Verify config file is accessible in container
```bash
docker exec jenkins-pytest cat /workspace/config/test_config.json
```

**Expected:** JSON config content displayed

---

### Step 40: Check volume mount
```bash
docker exec jenkins-pytest ls -la /workspace
```

**Expected:** Your project files listed

---

## Phase 11: Explore and Customize

### Step 41: Edit JSON config for custom environment
```bash
# Open in your editor
open -a TextEdit config/test_config.json

# Or use vim
vim config/test_config.json
```

**Manual action:**
- Add your own environment settings
- Save the file

---

### Step 42: Run tests with your custom config
```bash
TEST_ENV=staging pytest --config-file=config/test_config.json tests/test_with_config.py::test_config_loading -v
```

**Expected:** Test passes using your custom config

---

## Phase 12: Cleanup (Optional)

### Step 43: Stop Jenkins (without removing data)
```bash
docker-compose stop
```

---

### Step 44: Start Jenkins again
```bash
docker-compose start
```

---

### Step 45: Remove everything and start fresh
```bash
# Stop and remove containers
docker-compose down

# Remove volumes (deletes Jenkins data)
docker-compose down -v

# Stop Colima
colima stop

# Delete Colima VM (complete cleanup)
colima delete
```

---

## ✅ Success Checklist

After completing all steps, you should have:

- [ ] Colima installed and running
- [ ] Docker CLI working
- [ ] Jenkins running in container
- [ ] Can access Jenkins at http://localhost:8080
- [ ] Can login to Jenkins
- [ ] Created pipeline job manually
- [ ] Job shows "Build with Parameters" option
- [ ] Successfully ran tests from Jenkins
- [ ] HTML report generated and viewable
- [ ] Created seed job with Groovy script
- [ ] Seed job created 3 additional jobs
- [ ] Tests can read from JSON config file
- [ ] Tests receive Jenkins parameters (environment, build number)
- [ ] Ran tests locally via pytest CLI
- [ ] Ran tests with different environments (dev/staging/production)
- [ ] Ran different test suites (smoke/unit/regression/all)

---

## 🆘 Troubleshooting During Setup

### Issue: Colima won't start
```bash
# Check if VMs are already running
VBoxManage list runningvms

# Delete and retry
colima delete
colima start --cpu 2 --memory 4 --disk 20
```

### Issue: Docker build fails
```bash
# Check Docker is working
docker info

# Restart Colima
colima restart
```

### Issue: Jenkins container won't start
```bash
# Check logs
docker-compose logs jenkins

# Restart
docker-compose restart
```

### Issue: Can't access Jenkins on port 8080
```bash
# Check if port is in use
lsof -i :8080

# Change port in docker-compose.yml to 8081
# Then restart: docker-compose down && docker-compose up -d
```

### Issue: Tests can't find config file
```bash
# Verify file exists
ls -la config/test_config.json

# Check if mounted in container
docker exec jenkins-pytest ls -la /workspace/config/
```

### Issue: Permission errors
```bash
# Fix ownership
sudo chown -R $(whoami) .

# Make scripts executable
chmod +x setup-jenkins.sh
```

---

## 📊 What You've Learned

By completing this guide, you've:

1. ✅ Set up Docker environment on macOS using Colima
2. ✅ Built custom Docker image with Jenkins + Python
3. ✅ Created parameterized Jenkins pipelines
4. ✅ Used Groovy DSL to create jobs programmatically
5. ✅ Passed parameters from Jenkins to pytest tests
6. ✅ Loaded configuration from JSON files in tests
7. ✅ Merged multiple configuration sources
8. ✅ Generated HTML and JSON test reports
9. ✅ Organized tests with pytest markers
10. ✅ Set up complete CI/CD pipeline for Python testing

---

## 🎯 Next Steps

Now that everything is working:

1. Customize `config/test_config.json` for your actual environments
2. Add your own tests in `tests/` directory
3. Modify `Jenkinsfile` to add more stages
4. Create more Groovy jobs for different scenarios
5. Set up webhooks to trigger builds automatically
6. Configure notifications (email, Slack, etc.)
7. Add code coverage thresholds
8. Implement parallel test execution

---

**Congratulations! You've successfully set up and run the complete Jenkins + Pytest + Colima system! 🎉**
