#!/bin/bash

# Verification Script for Jenkins Docker Setup
# This script verifies that Jenkins is running with the workspace properly mounted

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║     Jenkins + Pytest Docker Setup Verification                     ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $2"
    else
        echo -e "${RED}✗${NC} $2"
    fi
}

# 1. Check Docker is running
echo "1. Checking Docker..."
docker --version > /dev/null 2>&1
print_status $? "Docker is installed and running"
echo ""

# 2. Check container is running
echo "2. Checking Jenkins container..."
docker ps --filter name=jenkins-pytest --format "{{.Names}}" | grep -q jenkins-pytest
if [ $? -eq 0 ]; then
    STATUS=$(docker ps --filter name=jenkins-pytest --format "{{.Status}}")
    print_status 0 "Container 'jenkins-pytest' is running ($STATUS)"
else
    print_status 1 "Container 'jenkins-pytest' is NOT running"
    exit 1
fi
echo ""

# 3. Check workspace mount
echo "3. Checking workspace mount..."
docker exec jenkins-pytest ls /workspace > /dev/null 2>&1
print_status $? "Workspace mounted at /workspace"

docker exec jenkins-pytest ls /workspace/tests > /dev/null 2>&1
print_status $? "Tests directory accessible"

docker exec jenkins-pytest ls /workspace/config > /dev/null 2>&1
print_status $? "Config directory accessible"

docker exec jenkins-pytest cat /workspace/Jenkinsfile > /dev/null 2>&1
print_status $? "Jenkinsfile accessible"
echo ""

# 4. Check Python and pytest
echo "4. Checking Python environment..."
PYTHON_VERSION=$(docker exec jenkins-pytest python3 --version 2>&1)
print_status $? "Python installed: $PYTHON_VERSION"

PYTEST_VERSION=$(docker exec jenkins-pytest pytest --version 2>&1 | head -1)
print_status $? "Pytest installed: $PYTEST_VERSION"
echo ""

# 5. Check test collection
echo "5. Checking test discovery..."
TEST_COUNT=$(docker exec jenkins-pytest bash -c "cd /workspace && pytest --collect-only -q 2>&1 | grep 'test collected' | awk '{print \$1}'")
if [ ! -z "$TEST_COUNT" ]; then
    print_status 0 "Collected $TEST_COUNT tests successfully"
else
    print_status 1 "Failed to collect tests"
fi
echo ""

# 6. Check Jenkins is accessible
echo "6. Checking Jenkins web UI..."
curl -s http://localhost:8080 > /dev/null 2>&1
print_status $? "Jenkins UI accessible at http://localhost:8080"
echo ""

# 7. Summary
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                         SETUP SUMMARY                               ║"
echo "╠════════════════════════════════════════════════════════════════════╣"
echo "║  Container:    jenkins-pytest                                       ║"
echo "║  Workspace:    /workspace                                           ║"
echo "║  Tests:        $TEST_COUNT tests                                           ║"
echo "║  Jenkins UI:   http://localhost:8080                                ║"
echo "║  Credentials:  admin / admin123                                     ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

echo "Next Steps:"
echo "  1. Open Jenkins: http://localhost:8080"
echo "  2. Login with: admin / admin123"
echo "  3. Create new Pipeline job"
echo "  4. Configure to use: file:///workspace"
echo "  5. Script Path: Jenkinsfile"
echo ""
echo "Quick Test:"
echo "  docker exec jenkins-pytest bash -c 'cd /workspace && pytest tests/ -v'"
echo ""
