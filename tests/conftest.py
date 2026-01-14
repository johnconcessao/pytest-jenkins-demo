"""
Pytest configuration and fixtures
Handles loading configuration from JSON files and Jenkins parameters
"""
import os
import json
import pytest
from pathlib import Path


def pytest_addoption(parser):
    """Add custom command line options to pytest"""
    parser.addoption(
        "--test-config-file",
        action="store",
        default="config/test_config.json",
        help="Path to JSON configuration file"
    )
    parser.addoption(
        "--env",
        action="store",
        default=None,
        help="Test environment (overrides TEST_ENV environment variable)"
    )


@pytest.fixture(scope="session")
def config(request):
    """
    Load configuration from JSON file and merge with environment variables
    Priority: CLI args > Jenkins params (env vars) > JSON config
    """
    # Get config file path from pytest option
    config_file = request.config.getoption("--test-config-file")
    config_path = Path(config_file)

    # Initialize config dict
    config_data = {}

    # Load JSON config if file exists
    if config_path.exists():
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        print(f"\n[CONFIG] Loaded configuration from: {config_file}")
    else:
        print(f"\n[CONFIG] Warning: Config file not found at {config_file}")

    # Get environment from CLI option or environment variable
    env = request.config.getoption("--env") or os.environ.get('TEST_ENV', 'staging')

    # Merge environment-specific config
    if 'environments' in config_data and env in config_data['environments']:
        env_config = config_data['environments'][env]
        print(f"[CONFIG] Using environment: {env}")
    else:
        env_config = {}
        print(f"[CONFIG] Environment '{env}' not found in config, using defaults")

    # Build final config with environment variables taking precedence
    final_config = {
        'environment': env,
        'api_url': env_config.get('api_url', 'http://localhost'),
        'timeout': int(os.environ.get('API_TIMEOUT', env_config.get('timeout', 10))),
        'retry_count': int(os.environ.get('RETRY_COUNT', env_config.get('retry_count', 3))),
        'database': env_config.get('database', {}),
        'test_data': config_data.get('test_data', {}),
        'feature_flags': config_data.get('feature_flags', {}),
        'thresholds': config_data.get('test_thresholds', {}),
        # Jenkins build parameters
        'build_number': os.environ.get('BUILD_NUMBER', 'local'),
        'job_name': os.environ.get('JOB_NAME', 'manual-run'),
        'workspace': os.environ.get('WORKSPACE', os.getcwd()),
        'jenkins_url': os.environ.get('JENKINS_URL', 'not-in-jenkins'),
        'verbose': os.environ.get('VERBOSE_OUTPUT', 'true').lower() == 'true',
    }

    print(f"[CONFIG] Final configuration loaded successfully")
    return final_config


@pytest.fixture(scope="session")
def environment(config):
    """Get the current test environment"""
    return config['environment']


@pytest.fixture(scope="session")
def api_config(config):
    """Get API-specific configuration"""
    return {
        'url': config['api_url'],
        'timeout': config['timeout'],
        'retry_count': config['retry_count']
    }


@pytest.fixture(scope="session")
def database_config(config):
    """Get database configuration"""
    return config.get('database', {})


@pytest.fixture(scope="session")
def test_users(config):
    """Get test user data from config"""
    return config.get('test_data', {}).get('users', [])


@pytest.fixture(scope="function")
def print_test_info(request, config):
    """Print test information at the start of each test"""
    print(f"\n{'='*60}")
    print(f"Test: {request.node.name}")
    print(f"Environment: {config['environment']}")
    print(f"Build: {config['job_name']} #{config['build_number']}")
    print(f"{'='*60}")
    yield
    print(f"{'='*60}\n")


@pytest.fixture(scope="session", autouse=True)
def print_session_info(config):
    """Print session information at the start of test session"""
    print("\n" + "="*70)
    print(" "*20 + "PYTEST TEST SESSION")
    print("="*70)
    print(f"Environment:      {config['environment']}")
    print(f"API URL:          {config['api_url']}")
    print(f"Timeout:          {config['timeout']}s")
    print(f"Retry Count:      {config['retry_count']}")
    print(f"Jenkins Job:      {config['job_name']}")
    print(f"Build Number:     {config['build_number']}")
    print(f"Workspace:        {config['workspace']}")
    print(f"Jenkins URL:      {config['jenkins_url']}")
    print("="*70 + "\n")
    yield
    print("\n" + "="*70)
    print(" "*20 + "TEST SESSION COMPLETED")
    print("="*70 + "\n")


@pytest.fixture
def feature_flags(config):
    """Get feature flags from config"""
    return config.get('feature_flags', {})


@pytest.fixture
def test_thresholds(config):
    """Get test thresholds from config"""
    return config.get('thresholds', {})
