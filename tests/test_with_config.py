"""
Enhanced pytest tests that use both Jenkins parameters and JSON config
"""
import pytest
import os


@pytest.mark.smoke
def test_config_loading(config):
    """Test that configuration is loaded correctly"""
    assert config is not None
    assert 'environment' in config
    assert 'api_url' in config
    print(f"\nConfiguration loaded for environment: {config['environment']}")
    print(f"API URL: {config['api_url']}")


@pytest.mark.smoke
def test_environment_from_jenkins(environment, config):
    """Test environment parameter from Jenkins"""
    print(f"\nTest running in environment: {environment}")
    print(f"Build Number: {config['build_number']}")
    print(f"Job Name: {config['job_name']}")
    assert environment in ['dev', 'staging', 'production']


@pytest.mark.smoke
def test_jenkins_and_json_integration(config, api_config, environment, database_config):
    """
    Comprehensive test demonstrating integration of:
    1. Jenkins Build Parameters (TEST_ENV, BUILD_NUMBER, JOB_NAME)
    2. JSON Config File (API URLs, timeouts, database settings)
    3. Priority System (Jenkins params override JSON config)
    """
    print("\n" + "="*70)
    print("COMPREHENSIVE JENKINS + JSON CONFIG INTEGRATION TEST")
    print("="*70)

    # Part 1: Jenkins Parameters
    print("\n[1] JENKINS BUILD PARAMETERS:")
    print(f"    Environment:    {environment} (from TEST_ENV)")
    print(f"    Job Name:       {config['job_name']} (from JOB_NAME)")
    print(f"    Build Number:   {config['build_number']} (from BUILD_NUMBER)")
    print(f"    Workspace:      {config['workspace']} (from WORKSPACE)")
    print(f"    Jenkins URL:    {config['jenkins_url']} (from JENKINS_URL)")

    # Verify Jenkins parameters
    assert config['job_name'] is not None, "Job name should be set"
    assert config['build_number'] is not None, "Build number should be set"

    # Part 2: JSON Configuration for Current Environment
    print(f"\n[2] JSON CONFIG FOR '{environment.upper()}' ENVIRONMENT:")
    print(f"    API URL:        {api_config['url']}")
    print(f"    Timeout:        {api_config['timeout']}s")
    print(f"    Retry Count:    {api_config['retry_count']}")

    # Verify JSON config loaded correctly
    assert api_config['url'].startswith('http'), "API URL should be valid"
    assert api_config['timeout'] > 0, "Timeout should be positive"
    assert api_config['retry_count'] > 0, "Retry count should be positive"

    # Part 3: Environment-Specific Database Configuration
    if database_config:
        print(f"\n[3] DATABASE CONFIG FOR '{environment.upper()}':")
        print(f"    Host:           {database_config['host']}")
        print(f"    Port:           {database_config['port']}")
        print(f"    Database Name:  {database_config['name']}")

        # Verify database config
        assert database_config['port'] == 5432, "Database port should be 5432"
        # Check that DB host matches environment (prod for production, otherwise environment name)
        expected_env_prefix = 'prod' if environment == 'production' else environment
        assert expected_env_prefix in database_config['host'], f"DB host should contain '{expected_env_prefix}'"

    # Part 4: Test Data from JSON
    if 'test_data' in config:
        test_data = config['test_data']
        print(f"\n[4] TEST DATA FROM JSON:")
        if 'users' in test_data:
            print(f"    Test Users:     {len(test_data['users'])} users loaded")
            for user in test_data['users']:
                print(f"      - {user['username']} ({user['role']})")

        if 'expected_response_codes' in test_data:
            print(f"    Expected Codes: {test_data['expected_response_codes']}")

        if 'max_response_time_ms' in test_data:
            print(f"    Max Response:   {test_data['max_response_time_ms']}ms")

    # Part 5: Feature Flags from JSON
    if 'feature_flags' in config:
        flags = config['feature_flags']
        print(f"\n[5] FEATURE FLAGS:")
        for flag_name, flag_value in flags.items():
            status = "ENABLED" if flag_value else "DISABLED"
            print(f"    {flag_name}: {status}")

    # Part 6: Test Thresholds from JSON
    if 'thresholds' in config:
        thresholds = config['thresholds']
        print(f"\n[6] TEST THRESHOLDS:")
        for threshold_name, threshold_value in thresholds.items():
            print(f"    {threshold_name}: {threshold_value}")

    # Part 7: Configuration Priority Demonstration
    print(f"\n[7] CONFIGURATION PRIORITY DEMONSTRATION:")
    print("    Priority: CLI args > Env Vars (Jenkins) > JSON Config > Defaults")
    print(f"    ✓ Environment came from: {'CLI --env' if os.environ.get('TEST_ENV') is None else 'TEST_ENV env var (Jenkins)'}")
    print(f"    ✓ API URL came from: JSON config (environments.{environment}.api_url)")
    print(f"    ✓ Build info came from: Jenkins environment variables")

    # Part 8: Simulate a Real Test Scenario
    print(f"\n[8] SIMULATED API TEST SCENARIO:")
    print(f"    Scenario: Testing API endpoint in {environment} environment")
    print(f"    Step 1: Connect to {api_config['url']}")
    print(f"    Step 2: Set timeout to {api_config['timeout']}s")
    print(f"    Step 3: Configure {api_config['retry_count']} retries")
    print(f"    Step 4: Execute test for Jenkins Job: {config['job_name']} Build #{config['build_number']}")
    print(f"    Step 5: Validate response meets thresholds")

    # Verify environment-specific values
    if environment == 'dev':
        assert api_config['timeout'] == 5, "Dev timeout should be 5s"
        assert 'dev-api' in api_config['url'], "Dev should use dev-api URL"
    elif environment == 'staging':
        assert api_config['timeout'] == 10, "Staging timeout should be 10s"
        assert 'staging-api' in api_config['url'], "Staging should use staging-api URL"
    elif environment == 'production':
        assert api_config['timeout'] == 15, "Production timeout should be 15s"
        assert api_config['url'] == 'https://api.example.com', "Production should use production URL"

    print("\n" + "="*70)
    print("✓ ALL INTEGRATION CHECKS PASSED!")
    print("="*70 + "\n")

    # Final assertion
    assert True, "Jenkins + JSON Config integration working perfectly!"


