![EPFL Center for Imaging logo](https://imaging.epfl.ch/resources/logo-for-gitlab.svg)
# {{ cookiecutter.project_name }} API in docker

Implementation of a web API server for [{{ cookiecutter.package_name }}]({{ cookiecutter.project_url }}).

Author: {{ cookiecutter.author }}

## Running with `docker-compose`

```
docker compose up
```

## Running with `docker`

Build the docker image:

```
docker build -t serverkit-{{ cookiecutter.package_name }} .
```

Run the server in a container:

```
docker run -it --rm -p 8000:8000 serverkit-{{ cookiecutter.package_name }}:latest
```

Running tests:

```
docker run --rm serverkit-{{ cookiecutter.package_name }}:latest pytest
```

Pushing the image to `registry.rcp.epfl.ch`:

```
docker tag serverkit-{{ cookiecutter.package_name }} registry.rcp.epfl.ch/imaging-server-kit/serverkit-{{ cookiecutter.package_name }}
docker push registry.rcp.epfl.ch/imaging-server-kit/serverkit-{{ cookiecutter.package_name }}
```

## Installation with `pip`

Install dependencies:

```
pip install -r requirements.txt
```

Run the server:

```
uvicorn main:app --host 0.0.0.0 --port 8000
```

Running tests:

```
pytest
```