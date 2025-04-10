![EPFL Center for Imaging logo](https://imaging.epfl.ch/resources/logo-for-gitlab.svg)
# serverkit-{{ cookiecutter.project_slug }}

Implementation of a web server for [{{ cookiecutter.project_name }}]({{ cookiecutter.project_url }}).

## Installing the algorithm server with `pip`

Install dependencies:

```
pip install -r requirements.txt
```

Run the server:

```
uvicorn main:app --host 0.0.0.0 --port 8000
```

or run `python main.py`. The server will be running on http://localhost:8000.

## Endpoints

A documentation of the endpoints is automatically generated at http://localhost:8000/docs.

**GET endpoints**

- http://localhost:8000/ : Running algorithm message.
- http://localhost:8000/version : Version of the `imaging-server-kit` package.
- http://localhost:8000/{{ cookiecutter.project_slug }}/info : Web page displaying project metadata.
- http://localhost:8000/{{ cookiecutter.project_slug }}/demo : Plotly Dash web demo app.
- http://localhost:8000/{{ cookiecutter.project_slug }}/parameters : Json Schema representation of algorithm parameters.
- http://localhost:8000/{{ cookiecutter.project_slug }}/sample_images : Byte string representation of the sample images.

**POST endpoints**

- http://localhost:8000/{{ cookiecutter.project_slug }}/process : Endpoint to run the algorithm.

## Running the server with `docker-compose`

To build the docker image and run a container for the algorithm server in a single command, use:

```
docker compose up
```

The server will be running on http://localhost:8000.

## Running the server with `docker`

Build the docker image:

```
docker build --build-arg PYTHON_VERSION={{ cookiecutter.python_version }} -t serverkit-{{ cookiecutter.project_slug }} .
```

Run the server in a container:

```
docker run -it --rm -p 8000:8000 serverkit-{{ cookiecutter.project_slug }}:latest
```

The server will be running on http://localhost:8000.

## Running unit tests

The unit tests implemented in the [tests](./tests/) folder can be run using pytest:

```
pytest
```

or directly in a docker container:

```
docker run --rm serverkit-{{ cookiecutter.project_slug }}:latest pytest
```

<!-- ## Sample images provenance -->

<!-- Fill if necessary. -->
