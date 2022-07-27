import os
import sys
from urllib import response

from requests import request
import pytest
from fastapi.testclient import TestClient
from service.api import app

# a token representing the tokens API or tenants API is required for running the tests.
TOKENS_API_TOKEN = os.environ.get('TOKENS_API_TOKEN')

if not TOKENS_API_TOKEN:
    sys.exit("TOKENS_API_TOKEN not set. aborting...")

@pytest.fixture
def client():
    return TestClient(app)


# =====================
# Actual test functions
# =====================

def test_ready(client):
    response = client.get("v3/site-router/ready")
    assert response.status_code == 200

def get_revoke_token_str():
    """
    returns the JWT string that will be revoked in the test suite.
    """
    return """eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJqdGkiOiI5MjNkN2JiOS1iMDFkLTRlYzUtYmU0My04NzY1NjRiYzU4YTQiLCJpc3MiOiJodHRwczovL2Rldi5kZXZlbG9wLnRhcGlzLmlvL3YzL3Rva2VucyIsInN1YiI6InRlc3R1c2VyM0BkZXYiLCJ0YXBpcy90ZW5hbnRfaWQiOiJkZXYiLCJ0YXBpcy90b2tlbl90eXBlIjoiYWNjZXNzIiwidGFwaXMvZGVsZWdhdGlvbiI6ZmFsc2UsInRhcGlzL2RlbGVnYXRpb25fc3ViIjpudWxsLCJ0YXBpcy91c2VybmFtZSI6InRlc3R1c2VyMyIsInRhcGlzL2FjY291bnRfdHlwZSI6InVzZXIiLCJleHAiOjE2NTg5NTU1MzAsInRhcGlzL2NsaWVudF9pZCI6bnVsbCwidGFwaXMvZ3JhbnRfdHlwZSI6InBhc3N3b3JkIn0.J5vB5wY5boAfB8XCKmaoG3I4ee91O9t52mNvTR49wfFlqQi3IwvC1I6cNh1SASDHsvhZ2AwtHi0GZ5jvCdJDOi4xpbuEmYusKp2jnSZtZiJh5O338BNgXSrW-o26u8m0OmAU1JEpTC4OEdTQTgkCAOHYmgDd8a8NBu_sRHQPluyus8r7oTCilcwoenXnNL7EHHV6AUtjgWsNItRePI94AtHkGyhChCiW1eds8a1NLOuEpQq6KNL1ytaUs-K-Ik6Dercv6cX1O-AO0LN1LWSLSDy5YAjQwhvo8KivKSQ2R8szgPcOFYEkBai17QMdjoCXG7--lkt07_v8ZXgMxhckJQ"""


def get_unrevoked_token_str():
    return """eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJqdGkiOiI0NzAwODBhNi1lYzIxLTQ3MGUtOGJmNC1iZjVhZDZlMzQwZDQiLCJpc3MiOiJodHRwczovL2Rldi5kZXZlbG9wLnRhcGlzLmlvL3YzL3Rva2VucyIsInN1YiI6InRlc3R1c2VyM0BkZXYiLCJ0YXBpcy90ZW5hbnRfaWQiOiJkZXYiLCJ0YXBpcy90b2tlbl90eXBlIjoiYWNjZXNzIiwidGFwaXMvZGVsZWdhdGlvbiI6ZmFsc2UsInRhcGlzL2RlbGVnYXRpb25fc3ViIjpudWxsLCJ0YXBpcy91c2VybmFtZSI6InRlc3R1c2VyMyIsInRhcGlzL2FjY291bnRfdHlwZSI6InVzZXIiLCJleHAiOjE2NTg5NjU0OTYsInRhcGlzL2NsaWVudF9pZCI6bnVsbCwidGFwaXMvZ3JhbnRfdHlwZSI6InBhc3N3b3JkIn0.UZdTobQxPFaA80OD7816Kg9QhQJVNc0FEcYjoESsKqittl2yi8HPNcMHFGvO1xbIvVK0DjIMXGK-uNIXatsCHZHc6w7itGMo4tedF3oY-ceKM3duBp5vcP7gxN6sriSv3U5ICetJIHjWaMVKFfgLmZLlu-P83Je3xnYXRsOf08MzKOw_sdvdnw72gPTEe2dJuKO9kA39wjzj1OO4Is1cUDRb6C8pAPJGUb99i8bbrO2M7nzShHU9Y_HfHHJaLWl1tBFWxp4FSKuHdtVfrVPUjQJrqU-lht6i7t5r7ApZu1Xd_b8IEvv-rCwExhSDDd6R6GebLlRSqOi2-imuNgoyXA"""

def test_test_user_cannot_revoke_token(client):
    response = client.post("v3/site-router/tokens/revoke", 
                            headers={"X-Tapis-Token": get_unrevoked_token_str()},
                            json={"token": get_revoke_token_str()})
    print(response.content)
    assert response.status_code == 400
    

def test_revoke_valid(client):
    response = client.post("v3/site-router/tokens/revoke", 
                            headers={"X-Tapis-Token": TOKENS_API_TOKEN},
                            json={"token": get_revoke_token_str()})
    print(response.content)
    assert response.status_code == 200

def test_revoked_token_is_revoked(client):
    response = client.get("v3/site-router/tokens/check",
                           headers={"X-Tapis-Token": get_revoke_token_str()}
    )
    print(response.content)
    assert response.status_code == 400

def test_unrevoked_token_is_valid(client):
    response = client.get("v3/site-router/tokens/check",
                           headers={"X-Tapis-Token": get_unrevoked_token_str()}
    )
    print(response.content)
    assert response.status_code == 200
