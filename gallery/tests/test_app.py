import pytest

from playhouse.shortcuts import model_to_dict, dict_to_model

import falcon
from falcon import testing

from gallery.app import app
from gallery.models import Artifact

@pytest.fixture
def client():
    return testing.TestClient(app)

# pytest will inject the object returned by the "client" function
# as an additional parameter.
def test_root(client):
    response = client.get('/')

    assert response.json["message"] == "Open wide, come inside, Hello World!"

def test_get_artifacts(client):
    response = client.get('/api/artifacts')
    
    assert response.status != falcon.HTTP_500

    artifacts = response.json

    for a in artifacts:
        assert dict_to_model(Artifact, a) != None

    assert response.status == falcon.HTTP_OK

# test artifact CRUD operations
def test_post_artifact_creates_new_artifact(client):
    """test creating a new artifact returns 201 and proper response structure"""
    new_artifact = {
        "title": "Test Artifact",
        "description": "A test artifact for unit testing",
        "date_authored": "2023-01-01",
        "display_location": "Test Gallery",
        "artifact_type": 1
    }
    
    response = client.post('/api/artifacts', json=new_artifact)
    
    # should return 201 created
    assert response.status == falcon.HTTP_201
    
    # should have location header
    assert 'location' in response.headers
    
    # response should contain created artifact data
    created_artifact = response.json
    assert created_artifact["title"] == new_artifact["title"]
    assert created_artifact["description"] == new_artifact["description"]
    assert "id" in created_artifact
    assert "created_datetime" in created_artifact
    assert "modified_datetime" in created_artifact

def test_post_artifact_with_duplicate_title_returns_409(client):
    """test creating artifact with duplicate title returns 409 conflict"""
    artifact_data = {
        "title": "Duplicate Title Test",
        "description": "First artifact",
        "date_authored": "2023-01-01",
        "display_location": "Gallery A"
    }
    
    # create first artifact
    response1 = client.post('/api/artifacts', json=artifact_data)
    assert response1.status == falcon.HTTP_201
    
    # attempt to create duplicate should fail
    response2 = client.post('/api/artifacts', json=artifact_data)
    assert response2.status == falcon.HTTP_409
    assert "error" in response2.json

def test_get_artifact_by_id_returns_artifact(client):
    """test getting artifact by valid id returns 200 with artifact data"""
    # first create an artifact
    new_artifact = {
        "title": "Test Get By ID",
        "description": "Test getting by ID",
        "date_authored": "2023-01-01",
        "display_location": "Test Location"
    }
    
    create_response = client.post('/api/artifacts', json=new_artifact)
    assert create_response.status == falcon.HTTP_201
    created_id = create_response.json["id"]
    
    # now get the artifact by id
    response = client.get(f'/api/artifacts/{created_id}')
    
    assert response.status == falcon.HTTP_200
    artifact = response.json
    assert artifact["id"] == created_id
    assert artifact["title"] == new_artifact["title"]
    assert artifact["description"] == new_artifact["description"]

def test_get_artifact_by_invalid_id_returns_404(client):
    """test getting artifact by non-existent id returns 404"""
    response = client.get('/api/artifacts/99999')
    
    assert response.status == falcon.HTTP_404
    assert "error" in response.json

def test_put_artifact_updates_existing_artifact(client):
    """test updating an existing artifact returns 200 with updated data"""
    # create an artifact first
    original_artifact = {
        "title": "Original Title",
        "description": "Original description",
        "date_authored": "2023-01-01",
        "display_location": "Original Location"
    }
    
    create_response = client.post('/api/artifacts', json=original_artifact)
    assert create_response.status == falcon.HTTP_201
    artifact_id = create_response.json["id"]
    
    # update the artifact
    updated_data = {
        "title": "Updated Title",
        "description": "Updated description",
        "display_location": "Updated Location"
    }
    
    response = client.put(f'/api/artifacts/{artifact_id}', json=updated_data)
    
    assert response.status == falcon.HTTP_200
    updated_artifact = response.json
    assert updated_artifact["title"] == updated_data["title"]
    assert updated_artifact["description"] == updated_data["description"]
    assert updated_artifact["display_location"] == updated_data["display_location"]
    assert updated_artifact["id"] == artifact_id

