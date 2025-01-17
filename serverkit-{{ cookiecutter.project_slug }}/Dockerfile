FROM mallorywittwerepfl/imaging-server-kit:latest

ARG PYTHON_VERSION={{ cookiecutter.python_version }}
RUN conda install python=$PYTHON_VERSION -y

COPY . .

RUN python -m pip install -r requirements.txt
