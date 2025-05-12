import pytest
from app import app  # assuming your Flask app is in app.py

# This is the test for the index route
def test_index():
    client = app.test_client()  # Create a test client
    response = client.get('/', follow_redirects=True)  # Send a GET request to the root route
    assert response.status_code == 200  # Check that the status code is 200 (OK)
    

# Test for the new feature route
def test_new_feature():
    client = app.test_client()
    response = client.get('/new-feature')
    assert response.status_code == 200
    assert b"This is a new feature!" in response.data