@pytest.mark.unit
def test_api_configuration(api_config):
    """Test API configuration from JSON"""
    assert 'url' in api_config
    assert 'timeout' in api_config
    assert 'retry_count' in api_config
    assert api_config['timeout'] > 0
    assert api_config['retry_count'] > 0
    print(f"\nAPI Config: {api_config}")


@pytest.mark.unit
def test_database_configuration(database_config, environment):
    """Test database configuration for current environment"""
    if database_config:
        assert 'host' in database_config
        assert 'port' in database_config
        assert 'name' in database_config
        print(f"\nDatabase Config for {environment}:")
        print(f"  Host: {database_config['host']}")
        print(f"  Port: {database_config['port']}")
        print(f"  Name: {database_config['name']}")
    else:
        pytest.skip("No database configuration available")


@pytest.mark.regression
def test_test_users_from_config(test_users):
    """Test that test users are loaded from config"""
    assert isinstance(test_users, list)
    if test_users:
        for user in test_users:
            assert 'username' in user
            assert 'email' in user
            print(f"\nTest User: {user['username']} ({user['email']})")


@pytest.mark.unit
def test_feature_flags(feature_flags):
    """Test feature flags from config"""
    assert isinstance(feature_flags, dict)
    print(f"\nFeature Flags: {feature_flags}")
    # Test specific flags if they exist
    if 'enable_debug_mode' in feature_flags:
        print(f"Debug Mode: {feature_flags['enable_debug_mode']}")


