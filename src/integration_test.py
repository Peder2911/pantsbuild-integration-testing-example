import integration_testing_utilities

def test_application():
    with integration_testing_utilities.TempContainer("local/application") as container:
        container_address = container.ports["8000/tcp"][0]
        response = integration_testing_utilities.patient_request("GET", f"http://{container_address['HostIp']}:{container_address['HostPort']}")
        data = response.json()

        assert response.status_code == 200
        assert data["message"] == "Hello world!"
