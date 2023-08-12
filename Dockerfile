FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/fitness
COPY requirements.txt ./
RUN pip cache purge
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install "PyYAML>=3.4.1,<6"
RUN pip install -r requirements.txt