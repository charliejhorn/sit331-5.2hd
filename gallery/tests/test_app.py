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
    
    artifacts = response.json

    for a in artifacts:
        assert dict_to_model(Artifact, a) != None
    
    assert response.status == falcon.HTTP_OK