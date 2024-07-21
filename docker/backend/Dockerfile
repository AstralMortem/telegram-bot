FROM python:3.12
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install poetry

WORKDIR /src

COPY ../../backend/ /src/
RUN poetry install


ENTRYPOINT [ "poetry", "run", "uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]

