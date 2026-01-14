#!/bin/bash

###############################################################################
# Jenkins Setup Script for macOS with Colima
# This script automates the setup of Jenkins in Docker using Colima
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}==>${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_header() {
    echo -e "\n${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC}  $1"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}\n"
}

# Check if Homebrew is installed
check_homebrew() {
    print_status "Checking for Homebrew..."
    if ! command -v brew &> /dev/null; then
        print_error "Homebrew not found!"
        echo "Please install Homebrew first:"
        echo '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        exit 1
    fi
    print_success "Homebrew is installed"
}

# Install Colima if not present
install_colima() {
    print_status "Checking for Colima..."
    if ! command -v colima &> /dev/null; then
        print_status "Installing Colima..."
        brew install colima
        print_success "Colima installed"
    else
        print_success "Colima is already installed"
    fi
}

# Install Docker CLI if not present
install_docker() {
    print_status "Checking for Docker CLI..."
    if ! command -v docker &> /dev/null; then
        print_status "Installing Docker CLI..."
        brew install docker docker-compose
        print_success "Docker CLI installed"
    else
        print_success "Docker CLI is already installed"
    fi
}

# Start Colima
start_colima() {
    print_status "Checking Colima status..."
    if ! colima status &> /dev/null; then
        print_status "Starting Colima with 4GB RAM and 2 CPUs..."
        colima start --cpu 2 --memory 4 --disk 20
        print_success "Colima started"
    else
        print_success "Colima is already running"
    fi
}

# Build and start Jenkins
build_jenkins() {
    print_status "Building Jenkins Docker image..."
    docker-compose build
    print_success "Jenkins image built"

    print_status "Starting Jenkins container..."
    docker-compose up -d
    print_success "Jenkins container started"
}

# Wait for Jenkins to be ready
wait_for_jenkins() {
    print_status "Waiting for Jenkins to start (this may take 1-2 minutes)..."
    local max_attempts=60
    local attempt=0

    while [ $attempt -lt $max_attempts ]; do
        if curl -s http://localhost:8080 > /dev/null 2>&1; then
            print_success "Jenkins is ready!"
            return 0
        fi
        echo -n "."
        sleep 2
        ((attempt++))
    done

    print_error "Jenkins failed to start within expected time"
    return 1
}

# Get Jenkins initial password
get_jenkins_password() {
    print_status "Retrieving Jenkins initial admin password..."
    if docker exec jenkins-pytest test -f /var/jenkins_home/secrets/initialAdminPassword 2>/dev/null; then
        local password=$(docker exec jenkins-pytest cat /var/jenkins_home/secrets/initialAdminPassword 2>/dev/null || echo "admin123")
        echo -e "\n${GREEN}Jenkins Initial Admin Password:${NC} ${YELLOW}$password${NC}\n"
    else
        echo -e "\n${GREEN}Jenkins Admin Credentials:${NC}"
        echo -e "  Username: ${YELLOW}admin${NC}"
        echo -e "  Password: ${YELLOW}admin123${NC}\n"
    fi
}

# Display access information
show_access_info() {
    print_header "Jenkins Setup Complete!"

    echo -e "${GREEN}Jenkins is now running!${NC}\n"
    echo -e "Access Jenkins at: ${BLUE}http://localhost:8080${NC}\n"

    get_jenkins_password

    echo -e "${YELLOW}Next Steps:${NC}"
    echo -e "1. Open ${BLUE}http://localhost:8080${NC} in your browser"
    echo -e "2. Log in with the credentials above"
    echo -e "3. Create a new Pipeline job or use the seed job:\n"
    echo -e "   ${BLUE}New Item → Pipeline → Name: 'pytest-demo'${NC}"
    echo -e "   ${BLUE}Pipeline Script from SCM → Git${NC}"
    echo -e "   ${BLUE}Repository URL: file:///workspace${NC}"
    echo -e "   ${BLUE}Script Path: Jenkinsfile${NC}\n"

    echo -e "${YELLOW}Useful Commands:${NC}"
    echo -e "  View logs:        ${BLUE}docker-compose logs -f${NC}"
    echo -e "  Stop Jenkins:     ${BLUE}docker-compose stop${NC}"
    echo -e "  Start Jenkins:    ${BLUE}docker-compose start${NC}"
    echo -e "  Restart Jenkins:  ${BLUE}docker-compose restart${NC}"
    echo -e "  Remove Jenkins:   ${BLUE}docker-compose down${NC}"
    echo -e "  Stop Colima:      ${BLUE}colima stop${NC}\n"

    echo -e "${YELLOW}Test Configuration:${NC}"
    echo -e "  Config file:      ${BLUE}config/test_config.json${NC}"
    echo -e "  Tests directory:  ${BLUE}tests/${NC}"
    echo -e "  Groovy seed job:  ${BLUE}jenkins/seed-job.groovy${NC}\n"
}

# Main execution
main() {
    print_header "Jenkins Setup for macOS with Colima"

    check_homebrew
    install_colima
    install_docker
    start_colima
    build_jenkins
    wait_for_jenkins
    show_access_info
}

# Run main function
main
