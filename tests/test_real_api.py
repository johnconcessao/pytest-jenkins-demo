"""
Real REST API tests using JSONPlaceholder
Demonstrates actual HTTP requests with Jenkins parameters and JSON config
"""
import pytest
import requests
import time
import json


@pytest.fixture
def api_client(config, api_config):
    """Create an API client with base configuration"""
    class APIClient:
        def __init__(self, base_url, timeout, retry_count):
            self.base_url = base_url
            self.timeout = timeout
            self.retry_count = retry_count
            self.session = requests.Session()

        def get(self, endpoint, **kwargs):
            """GET request with retry logic"""
            url = f"{self.base_url}{endpoint}"
            for attempt in range(self.retry_count):
                try:
                    response = self.session.get(url, timeout=self.timeout, **kwargs)
                    return response
                except requests.exceptions.RequestException as e:
                    if attempt == self.retry_count - 1:
                        raise
                    time.sleep(0.5 * (attempt + 1))

        def post(self, endpoint, data=None, **kwargs):
            """POST request with retry logic"""
            url = f"{self.base_url}{endpoint}"
            response = self.session.post(url, json=data, timeout=self.timeout, **kwargs)
            return response

        def put(self, endpoint, data=None, **kwargs):
            """PUT request"""
            url = f"{self.base_url}{endpoint}"
            response = self.session.put(url, json=data, timeout=self.timeout, **kwargs)
            return response

        def delete(self, endpoint, **kwargs):
            """DELETE request"""
            url = f"{self.base_url}{endpoint}"
            response = self.session.delete(url, timeout=self.timeout, **kwargs)
            return response

    return APIClient(
        base_url=api_config['url'],
        timeout=api_config['timeout'],
        retry_count=api_config['retry_count']
    )


@pytest.mark.smoke
@pytest.mark.api
def test_api_health_check(api_client, config, environment):
    """Test API is reachable and responding"""
    print(f"\n{'='*70}")
    print(f"API HEALTH CHECK - {environment.upper()} Environment")
    print(f"{'='*70}")
    print(f"Testing: {api_client.base_url}")
    print(f"Timeout: {api_client.timeout}s")
    print(f"Build: {config['job_name']} #{config['build_number']}")

    start_time = time.time()
    response = api_client.get('/posts/1')
    duration = (time.time() - start_time) * 1000

    print(f"\nResponse:")
    print(f"  Status Code: {response.status_code}")
    print(f"  Response Time: {duration:.2f}ms")
    print(f"  Content Length: {len(response.content)} bytes")

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert duration < config.get('max_response_time', 5000), f"Response too slow: {duration}ms"
    print(f"\n✓ API Health Check PASSED")
    print(f"{'='*70}\n")


@pytest.mark.regression
@pytest.mark.api
def test_get_all_posts(api_client, config):
    """Test fetching all posts from API"""
    print(f"\nTesting: GET /posts")

    response = api_client.get('/posts')

    assert response.status_code == 200
    posts = response.json()

    print(f"Response: {response.status_code}")
    print(f"Posts Count: {len(posts)}")
    print(f"Expected: {config['test_data']['expected_post_count']}")

    assert isinstance(posts, list), "Response should be a list"
    assert len(posts) == config['test_data']['expected_post_count'], \
        f"Expected {config['test_data']['expected_post_count']} posts"

    # Verify structure of first post
    if posts:
        first_post = posts[0]
        assert 'id' in first_post
        assert 'userId' in first_post
        assert 'title' in first_post
        assert 'body' in first_post
        print(f"Sample Post: ID={first_post['id']}, Title='{first_post['title'][:30]}...'")

    print("✓ GET all posts PASSED")


@pytest.mark.smoke
@pytest.mark.api
def test_get_single_post(api_client, config):
    """Test fetching a single post by ID"""
    post_id = config['test_data']['sample_post_id']
    print(f"\nTesting: GET /posts/{post_id}")

    start_time = time.time()
    response = api_client.get(f'/posts/{post_id}')
    duration = (time.time() - start_time) * 1000

    assert response.status_code == 200
    post = response.json()

    print(f"Response Time: {duration:.2f}ms")
    print(f"Post ID: {post['id']}")
    print(f"User ID: {post['userId']}")
    print(f"Title: {post['title']}")
    print(f"Body: {post['body'][:50]}...")

    assert post['id'] == post_id
    assert 'userId' in post
    assert 'title' in post
    assert 'body' in post
    assert len(post['title']) > 0
    assert len(post['body']) > 0

    print("✓ GET single post PASSED")


@pytest.mark.regression
@pytest.mark.api
def test_get_all_users(api_client, config):
    """Test fetching all users"""
    print(f"\nTesting: GET /users")

    response = api_client.get('/users')

    assert response.status_code == 200
    users = response.json()

    print(f"Response: {response.status_code}")
    print(f"Users Count: {len(users)}")
    print(f"Expected: {config['test_data']['expected_user_count']}")

    assert len(users) == config['test_data']['expected_user_count']

    # Verify structure
    if users:
        first_user = users[0]
        assert 'id' in first_user
        assert 'name' in first_user
        assert 'username' in first_user
        assert 'email' in first_user
        print(f"Sample User: {first_user['name']} ({first_user['email']})")

    print("✓ GET all users PASSED")


@pytest.mark.unit
@pytest.mark.api
def test_get_user_posts(api_client, config):
    """Test fetching posts for a specific user"""
    user_id = config['test_data']['sample_user_id']
    print(f"\nTesting: GET /posts?userId={user_id}")

    response = api_client.get('/posts', params={'userId': user_id})

    assert response.status_code == 200
    posts = response.json()

    print(f"Posts by User {user_id}: {len(posts)}")

    assert isinstance(posts, list)
    assert len(posts) > 0, f"User {user_id} should have posts"

    # Verify all posts belong to the user
    for post in posts:
        assert post['userId'] == user_id, f"Post {post['id']} belongs to different user"

    print(f"All {len(posts)} posts verified for user {user_id}")
    print("✓ GET user posts PASSED")


@pytest.mark.unit
@pytest.mark.api
def test_get_post_comments(api_client, config):
    """Test fetching comments for a specific post"""
    post_id = config['test_data']['sample_post_id']
    print(f"\nTesting: GET /posts/{post_id}/comments")

    response = api_client.get(f'/posts/{post_id}/comments')

    assert response.status_code == 200
    comments = response.json()

    print(f"Comments on Post {post_id}: {len(comments)}")

    assert isinstance(comments, list)
    assert len(comments) > 0

    # Verify structure
    if comments:
        first_comment = comments[0]
        assert 'postId' in first_comment
        assert 'id' in first_comment
        assert 'name' in first_comment
        assert 'email' in first_comment
        assert 'body' in first_comment
        assert first_comment['postId'] == post_id
        print(f"Sample Comment: '{first_comment['name']}' by {first_comment['email']}")

    print("✓ GET post comments PASSED")


@pytest.mark.smoke
@pytest.mark.api
def test_create_post(api_client, config, environment):
    """Test creating a new post via POST request"""
    print(f"\nTesting: POST /posts (Environment: {environment})")

    new_post = {
        'title': f'Test Post from Jenkins Build #{config["build_number"]}',
        'body': f'This is a test post created in {environment} environment',
        'userId': config['test_data']['sample_user_id']
    }

    print(f"Creating post: {json.dumps(new_post, indent=2)}")

    response = api_client.post('/posts', data=new_post)

    assert response.status_code == 201, f"Expected 201 Created, got {response.status_code}"
    created_post = response.json()

    print(f"\nResponse: {response.status_code}")
    print(f"Created Post ID: {created_post.get('id')}")
    print(f"Title: {created_post.get('title')}")

    assert 'id' in created_post
    assert created_post['title'] == new_post['title']
    assert created_post['body'] == new_post['body']
    assert created_post['userId'] == new_post['userId']

    print("✓ POST create post PASSED")


@pytest.mark.unit
@pytest.mark.api
def test_update_post_put(api_client, config):
    """Test updating a post using PUT"""
    post_id = config['test_data']['sample_post_id']
    print(f"\nTesting: PUT /posts/{post_id}")

    updated_data = {
        'id': post_id,
        'title': 'Updated Title via PUT',
        'body': 'Updated body content',
        'userId': 1
    }

    response = api_client.put(f'/posts/{post_id}', data=updated_data)

    assert response.status_code == 200
    updated_post = response.json()

    print(f"Response: {response.status_code}")
    print(f"Updated Post: {updated_post['title']}")

    assert updated_post['title'] == updated_data['title']
    assert updated_post['body'] == updated_data['body']

    print("✓ PUT update post PASSED")


