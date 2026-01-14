# Jenkins UI Guide: Step-by-Step Pipeline Job Creation

## 🎯 Complete Step-by-Step Guide

Follow these exact steps to create and run your first Jenkins pipeline job.

---

## STEP 1: Open Jenkins in Browser

### Action:
Open your web browser and navigate to:
```
http://localhost:8080
```

### What You'll See:
- Jenkins login page with username and password fields

### Screenshot Guide:
```
┌─────────────────────────────────────────┐
│         Jenkins Login Page              │
│                                          │
│  Username: [________________]           │
│  Password: [________________]           │
│                                          │
│            [ Sign In ]                   │
└─────────────────────────────────────────┘
```

---

## STEP 2: Login to Jenkins

### Action:
Enter credentials:
- **Username**: `admin`
- **Password**: `admin123`

Click **"Sign In"** button

### What You'll See:
- Jenkins dashboard (main page)
- Menu on the left side
- Welcome message or "Create New Jobs" area

### If You See Setup Wizard:
- Click **"Skip and continue as admin"** or **"Start using Jenkins"**
- If asked to install plugins, click **"Install suggested plugins"** (optional)

---

## STEP 3: Navigate to Create New Job

### Action:
Click on **"New Item"** in the left sidebar menu

### Left Sidebar Menu:
```
┌─────────────────┐
│ ☰ Dashboard     │
│ ➕ New Item     │  ← Click Here
│ 👤 People       │
│ 📊 Build History│
│ ⚙️ Manage Jenkins│
└─────────────────┘
```

### What You'll See:
- Page titled "Enter an item name"
- Empty text field for job name
- List of job types below

---

## STEP 4: Enter Job Name and Select Type

### Action:
1. In the text field at the top, enter:
   ```
   pytest-demo-job
   ```

2. Scroll down and click on **"Pipeline"** (icon looks like connected nodes)

3. Click **"OK"** button at the bottom

### Job Types You'll See:
```
┌─────────────────────────────────────────────┐
│ Enter an item name                          │
│ [pytest-demo-job___________________]        │
│                                              │
│ ○ Freestyle project                         │
│ ○ Pipeline                    ← SELECT THIS │
│ ○ Multi-configuration project              │
│ ○ Folder                                    │
│ ○ Multibranch Pipeline                      │
│                                              │
│                                    [ OK ]    │
└─────────────────────────────────────────────┘
```

---

## STEP 5: Configure General Settings (Optional)

### Action:
You'll now see the job configuration page with multiple tabs/sections.

**Optional Settings:**
- **Description**: Enter a description like:
  ```
  Automated pytest job with parameters from Jenkins and JSON config
  ```

- **Discard old builds**: Check this box if you want
  - Days to keep builds: `30`
  - Max # of builds to keep: `10`

**You can skip these and go directly to Pipeline section**

### Configuration Page Sections:
```
┌─────────────────────────────────────────┐
│ Configuration for pytest-demo-job       │
├─────────────────────────────────────────┤
│ ☐ Discard old builds                    │
│ ☐ GitHub project                        │
│ ☐ This project is parameterized         │
│ ☐ Throttle builds                       │
│                                          │
│ ... (scroll down for more options)      │
└─────────────────────────────────────────┘
```

---

## STEP 6: Scroll to Pipeline Section

### Action:
Scroll down to the **"Pipeline"** section (usually at the bottom)

You'll see:
- **Definition** dropdown
- **Script** or **SCM** options

### Pipeline Section Look:
```
┌─────────────────────────────────────────────┐
│ Pipeline                                     │
├─────────────────────────────────────────────┤
│ Definition: [Pipeline script from SCM ▼]    │
│                                              │
│ SCM: [Git ▼]                                │
│                                              │
│ Repository URL: [___________________]        │
│                                              │
│ Script Path: [___________________]           │
└─────────────────────────────────────────────┘
```

---

## STEP 7: Configure Pipeline Definition

### Action:
1. Click on **"Definition"** dropdown
2. Select **"Pipeline script from SCM"**

### Why This Option?
- Your Jenkinsfile is in your project directory
- Jenkins will read it from the file system
- Easier to maintain and version control

