FROM python:3.9-slim-bullseye AS requirements
RUN adduser --system --no-create-home nonroot

RUN apt-get update \
    && python -m pip install --upgrade pip \
    && apt-get -y install libpq-dev gcc curl procps net-tools tini \
    && apt-get -y clean \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /ip-camera-mock

RUN curl -L https://github.com/bluenviron/mediamtx/releases/download/v1.4.2/mediamtx_v1.4.2_linux_amd64.tar.gz > mediamtx_v1.4.2_linux_amd64.tar.gz
RUN tar -xvzf mediamtx_v1.4.2_linux_amd64.tar.gz

# Install third-party libraries
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Run the API with a Nonroot user
USER nonroot
CMD python main.py
