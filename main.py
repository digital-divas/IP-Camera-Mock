import dotenv
import subprocess

dotenv.load_dotenv()

import logging
import time
import os
import time

import av

from animation import Animation

if os.path.isfile("./mediamtx"):
    subprocess.Popen(["./mediamtx"])

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

fps = int(os.getenv("CAMERA_FPS", "15"))
output_stream = os.getenv("ADDRESS", "rtsp://localhost:8554/live")
width = int(os.getenv("CAMERA_WIDTH", "480"))
height = int(os.getenv("CAMERA_HEIGHT", "320"))
# You can also use h264
codec_name = os.getenv("CODEC_NAME", "hevc")

while True:
    format = "rtsp"

    if output_stream.split(":")[0] == "rtmp":
        format = "flv"
        # 'flv' format does not support 'hevc' codec for this version of ffmpeg
        # TODO: maybe build a custom ffmpeg or install a plugin so it can support hevc over flv?
        codec_name = "h264"

    container = av.open(output_stream, mode="w", format=format)
    stream = container.add_stream(rate=fps, codec_name=codec_name)
    stream.width = width
    stream.height = height
    custom_video = Animation(fps, stream)

    while True:
        pix = custom_video.loop()

        frame = av.VideoFrame.from_ndarray(pix, format="rgb24")

        for packet in stream.encode(frame):
            container.mux(packet)