---

## STEP 8: Select SCM Type

### Action:
1. Under **"SCM"**, select **"Git"** from dropdown

### What You'll See:
New fields appear:
- Repository URL
- Credentials (can leave as "none")
- Branches to build
- Script Path

---

## STEP 9: Enter Repository URL

### Action:
In the **"Repository URL"** field, enter:
```
file:///workspace
```

### Important:
- Use exactly `file:///workspace` (three slashes!)
- This points to the mounted directory in the container
- No credentials needed for local file system

### Repository Configuration:
```
┌─────────────────────────────────────────────┐
│ SCM: [Git ▼]                                │
│                                              │
│ Repository URL:                              │
│ [file:///workspace________________]         │
│                                              │
│ Credentials: [- none - ▼]                  │
│                                              │
│ Branches to build                           │
│ Branch Specifier: [*/main__]               │
└─────────────────────────────────────────────┘
```

---

## STEP 10: Configure Branch (If Needed)

### Action:
Under **"Branches to build"** section:

**Option A** (if you have a git repo):
- Leave as `*/main` or change to `*/master` if that's your branch

**Option B** (if NOT a git repo - you'll see an error):
- Change to `*/*` (matches any branch)
- This is more forgiving for non-git directories

### Branch Specifier Field:
```
Branch Specifier (blank for 'any'):
[*/*___________________________]
```

---

## STEP 11: Set Script Path

### Action:
In the **"Script Path"** field, enter:
```
Jenkinsfile
```

### What This Does:
- Tells Jenkins to look for a file named "Jenkinsfile" in the repository root
- This file contains your pipeline definition
- It's already created in your project!

### Script Path Configuration:
```
┌─────────────────────────────────────────────┐
│ Script Path:                                 │
│ [Jenkinsfile_____________________]          │
│                                              │
│ ☐ Lightweight checkout                      │
└─────────────────────────────────────────────┘
```

---

## STEP 12: Save the Job

### Action:
1. Scroll to the bottom of the page
2. Click the **"Save"** button (blue button)

### Buttons You'll See:
```
[ Apply ]  [ Save ]  [ Cancel ]
            ↑
         Click Here
```

### What Happens:
- Configuration is saved
- You're redirected to the job page
- You'll see the job menu on the left

---

## STEP 13: Review Job Page

### What You'll See:
The job page with left sidebar menu:

```
┌──────────────────────────────────┐
│ pytest-demo-job                  │
├──────────────────────────────────┤
│ ← Back to Dashboard             │
│                                  │
│ 🔨 Build with Parameters        │ ← Will use this!
│ ⚙️ Configure                     │
│ 📊 Status                        │
│ 📈 Changes                       │
│ 🏗️ Build Now                    │ (if no params)
│ 📂 Workspace                     │
│ 🗑️ Delete Pipeline              │
└──────────────────────────────────┘
```

### Important:
- Since your Jenkinsfile has `parameters` section, you'll see **"Build with Parameters"**
- If you see **"Build Now"** instead, the parameters aren't loaded yet (first build will load them)

---

## STEP 14: Build with Parameters (First Time)

### Action:
Click **"Build with Parameters"** in the left sidebar

### If You See "Build Now" Instead:
1. Click **"Build Now"** once
2. Wait for it to complete (or fail - that's OK!)
3. Refresh the page
4. Now you should see **"Build with Parameters"**

### Why?
Jenkins needs to parse the Jenkinsfile once to discover the parameters.

---

## STEP 15: Configure Build Parameters

### What You'll See:
A form with all the parameters from your Jenkinsfile:

```
┌─────────────────────────────────────────────┐
│ Build with Parameters                        │
├─────────────────────────────────────────────┤
│ TEST_ENVIRONMENT                            │
│ [staging ▼]                                 │
│ Options: staging, dev, production           │
│                                              │
│ TEST_SUITE                                  │
│ [all ▼]                                     │
│ Options: all, smoke, unit, regression       │
│                                              │
│ VERBOSE_OUTPUT                              │
│ ☑ Enable verbose test output               │
│                                              │
│ GENERATE_HTML_REPORT                        │
│ ☑ Generate HTML test report                │
│                                              │
│ CUSTOM_PYTEST_ARGS                          │
│ [________________________________]          │
│                                              │
│                      [ Build ]              │
└─────────────────────────────────────────────┘
```

---

## STEP 16: Select Your Parameters

### Recommended First Run:
Configure these parameters:

1. **TEST_ENVIRONMENT**: Select `staging`
2. **TEST_SUITE**: Select `smoke`
3. **VERBOSE_OUTPUT**: ✓ Checked
4. **GENERATE_HTML_REPORT**: ✓ Checked
5. **CUSTOM_PYTEST_ARGS**: Leave empty

### Why These Settings?
- `staging`: Safe environment to test
- `smoke`: Quick tests (finishes fast)
- `verbose`: See detailed output
- `HTML report`: Get nice visual report

---

## STEP 17: Start the Build

### Action:
Click the **"Build"** button at the bottom

### What Happens:
1. You're taken back to the job page
2. A new build appears in **"Build History"** (left sidebar)
3. You'll see a progress indicator (blue ball or animation)

### Build History Look:
```
┌──────────────────────┐
│ Build History        │
├──────────────────────┤
│ #1 ⚪ (blinking)     │ ← Your build
│                      │
│ [Timeline View]      │
└──────────────────────┘
```

### Build Status Colors:
- 🔵 Blue (blinking) = Building in progress
- ✅ Blue (solid) = Success
- ❌ Red = Failed
- ⚪ Gray = Not built / Aborted
- 🟡 Yellow = Unstable

---

## STEP 18: View Build Console Output

### Action:
1. Click on the build number (e.g., **"#1"**)
2. On the build page, click **"Console Output"** in the left menu

### Alternative (Faster):
- Hover over the build number in Build History
- Click the small console icon that appears

### Console Output Menu:
```
┌──────────────────────────────────┐
│ Build #1                          │
├──────────────────────────────────┤
│ ← Back to Project                │
│                                  │
│ 📊 Status                        │
│ 🗒️ Changes                       │
│ 📝 Console Output               │ ← Click Here
│ ⚙️ Parameters                    │
│ 🔄 Restart                       │
│ 🗑️ Delete                        │
└──────────────────────────────────┘
```

---

## STEP 19: Watch Console Output

### What You'll See:
Live console output showing:

```
Started by user admin
Running in Durability level: MAX_SURVIVABILITY
[Pipeline] Start of Pipeline
[Pipeline] node
[Pipeline] {
[Pipeline] stage
[Pipeline] { (Declarative: Checkout SCM)
[Pipeline] checkout
...

[Pipeline] stage
[Pipeline] { (Show Parameters)
=== Build Parameters ===
Environment: staging
Test Suite: smoke
Verbose Output: true
...
=======================

[Pipeline] stage
[Pipeline] { (Run Tests)
Running smoke tests...
============================= test session starts ==============================
platform linux -- Python 3.13.5
collected 9 items

tests/test_sample.py::test_basic_addition PASSED                    [ 11%]
tests/test_sample.py::test_basic_subtraction PASSED                 [ 22%]
...
============================== 9 passed in 0.02s ===============================

[Pipeline] }
[Pipeline] stage
[Pipeline] { (Publish Reports)
Archiving artifacts
...

[Pipeline] End of Pipeline
Finished: SUCCESS
```

### What to Look For:
- ✓ Parameters displayed correctly
- ✓ Tests running and passing
- ✓ Reports being archived
- ✓ "Finished: SUCCESS" at the end

---

## STEP 20: View Build Results

### Action:
Go back to the build page (click **"← Back to Project"** or build number)

### What You'll See:

#### Build Summary:
```
┌─────────────────────────────────────────────┐
│ Build #1                                     │
│ Success  ✓                                  │
│                                              │
│ Duration: 15 sec                             │
│ Started: Jan 14, 2026 7:20 PM               │
│                                              │
│ Parameters:                                  │
│   TEST_ENVIRONMENT: staging                  │
│   TEST_SUITE: smoke                         │
│   VERBOSE_OUTPUT: true                      │
└─────────────────────────────────────────────┘
```

#### Build Artifacts Section:
```
┌─────────────────────────────────────────────┐
│ Build Artifacts                              │
├─────────────────────────────────────────────┤
│ 📄 report.html                              │ ← Click to download
│ 📄 report.json                              │ ← Click to download
└─────────────────────────────────────────────┘
```

---

## STEP 21: Download and View HTML Report

### Action:
1. In the **"Build Artifacts"** section, click **"report.html"**
2. File will download to your computer
3. Open the downloaded file in your browser

### HTML Report Features:
- ✓ Summary of all tests (passed/failed/skipped)
- ✓ Detailed results for each test
- ✓ Duration of each test
- ✓ Environment information
- ✓ Beautiful visual formatting

---

## STEP 22: Run Build with Different Parameters

### Action:
1. Go back to job page (click job name in breadcrumb at top)
2. Click **"Build with Parameters"** again
3. This time, try different settings:

### Example - Test Production:
```
TEST_ENVIRONMENT: production  ← Changed
TEST_SUITE: all              ← Changed
VERBOSE_OUTPUT: ✓
GENERATE_HTML_REPORT: ✓
```

4. Click **"Build"**

### What This Tests:
- Different environment (production vs staging)
- All tests instead of just smoke tests
- See how configuration changes affect test execution

---

## STEP 23: Compare Builds

### Action:
Run a few builds with different parameters and compare:

### Build Comparison:
```
┌────────────────────────────────────────────┐
│ Build History                               │
├────────────────────────────────────────────┤
│ #3 ✓ production, all tests (25 sec)      │
│ #2 ✓ staging, unit tests (12 sec)        │
│ #1 ✓ staging, smoke tests (10 sec)       │
└────────────────────────────────────────────┘
```

### Observations:
- Production tests take longer (15s timeout vs 10s)
- More tests = longer duration
- All builds passing = good!

---

## STEP 24: View Test Output in Console

### Action:
Click on build #1 → Console Output

Look for the integration test output:

```
======================================================================
COMPREHENSIVE JENKINS + JSON CONFIG INTEGRATION TEST
======================================================================

[1] JENKINS BUILD PARAMETERS:
    Environment:    staging (from TEST_ENV)
    Job Name:       pytest-demo-job (from JOB_NAME)
    Build Number:   1 (from BUILD_NUMBER)
    Workspace:      /workspace (from WORKSPACE)
    Jenkins URL:    http://localhost:8080 (from JENKINS_URL)

[2] JSON CONFIG FOR 'STAGING' ENVIRONMENT:
    API URL:        https://staging-api.example.com
    Timeout:        10s
    Retry Count:    5

[3] DATABASE CONFIG FOR 'STAGING':
    Host:           staging-db.example.com
    Port:           5432
    Database Name:  test_db_staging

... (8 sections total) ...

======================================================================
✓ ALL INTEGRATION CHECKS PASSED!
======================================================================
```

### This Shows:
- ✓ Jenkins parameters received correctly
- ✓ JSON config loaded for staging environment
- ✓ All integrations working

---

## 🎉 SUCCESS! You've Created Your First Jenkins Pipeline Job!

### What You've Accomplished:
✅ Created a parameterized pipeline job
✅ Configured it to use Jenkinsfile from filesystem
✅ Ran tests with different parameters
✅ Viewed console output and test results
✅ Downloaded HTML reports
✅ Saw Jenkins + JSON config integration working

---

## 🚀 Next Steps (Optional Advanced Topics)

### 1. Create More Jobs Using Groovy Seed Job

**Follow these steps:**
1. Dashboard → New Item
2. Name: `seed-job`
3. Type: Pipeline
4. Pipeline section:
   - Definition: `Pipeline script` (not SCM!)
   - Script: Copy contents of `jenkins/seed-job.groovy`
5. Save
6. Click "Build Now"
7. Three new jobs will be created automatically!

### 2. Schedule Automatic Builds

1. Go to job → Configure
2. Find "Build Triggers" section
3. Check "Build periodically"
4. Schedule syntax (cron format):
   ```
   H 2 * * *        # Run daily at 2 AM
   H/15 * * * *     # Run every 15 minutes
   0 9 * * 1-5      # Run at 9 AM on weekdays
   ```

### 3. Set Up Email Notifications

1. Manage Jenkins → Configure System
2. Find "Extended E-mail Notification"
3. Configure SMTP server
4. In your job → Configure → Post-build Actions
5. Add "Editable Email Notification"

### 4. Add GitHub Integration

1. Install GitHub plugin (if not already)
2. Configure → General → Check "GitHub project"
3. Build Triggers → Check "GitHub hook trigger"
4. Set up webhook in GitHub repository

### 5. View Pipeline Stage View

1. Install "Pipeline Stage View Plugin" (if not installed)
2. On job page, you'll see visual pipeline stages
3. Click on stages to see detailed logs

---

## 🐛 Troubleshooting Common Issues

### Issue 1: Can't See "Build with Parameters"
**Problem**: Only see "Build Now"
**Solution**:
1. Click "Build Now" once
2. Wait for build to complete
3. Refresh page - should see "Build with Parameters"

### Issue 2: Git Repository Error
**Problem**: "Couldn't find any revision to build"
**Solution**:
1. Change branch specifier to `*/*`
2. Or initialize git repo: `git init && git add . && git commit -m "init"`

### Issue 3: Tests Not Found
**Problem**: "No tests collected"
**Solution**:
1. Check workspace is mounted: `docker exec jenkins-pytest ls /workspace/tests`
2. Verify Jenkinsfile uses correct path: `tests/`

### Issue 4: Config File Not Found
**Problem**: "Config file not found at config/test_config.json"
**Solution**:
1. Check file exists: `ls config/test_config.json`
2. Verify path in Jenkinsfile: `--test-config-file=config/test_config.json`

### Issue 5: Permission Denied
**Problem**: Cannot read/write files
**Solution**:
```bash
# Fix ownership
sudo chown -R $(whoami) .
```

### Issue 6: Port 8080 Already in Use
**Problem**: Cannot access Jenkins
**Solution**:
```bash
# Find what's using port 8080
lsof -i :8080

# Change port in docker-compose.yml
# Change "8080:8080" to "8081:8080"
# Then access at http://localhost:8081
```

---

## 📚 Quick Reference: Jenkins UI Navigation

### Main Dashboard:
- **New Item**: Create new job
- **People**: View users
- **Build History**: All recent builds
- **Manage Jenkins**: System configuration

### Job Page:
- **Build with Parameters**: Start parameterized build
- **Build Now**: Start simple build
- **Configure**: Edit job settings
- **Workspace**: View job files
- **Status**: View current status

### Build Page:
- **Console Output**: View logs
- **Changes**: See what changed
- **Tests**: Test results (if configured)
- **Build Artifacts**: Download generated files

### Keyboard Shortcuts:
- `g + d`: Go to dashboard
- `g + c`: Go to changes
- `?`: Show all shortcuts

---

## 🎓 What You Learned

### Jenkins Concepts:
- ✅ Pipeline as Code (Jenkinsfile)
- ✅ Parameterized builds
- ✅ SCM integration (Git)
- ✅ Build artifacts
- ✅ Console output

### Pipeline Stages:
- ✅ Checkout SCM
- ✅ Show Parameters
- ✅ Setup & Install Dependencies
- ✅ Run Tests
- ✅ Publish Reports

### Best Practices:
- ✅ Use version control for Jenkinsfile
- ✅ Parameterize for flexibility
- ✅ Archive important artifacts
- ✅ Always check console output
- ✅ Start with smoke tests

---

## 🌟 Congratulations!

You now know how to:
1. ✅ Create Jenkins pipeline jobs via UI
2. ✅ Configure SCM and parameters
3. ✅ Run builds with different settings
4. ✅ View results and download reports
5. ✅ Debug using console output
6. ✅ Understand Jenkins + pytest integration

**You're ready to use Jenkins for your pytest automation!** 🚀
