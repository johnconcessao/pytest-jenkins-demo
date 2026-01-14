# Jenkins Setup on Mac - Complete Guide

## Prerequisites
- macOS with Homebrew installed
- Java 17 or 21 (Jenkins requirement)

## Step 1: Install Jenkins

### Option A: Using Homebrew (Recommended)
```bash
# Install Jenkins LTS
brew install jenkins-lts

# Start Jenkins as a service
brew services start jenkins-lts

# Jenkins will be available at: http://localhost:8080
```

### Option B: Using Docker
```bash
# Run Jenkins in Docker container
docker run -d -p 8080:8080 -p 50000:50000 \
  --name jenkins \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts
```

## Step 2: Initial Setup

1. **Get Initial Admin Password**
   ```bash
   # For Homebrew installation
   cat /Users/Shared/Jenkins/Home/secrets/initialAdminPassword

   # For Docker installation
   docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
   ```

2. **Access Jenkins**
   - Open browser: http://localhost:8080
   - Enter the initial admin password
   - Install suggested plugins
   - Create your first admin user

## Step 3: Install Required Plugins

Navigate to: **Manage Jenkins → Plugins → Available plugins**

Install these plugins:
- **Pipeline** (for Groovy scripts)
- **Git plugin** (for repository integration)
- **Blue Ocean** (modern UI, optional)
- **ShiningPanda** or **Python Plugin** (for pytest support)

## Step 4: Configure Python/Pytest

1. Go to **Manage Jenkins → Tools**
2. Add Python installation or configure system Python
3. Ensure pytest is installed:
   ```bash
   pip install pytest pytest-html pytest-json-report
   ```

## Step 5: Create Your First Parameterized Pipeline

1. Click **New Item**
2. Enter name: "Pytest-Demo-Pipeline"
3. Select **Pipeline**
4. Click **OK**

## Common Commands

```bash
# Start Jenkins
brew services start jenkins-lts

# Stop Jenkins
brew services stop jenkins-lts

# Restart Jenkins
brew services restart jenkins-lts

# Check Jenkins status
brew services info jenkins-lts

# View Jenkins logs
tail -f /opt/homebrew/var/log/jenkins-lts/jenkins-lts.log
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8080
lsof -ti:8080

# Kill the process
kill -9 $(lsof -ti:8080)
```

### Reset Jenkins
```bash
# Stop Jenkins
brew services stop jenkins-lts

# Backup and remove Jenkins home
mv /Users/Shared/Jenkins/Home /Users/Shared/Jenkins/Home.backup

# Start Jenkins (will create fresh installation)
brew services start jenkins-lts
```

## Next Steps
- See `Jenkinsfile` for sample Groovy pipeline script
- See `JENKINS_PIPELINE_GUIDE.md` for detailed pipeline examples
- Run `pytest` locally first to ensure tests work
