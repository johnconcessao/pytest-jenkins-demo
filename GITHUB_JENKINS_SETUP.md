# Using GitHub with Jenkins - Complete Guide

## 🎯 Two Ways to Configure Jenkins

You can use **EITHER** local files OR GitHub. Here's how to do both:

---

## 📁 OPTION 1: Local Files (Current Setup)

### Jenkins Configuration:
```
Definition: Pipeline script from SCM
SCM: Git
Repository URL: file:///workspace
Branch Specifier: */*
Script Path: Jenkinsfile
```

### Pros:
✅ No need to push to GitHub
✅ Instant changes (just modify files)
✅ No internet required
✅ Good for development/testing

### Cons:
❌ Changes not version controlled externally
❌ Can't share easily with team
❌ No GitHub webhooks for auto-builds

---

## 🌐 OPTION 2: GitHub Repository (Recommended for Production)

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `pytest-jenkins-demo` (or your choice)
3. Description: "Jenkins + Pytest integration with Docker"
4. **Public** or **Private** (your choice)
5. **Do NOT** initialize with README (we already have one)
6. Click "Create repository"

### Step 2: Push Your Code to GitHub

**You already have git initialized! Just add remote and push:**

```bash
# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/pytest-jenkins-demo.git

# Push to GitHub
git push -u origin main
```

**Example (replace YOUR_USERNAME):**
```bash
git remote add origin https://github.com/johnpradeep/pytest-jenkins-demo.git
git push -u origin main
```

### Step 3: Configure Jenkins to Use GitHub

#### In Jenkins Job Configuration:

**A. Pipeline Section:**
```
Definition: Pipeline script from SCM
SCM: Git
```

**B. Repository URL:**
```
https://github.com/YOUR_USERNAME/pytest-jenkins-demo.git
```

**C. Credentials:**
- If **Public repo**: Select `- none -`
- If **Private repo**: Click "Add" → Create credentials (see below)

**D. Branch Specifier:**
```
*/main
```
(or `*/master` if your default branch is master)

**E. Script Path:**
```
Jenkinsfile
```

### Step 4: Add GitHub Credentials (If Private Repo)

1. In Jenkins, click "Add" next to Credentials
2. Select "Jenkins" as the scope
3. Kind: `Username with password`
4. Username: Your GitHub username
5. Password: **GitHub Personal Access Token** (NOT your GitHub password!)
6. ID: `github-credentials`
7. Description: "GitHub Access"
8. Click "Add"

#### Creating GitHub Personal Access Token:

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token" → "Generate new token (classic)"
3. Note: "Jenkins access"
4. Select scopes:
   - ✓ `repo` (all repo permissions)
