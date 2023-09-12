import http
import integration_testing_utilities
import requests
import furl

def test_application():
    with integration_testing_utilities.TempContainer("local/application") as container:
        container_address = container.ports["8000/tcp"][0]
        url = furl.furl(f"http://{container_address['HostIp']}:{container_address['HostPort']}")
        response = integration_testing_utilities.patient_request("GET", (url/"status"))
        data = response.json()
        assert response.status_code == 200
        assert data["status"] == "ok"

        response = requests.post((url/"snippets").url,json={"name":"Valid snippet","snippet":"print('hello world')"})
        assert response.status_code == http.HTTPStatus.CREATED
        valid_snippet_id = response.json()["id"]

        response = requests.get((url/"snippets").url)
        data = response.json()
        assert len(data["snippets"]) == 1
        assert data["snippets"][0]["name"] == "Valid snippet"
        assert requests.get((url/"snippets"/str(valid_snippet_id)).url).status_code == http.HTTPStatus.OK

        response = requests.post((url/"snippets").url,json={"name":"Invalid snippet","snippet":"This is not valid python."})
        assert response.status_code == http.HTTPStatus.UNPROCESSABLE_ENTITY
        response = requests.get((url/"snippets").url)
        data = response.json()
        assert len(data["snippets"]) == 1

        response = requests.delete((url/"snippets"/str(valid_snippet_id)).url)
        assert response.status_code == http.HTTPStatus.NO_CONTENT

        # Now everything is cleaned up.
        assert len(requests.get((url/"snippets").url).json()["snippets"]) == 0
        assert requests.get((url/"snippets"/str(valid_snippet_id)).url).status_code == http.HTTPStatus.NOT_FOUND