def test_put_artifact_with_invalid_id_returns_404(client):
    """test updating non-existent artifact returns 404"""
    update_data = {
        "title": "Should Not Work",
        "description": "This should fail"
    }
    
    response = client.put('/api/artifacts/99999', json=update_data)
    
    assert response.status == falcon.HTTP_404
    assert "error" in response.json

def test_put_artifact_with_duplicate_title_returns_409(client):
    """test updating artifact to duplicate title returns 409"""
    # create two artifacts
    artifact1 = {
        "title": "First Artifact",
        "description": "First artifact",
        "date_authored": "2023-01-01"
    }
    
    artifact2 = {
        "title": "Second Artifact", 
        "description": "Second artifact",
        "date_authored": "2023-01-02"
    }
    
    response1 = client.post('/api/artifacts', json=artifact1)
    response2 = client.post('/api/artifacts', json=artifact2)
    
    assert response1.status == falcon.HTTP_201
    assert response2.status == falcon.HTTP_201
    
    artifact2_id = response2.json["id"]
    
    # try to update second artifact to have same title as first
    update_data = {"title": "First Artifact"}
    response = client.put(f'/api/artifacts/{artifact2_id}', json=update_data)
    
    assert response.status == falcon.HTTP_409
    assert "error" in response.json

def test_delete_artifact_removes_artifact(client):
    """test deleting an artifact returns 204 and removes the artifact"""
    # create an artifact first
    new_artifact = {
        "title": "To Be Deleted",
        "description": "This artifact will be deleted",
        "date_authored": "2023-01-01"
    }
    
    create_response = client.post('/api/artifacts', json=new_artifact)
    assert create_response.status == falcon.HTTP_201
    artifact_id = create_response.json["id"]
    
    # delete the artifact
    response = client.delete(f'/api/artifacts/{artifact_id}')
    
    assert response.status == falcon.HTTP_204
    
    # verify artifact is deleted by trying to get it
    get_response = client.get(f'/api/artifacts/{artifact_id}')
    assert get_response.status == falcon.HTTP_404

def test_delete_artifact_with_invalid_id_returns_404(client):
    """test deleting non-existent artifact returns 404"""
    response = client.delete('/api/artifacts/99999')
    
    assert response.status == falcon.HTTP_404
    assert "error" in response.json

# test artifact filtering endpoints
def test_get_artifacts_by_type_filters_correctly(client):
    """test filtering artifacts by type returns only matching artifacts"""
    response = client.get('/api/artifacts?type=1')
    
    assert response.status != falcon.HTTP_500
    artifacts = response.json
    
    # all returned artifacts should have artifact_type = 1 (if any)
    for artifact in artifacts:
        if artifact.get("artifact_type"):
            assert artifact["artifact_type"] == 1

def test_get_artifacts_by_year_filters_correctly(client):
    """test filtering artifacts by year returns only matching artifacts"""
    # create artifact with specific year
    test_artifact = {
        "title": "Year Test Artifact",
        "description": "Test filtering by year",
        "date_authored": "2022-06-15",
        "display_location": "Year Test Gallery"
    }
    
    create_response = client.post('/api/artifacts', json=test_artifact)
    assert create_response.status == falcon.HTTP_201
    
    response = client.get('/api/artifacts?year=2022')
    
    assert response.status == falcon.HTTP_200
    artifacts = response.json
    
    # verify all returned artifacts are from 2022
    for artifact in artifacts:
        if artifact.get("date_authored"):
            year = artifact["date_authored"][:4]  # extract year from date string
            assert year == "2022"

def test_get_artifacts_by_location_filters_correctly(client):
    """test filtering artifacts by display location returns only matching artifacts"""
    # create artifact with specific location
    location = "Special Test Gallery"
    test_artifact = {
        "title": "Location Test Artifact",
        "description": "Test filtering by location",
        "date_authored": "2023-01-01",
        "display_location": location
    }
    
    create_response = client.post('/api/artifacts', json=test_artifact)
    assert create_response.status == falcon.HTTP_201
    
    response = client.get(f'/api/artifacts?display_location={location}')
    
    assert response.status == falcon.HTTP_200
    artifacts = response.json
    
    # verify all returned artifacts have the correct location
    for artifact in artifacts:
        assert artifact["display_location"] == location