5. Click "Generate token"
6. **COPY THE TOKEN** (you won't see it again!)
7. Use this token as the password in Jenkins credentials

---

## 🔄 Comparison: Local vs GitHub

| Feature | Local Files | GitHub |
|---------|-------------|--------|
| Setup Complexity | ⭐ Easy | ⭐⭐ Medium |
| Version Control | Local only | ✅ Full history |
| Team Collaboration | ❌ Limited | ✅ Easy |
| Auto-build on Commit | ❌ No | ✅ Yes (with webhooks) |
| Internet Required | ❌ No | ✅ Yes |
| Best For | Development | Production |

---

## 🚀 RECOMMENDED: Use Both!

### Development Workflow:
1. **Develop locally** with `file:///workspace` (fast iteration)
2. **Test changes** immediately in Jenkins
3. **When satisfied**, commit and push to GitHub
4. **Switch Jenkins** to use GitHub URL
5. **Set up webhooks** for automatic builds

### Commands for This Workflow:

```bash
# Make changes to your tests
vim tests/test_real_api.py

# Test locally
pytest tests/test_real_api.py -v

# Test in Jenkins with local files (no git needed)
# Just click "Build with Parameters" in Jenkins

# When ready, commit and push
git add .
git commit -m "Add new API test"
git push origin main

# Jenkins auto-builds if webhook is set up!
```

---

## 🎯 Current Status

✅ **Git initialized and committed**
```
Commit: 63be302
Files: 20 files, 5049 lines
Branch: main
```

✅ **Ready to push to GitHub**
```bash
# Just run:
git remote add origin https://github.com/YOUR_USERNAME/pytest-jenkins-demo.git
git push -u origin main
```

---

## 📋 Jenkins Configuration Examples

### For Local Files (Current):
```groovy
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Files already available at /workspace
                echo 'Using local files'
            }
        }
    }
}
```

### For GitHub:
```groovy
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Jenkins automatically checks out from GitHub
                echo "Checked out from GitHub: ${env.GIT_URL}"
                echo "Branch: ${env.GIT_BRANCH}"
                echo "Commit: ${env.GIT_COMMIT}"
            }
        }
    }
}
```

---

## 🔔 Setting Up GitHub Webhooks (Auto-Build on Push)

### Step 1: In Jenkins Job Configuration

Check: **"GitHub hook trigger for GITScm polling"**

### Step 2: In GitHub Repository Settings

1. Go to your GitHub repo → Settings → Webhooks
2. Click "Add webhook"
3. Payload URL: `http://YOUR_JENKINS_URL:8080/github-webhook/`
4. Content type: `application/json`
5. Which events: "Just the push event"
6. Click "Add webhook"

**Note:** For local Jenkins (localhost), webhooks won't work unless you:
- Use ngrok or similar tunnel service
- OR deploy Jenkins to a public server
- OR use GitHub Actions instead

---

## 🎨 Recommended Setup for You

### Phase 1: Development (Now)
```
Jenkins: file:///workspace
Benefits: Fast iteration, no git needed
```

### Phase 2: Share & Collaborate (When Ready)
```bash
# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/pytest-jenkins-demo.git
git push -u origin main

# Update Jenkins to use:
Repository URL: https://github.com/YOUR_USERNAME/pytest-jenkins-demo.git
```

### Phase 3: Production (Future)
- Deploy Jenkins to public server
- Set up GitHub webhooks
- Configure branch protection
- Add pull request builds

---

## 🔧 Quick Commands Reference

### Using Local Files:
```bash
# No git commands needed
# Just edit files and run Jenkins builds
```

### Using GitHub:
```bash
# First time setup
git remote add origin https://github.com/YOUR_USERNAME/REPO.git
git push -u origin main

# Daily workflow
git add .
git commit -m "Your changes"
git push

# Update from GitHub
git pull
```

### Switch Between Local and GitHub in Jenkins:
```
Local:  file:///workspace
GitHub: https://github.com/YOUR_USERNAME/pytest-jenkins-demo.git
```

---

## 📝 Current Jenkins Configuration (What You Should Enter)

Since you're just starting, use **Local Files** for now:

```
┌─────────────────────────────────────────────────────────┐
│ Pipeline                                                 │
├─────────────────────────────────────────────────────────┤
│ Definition: [Pipeline script from SCM ▼]                │
│                                                           │
│ SCM: [Git ▼]                                            │
│                                                           │
│ Repository URL:                                          │
│ [file:///workspace_________________]                    │
│                                                           │
│ Credentials: [- none - ▼]                              │
│                                                           │
│ Branch Specifier: [*/*____________]                     │
│                                                           │
│ Script Path: [Jenkinsfile__________]                    │
└─────────────────────────────────────────────────────────┘

Click "Save"
```

**When you're ready to use GitHub**, just come back and change:
- Repository URL to: `https://github.com/YOUR_USERNAME/pytest-jenkins-demo.git`
- Branch Specifier to: `*/main`

---

## ✅ Summary

**Current State:**
- ✅ Git initialized
- ✅ All files committed
- ✅ Ready to push to GitHub
- ✅ Jenkins can use local files NOW

**Next Steps:**

**Option A - Keep it Simple (Recommended for now):**
1. Use `file:///workspace` in Jenkins
2. Start running tests
3. Push to GitHub later when you want to share

**Option B - Use GitHub Now:**
1. Create GitHub repo
2. `git remote add origin https://github.com/YOUR_USERNAME/REPO.git`
3. `git push -u origin main`
4. Update Jenkins to use GitHub URL

**Both work perfectly! Choose based on your needs.** 🚀
