import time
import docker
import docker.errors
import requests

class TempContainer():
    def __init__(self, image: str, port: int = 8000):
        self._image = image
        self._client = docker.from_env()
        self._container = self._client.containers.run(image = self._image, detach = True, remove = True, ports = {f"{port}": None})

    def __enter__(self):
        self._container.reload()
        return self._container

    def __exit__(self, *args):
        try:
            self._container.kill()
        except docker.errors.NotFound:
            ...

def patient_request(*args, timeout: int = 30, **kwargs):
    start = time.time()
    while True:
        try:
            return requests.request(*args, **kwargs)
        except requests.ConnectionError:
            if (time.time()-start) > timeout:
                break
            time.sleep(.1)
    raise ConnectionError