@pytest.mark.unit
@pytest.mark.api
def test_delete_post(api_client, config):
    """Test deleting a post"""
    post_id = config['test_data']['sample_post_id']
    print(f"\nTesting: DELETE /posts/{post_id}")

    response = api_client.delete(f'/posts/{post_id}')

    assert response.status_code == 200
    print(f"Response: {response.status_code}")
    print(f"Post {post_id} deleted successfully")

    print("✓ DELETE post PASSED")


@pytest.mark.regression
@pytest.mark.api
def test_api_performance(api_client, config, environment):
    """Test API response time meets performance threshold"""
    print(f"\n{'='*70}")
    print(f"API PERFORMANCE TEST - {environment.upper()}")
    print(f"{'='*70}")

    threshold = config['thresholds'].get('api_max_response_time_ms', 3000)
    print(f"Performance Threshold: {threshold}ms")

    endpoints = ['/posts/1', '/users/1', '/comments/1']
    results = []

    for endpoint in endpoints:
        start_time = time.time()
        response = api_client.get(endpoint)
        duration = (time.time() - start_time) * 1000

        results.append({
            'endpoint': endpoint,
            'duration': duration,
            'status': response.status_code
        })

        print(f"\n{endpoint}:")
        print(f"  Status: {response.status_code}")
        print(f"  Time: {duration:.2f}ms")
        print(f"  {'✓ PASS' if duration < threshold else '✗ FAIL'}")

        assert response.status_code == 200
        assert duration < threshold, f"{endpoint} took {duration}ms, exceeds {threshold}ms"

    avg_duration = sum(r['duration'] for r in results) / len(results)
    print(f"\nAverage Response Time: {avg_duration:.2f}ms")
    print(f"All endpoints under threshold: ✓")
    print(f"{'='*70}\n")


@pytest.mark.smoke
@pytest.mark.api
def test_api_with_jenkins_params_and_json_config(api_client, config, environment, api_config):
    """
    Comprehensive test showing integration of:
    1. Real REST API calls (JSONPlaceholder)
    2. Jenkins parameters (environment, build number)
    3. JSON configuration (API URL, timeouts, thresholds)
    """
    print(f"\n{'='*70}")
    print(f"COMPREHENSIVE REAL API + JENKINS + JSON CONFIG TEST")
    print(f"{'='*70}")

    # Part 1: Jenkins Parameters
    print(f"\n[1] JENKINS PARAMETERS:")
    print(f"    Environment: {environment}")
    print(f"    Job: {config['job_name']}")
    print(f"    Build: #{config['build_number']}")

    # Part 2: JSON Configuration
    print(f"\n[2] JSON CONFIG FOR '{environment.upper()}':")
    print(f"    API URL: {api_config['url']}")
    print(f"    Timeout: {api_config['timeout']}s")
    print(f"    Retry Count: {api_config['retry_count']}")
    print(f"    Max Response: {config.get('max_response_time', 5000)}ms")

    # Part 3: Real API Call
    print(f"\n[3] MAKING REAL API CALL:")
    print(f"    Target: {api_client.base_url}/posts/1")

    start_time = time.time()
    response = api_client.get('/posts/1')
    duration = (time.time() - start_time) * 1000

    print(f"    Status: {response.status_code}")
    print(f"    Time: {duration:.2f}ms")
    print(f"    Size: {len(response.content)} bytes")

    # Part 4: Response Validation
    print(f"\n[4] RESPONSE VALIDATION:")
    post = response.json()
    print(f"    Post ID: {post['id']}")
    print(f"    User ID: {post['userId']}")
    print(f"    Title: {post['title']}")
    print(f"    Body Length: {len(post['body'])} chars")

    # Assertions
    assert response.status_code == 200, "API should return 200 OK"
    assert duration < config.get('max_response_time', 5000), \
        f"Response time {duration}ms exceeds threshold"
    assert 'id' in post and post['id'] == 1
    assert 'title' in post and len(post['title']) > 0

    # Part 5: Summary
    print(f"\n[5] INTEGRATION SUMMARY:")
    print(f"    ✓ Jenkins parameters received")
    print(f"    ✓ JSON config loaded for {environment}")
    print(f"    ✓ Real API call successful")
    print(f"    ✓ Response validated")
    print(f"    ✓ Performance threshold met")

    print(f"\n{'='*70}")
    print(f"✓ ALL CHECKS PASSED - REAL API TEST SUCCESSFUL!")
    print(f"{'='*70}\n")
