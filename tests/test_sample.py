"""
Sample pytest tests with markers for Jenkins demo
"""
import pytest
import os


# Test markers for different test suites
@pytest.mark.smoke
def test_basic_addition():
    """Basic smoke test - simple addition"""
    assert 1 + 1 == 2


@pytest.mark.smoke
def test_basic_subtraction():
    """Basic smoke test - simple subtraction"""
    assert 5 - 3 == 2


@pytest.mark.unit
def test_string_operations():
    """Unit test - string operations"""
    test_string = "Hello Jenkins"
    assert test_string.upper() == "HELLO JENKINS"
    assert len(test_string) == 13


@pytest.mark.unit
def test_list_operations():
    """Unit test - list operations"""
    test_list = [1, 2, 3, 4, 5]
    assert len(test_list) == 5
    assert sum(test_list) == 15
    assert max(test_list) == 5


@pytest.mark.regression
def test_environment_variable():
    """Regression test - check environment variables"""
    test_env = os.environ.get('TEST_ENV', 'not_set')
    print(f"Current TEST_ENV: {test_env}")
    # This will pass regardless but shows parameter in action
    assert test_env in ['staging', 'production', 'dev', 'not_set']


@pytest.mark.regression
def test_dictionary_operations():
    """Regression test - dictionary operations"""
    test_dict = {'name': 'Jenkins', 'type': 'CI/CD', 'version': '2.0'}
    assert 'name' in test_dict
    assert test_dict['name'] == 'Jenkins'
    assert len(test_dict) == 3


@pytest.mark.smoke
@pytest.mark.unit
def test_boolean_logic():
    """Test with multiple markers - boolean logic"""
    assert True is True
    assert False is not True
    assert not False


@pytest.mark.regression
def test_multiplication():
    """Regression test - multiplication"""
    assert 3 * 4 == 12
    assert 7 * 0 == 0


def test_no_marker():
    """Test without marker - runs with 'all' suite"""
    assert "pytest" in "pytest is awesome"


class TestCalculator:
    """Test class for calculator operations"""

    @pytest.mark.unit
    def test_add(self):
        """Test addition"""
        assert 10 + 5 == 15

    @pytest.mark.unit
    def test_divide(self):
        """Test division"""
        assert 10 / 2 == 5

    @pytest.mark.unit
    def test_divide_by_zero(self):
        """Test division by zero raises exception"""
        with pytest.raises(ZeroDivisionError):
            result = 10 / 0


@pytest.mark.smoke
def test_jenkins_parameters_demo():
    """
    Test to demonstrate Jenkins parameters
    Prints environment variables set by Jenkins
    """
    print("\n=== Jenkins Parameters Demo ===")
    print(f"TEST_ENV: {os.environ.get('TEST_ENV', 'Not set')}")
    print(f"WORKSPACE: {os.environ.get('WORKSPACE', 'Not set')}")
    print(f"BUILD_NUMBER: {os.environ.get('BUILD_NUMBER', 'Not set')}")
    print(f"JOB_NAME: {os.environ.get('JOB_NAME', 'Not set')}")
    print("================================\n")
    assert True  # Always passes


@pytest.mark.parametrize("input_val,expected", [
    (2, 4),
    (3, 9),
    (4, 16),
    (5, 25),
])
@pytest.mark.unit
def test_square_numbers(input_val, expected):
    """Parameterized test - square numbers"""
    assert input_val ** 2 == expected


@pytest.fixture
def sample_data():
    """Fixture providing sample data"""
    return {"users": ["Alice", "Bob", "Charlie"], "count": 3}


@pytest.mark.regression
def test_with_fixture(sample_data):
    """Test using fixture"""
    assert sample_data["count"] == len(sample_data["users"])
    assert "Alice" in sample_data["users"]
