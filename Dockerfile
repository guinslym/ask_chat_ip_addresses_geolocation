# 
FROM python:3.9 as requirements-stage

LABEL user="Guinsly"
LABEL email="guinsly@scholarsportal.info"
LABEL version="0.4"

# 
WORKDIR /tmp


# 
RUN pip install poetry

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TERM xterm
ENV PYTHONIOENCODING utf-8
ENV TZ "Ameria/Montreal"
# 
COPY ./pyproject.toml ./poetry.lock* /tmp/

# 
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# 
FROM python:3.10.3

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        git \
    && apt-get clean \
    && rm -r /var/lib/apt/lists/*

# 
WORKDIR /code
RUN pip install pytest
RUN pip install pandas
RUN pip install ipinfo
RUN pip install lh3api
# 
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

# 
RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY . .

