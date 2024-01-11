# IP-Camera-Mock

![Generic badge](https://img.shields.io/badge/python-3.9.1-blue)

## Setup environment

To develop and test on your local environment, we highly recommend to use [pyenv](https://github.com/pyenv/pyenv) with [virtualenv](https://github.com/pyenv/pyenv-virtualenv) extension to manage the project python versions. Currently the latest one that we are using is the `3.9.1`.

### Downloading Python 3.9.1

To install the python version that we use on the project, simply run the code below on your terminal:

```bash
pyenv install 3.9.1
```

After the download is complete, you can check if the python version was downloaded successfully if the version 3.8.3 appears after running the following command:

```bash
pyenv versions
```

Finally, create the virtualenv for this project:

```bash
pyenv virtualenv 3.9.1 IP-Camera-Mock
```

### Using the virtualenv

By default the project already have a `.python-version` file that will automatically change your version, if you are using VS Code. But if you are using another IDE to run and execute your code, you can activate your environment by just using the following command:

```bash
pyenv activate IP-Camera-Mock
```

### How to build?

```sh
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## How to Run?

You'll need to have a RTSP server running on background. I recommend using MediaMTX. You can use it via docker like this:

```sh
docker run --rm -it --network=host bluenviron/mediamtx:latest
```

Once you have the docker running, you can run the application using:

```sh
python main.py
```

To test it just use the variable configured on `ADDRESS` (default value `rtsp://localhost:8554/live`) on your player of choice.

```sh
ffplay rtsp://localhost:8554/live
# VLC should work too
```

## Next steps

- [ ] build an docker image that generates the RTSP immediately.
Something like `docker run -e optional_env_name=env_value -p 8554:8554 -p 8890:8890/udp -p 8189:8189/udp IP-Camera-Mock`.
To achieve that we could try to extend MediaMTX image or get an empty python image and install MediaMtx on it (MediaMTX provides an standalone binary as described on [their README](https://github.com/bluenviron/mediamtx#standalone-binary) ).
Try to use maybe systemctl to have both MediaMTX and the python script running at the same time.
- [ ] generate an mock for ONVIF showing some response to the stream screen
- [ ] configure fake detections of vehicle plates
- [ ] configure fake detections of people's face
