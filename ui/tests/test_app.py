def test_request_example(client):
    response = client.get("/")
    assert b"eCOBIDAS" in response.data
    response = client.get("/faq/")
    assert b"FAQ" in response.data
    response = client.get("/about/")
    assert b"about" in response.data
    response = client.get("/protocols/neurovault/mri_acquisition")
    assert b"neurovault" in response.data
