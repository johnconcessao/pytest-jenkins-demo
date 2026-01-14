FROM jenkins/jenkins:lts-jdk17

# Switch to root user to install packages
USER root

# Install Python 3, pip, and other necessary packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Create symbolic links for python and pip (if they don't exist)
RUN ln -sf /usr/bin/python3 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip

# Install Python packages globally (using --break-system-packages for PEP 668)
RUN pip3 install --no-cache-dir --break-system-packages \
    pytest \
    pytest-html \
    pytest-json-report \
    pytest-cov \
    requests

# Switch back to jenkins user
USER jenkins

# Install Jenkins plugins
RUN jenkins-plugin-cli --plugins \
    git \
    workflow-aggregator \
    docker-workflow \
    pipeline-stage-view \
    blueocean \
    junit \
    htmlpublisher \
    configuration-as-code \
    job-dsl \
    ansicolor

# Skip initial setup wizard
ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false"

# Expose ports
EXPOSE 8080 50000