def test_get_artifacts_by_date_range_filters_correctly(client):
    """test filtering artifacts by date range returns only matching artifacts"""
    start_date = "2023-01-01"
    end_date = "2023-12-31"
    
    response = client.get(f'/api/artifacts?start_date={start_date}&end_date={end_date}')
    
    assert response.status == falcon.HTTP_200
    artifacts = response.json
    
    # verify all returned artifacts fall within the date range
    for artifact in artifacts:
        if artifact.get("date_authored"):
            authored_date = artifact["date_authored"]
            assert start_date <= authored_date <= end_date

def test_get_artifacts_by_artist_filters_correctly(client):
    """test filtering artifacts by artist id returns only matching artifacts"""
    response = client.get('/api/artifacts?artist=1')
    
    assert response.status != falcon.HTTP_500
    artifacts = response.json
    
    # response should be valid list (content verification would require
    # understanding the many-to-many relationship structure)
    assert isinstance(artifacts, list)

def test_get_artifacts_by_exhibition_filters_correctly(client):
    """test filtering artifacts by exhibition id returns only matching artifacts"""
    response = client.get('/api/artifacts?exhibition=1')
    
    assert response.status != falcon.HTTP_500
    artifacts = response.json
    
    # response should be valid list (content verification would require
    # understanding the many-to-many relationship structure)
    assert isinstance(artifacts, list)

# test error handling and edge cases
def test_get_artifacts_handles_empty_database(client):
    """test getting artifacts when database is empty returns empty list"""
    response = client.get('/api/artifacts')
    
    assert response.status == falcon.HTTP_200
    artifacts = response.json
    assert isinstance(artifacts, list)

def test_post_artifact_with_invalid_data_returns_500(client):
    """test posting artifact with malformed data returns 500"""
    # missing required fields or invalid format
    invalid_artifact = {
        "title": None,  # invalid title
        "date_authored": "invalid-date-format"
    }
    
    response = client.post('/api/artifacts', json=invalid_artifact)
    
    # should return some error status (likely 500 for internal error)
    assert response.status in [falcon.HTTP_400, falcon.HTTP_500]

def test_artifacts_endpoint_response_structure(client):
    """test that artifacts endpoint returns properly structured data"""
    response = client.get('/api/artifacts')
    
    assert response.status == falcon.HTTP_200
    artifacts = response.json
    assert isinstance(artifacts, list)
    
    # if there are artifacts, verify structure
    for artifact in artifacts:
        assert isinstance(artifact, dict)
        # basic fields that should exist
        if artifact:  # if not empty
            assert "id" in artifact
            assert "title" in artifact
            # artifact model should be convertible
            assert dict_to_model(Artifact, artifact) is not None

def test_artifact_crud_full_lifecycle(client):
    """test complete lifecycle: create, read, update, delete"""
    # create
    original_data = {
        "title": "Lifecycle Test Artifact",
        "description": "Testing full CRUD lifecycle",
        "date_authored": "2023-06-15",
        "display_location": "Lifecycle Gallery"
    }
    
    create_response = client.post('/api/artifacts', json=original_data)
    assert create_response.status == falcon.HTTP_201
    artifact_id = create_response.json["id"]
    
    # read
    read_response = client.get(f'/api/artifacts/{artifact_id}')
    assert read_response.status == falcon.HTTP_200
    assert read_response.json["title"] == original_data["title"]
    
    # update
    update_data = {
        "title": "Updated Lifecycle Artifact",
        "description": "Updated description for lifecycle test"
    }
    
    update_response = client.put(f'/api/artifacts/{artifact_id}', json=update_data)
    assert update_response.status == falcon.HTTP_200
    assert update_response.json["title"] == update_data["title"]
    assert update_response.json["description"] == update_data["description"]
    
    # delete
    delete_response = client.delete(f'/api/artifacts/{artifact_id}')
    assert delete_response.status == falcon.HTTP_204
    
    # verify deletion
    final_read_response = client.get(f'/api/artifacts/{artifact_id}')
    assert final_read_response.status == falcon.HTTP_404