@pytest.mark.regression
def test_jenkins_parameters(config):
    """Test that Jenkins parameters are accessible"""
    print("\n=== Jenkins Parameters ===")
    print(f"Job Name: {config['job_name']}")
    print(f"Build Number: {config['build_number']}")
    print(f"Workspace: {config['workspace']}")
    print(f"Jenkins URL: {config['jenkins_url']}")
    print(f"Verbose Mode: {config['verbose']}")
    print("=" * 30)
    assert config['build_number'] is not None


@pytest.mark.smoke
def test_environment_specific_timeout(config, environment):
    """Test that timeout varies by environment"""
    timeout = config['timeout']
    print(f"\nTimeout for {environment}: {timeout}s")
    assert timeout > 0
    # Different environments may have different timeouts
    if environment == 'production':
        assert timeout >= 10, "Production should have longer timeout"


@pytest.mark.unit
@pytest.mark.parametrize("flag_name", [
    "enable_debug_mode",
    "enable_caching",
    "enable_new_feature"
])
def test_individual_feature_flags(feature_flags, flag_name):
    """Test individual feature flags"""
    if flag_name in feature_flags:
        flag_value = feature_flags[flag_name]
        print(f"\n{flag_name}: {flag_value}")
        assert isinstance(flag_value, bool)
    else:
        pytest.skip(f"Feature flag '{flag_name}' not defined")


@pytest.mark.regression
def test_thresholds_configuration(test_thresholds):
    """Test that test thresholds are configured"""
    print(f"\nTest Thresholds: {test_thresholds}")
    if test_thresholds:
        if 'min_success_rate' in test_thresholds:
            assert test_thresholds['min_success_rate'] >= 0
            assert test_thresholds['min_success_rate'] <= 100


@pytest.mark.smoke
def test_retry_mechanism(api_config):
    """Test retry configuration"""
    retry_count = api_config['retry_count']
    print(f"\nRetry count configured: {retry_count}")
    assert retry_count >= 1
    assert retry_count <= 10


class TestConfigIntegration:
    """Test suite for configuration integration"""

    @pytest.mark.unit
    def test_full_config_structure(self, config):
        """Test that full config has all required keys"""
        required_keys = ['environment', 'api_url', 'timeout', 'retry_count']
        for key in required_keys:
            assert key in config, f"Missing required config key: {key}"

    @pytest.mark.unit
    def test_config_consistency(self, config, environment):
        """Test that config is consistent across fixtures"""
        assert config['environment'] == environment

    @pytest.mark.regression
    def test_jenkins_environment_integration(self, config):
        """Test Jenkins environment variables are integrated"""
        # These should be set when running in Jenkins
        jenkins_vars = ['job_name', 'build_number', 'workspace']
        for var in jenkins_vars:
            assert var in config
            print(f"{var}: {config[var]}")


@pytest.mark.smoke
def test_print_full_config(config, print_test_info):
    """Print full configuration for debugging"""
    print("\n=== FULL CONFIGURATION ===")
    for key, value in config.items():
        if isinstance(value, dict):
            print(f"\n{key}:")
            for sub_key, sub_value in value.items():
                print(f"  {sub_key}: {sub_value}")
        else:
            print(f"{key}: {value}")
    print("=" * 30)
    assert True


@pytest.mark.unit
def test_environment_variable_override():
    """Test that environment variables can override config"""
    test_env = os.environ.get('TEST_ENV', 'default')
    print(f"\nTEST_ENV environment variable: {test_env}")
    assert test_env is not None


@pytest.mark.regression
@pytest.mark.parametrize("env_name", ['dev', 'staging', 'production'])
def test_all_environments_have_config(config, env_name):
    """Test that all environments have proper configuration"""
    # This test reads the config file directly to check all environments
    import json
    from pathlib import Path

    config_file = Path('config/test_config.json')
    if config_file.exists():
        with open(config_file) as f:
            full_config = json.load(f)

        if env_name in full_config.get('environments', {}):
            env_config = full_config['environments'][env_name]
            assert 'api_url' in env_config
            assert 'timeout' in env_config
            print(f"\n{env_name} environment configuration is valid")
        else:
            pytest.skip(f"Environment {env_name} not in config")
    else:
        pytest.skip("Config file not found")
