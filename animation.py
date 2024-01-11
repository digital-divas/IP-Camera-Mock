import time
from datetime import datetime

import numpy as np
from PIL import Image, ImageFont, ImageDraw


class Animation(object):
    def __init__(self, fps, stream):
        self.necessary_diff = 1 / fps
        self.magic_number = 4 * fps

        self.x_dir = 1
        self.y_dir = 1
        self.x_pos = 0
        self.y_pos = 0
        self.block_size = int(stream.height / 10)
        self.x_velocity = int(stream.width / 100)
        self.y_velocity = int(stream.height / 100)
        self.frame_i = -1
        self.stream = stream
        self.last_frame = time.time()
        self.font = ImageFont.truetype("FreeMono.ttf", int(stream.height / 20))

    def draw_object(self, color, draw):
        shape = [
            ((self.block_size * 0.1) + self.x_pos, 0 + self.y_pos),
            (
                self.block_size - (self.block_size * 0.1) + self.x_pos,
                self.block_size - (self.block_size * 0.1) + self.y_pos,
            ),
        ]
        draw.ellipse(shape, fill=color)

    def loop(self):
        now = time.time()

        diff = now - self.last_frame

        if diff < self.necessary_diff:
            time.sleep(self.necessary_diff - diff)

        self.last_frame = time.time()

        self.frame_i += 1

        if self.frame_i > self.magic_number:
            self.frame_i = 0

        img = np.zeros((self.stream.height, self.stream.width, 3))

        r = 0.5 + 0.5 * np.sin(2 * np.pi * (0 / 3 + self.frame_i / self.magic_number))
        g = 0.5 + 0.5 * np.sin(2 * np.pi * (1 / 3 + self.frame_i / self.magic_number))
        b = 0.5 + 0.5 * np.sin(2 * np.pi * (2 / 3 + self.frame_i / self.magic_number))

        img = np.round(255 * img).astype(np.uint8)
        img = np.clip(img, 0, 255)

        pil_image = Image.fromarray(img)
        draw = ImageDraw.Draw(pil_image)

        if self.x_pos < 0:
            self.x_dir = 1

        if self.block_size + self.x_pos > self.stream.width:
            self.x_dir = -1

        if self.y_pos < 0:
            self.y_dir = 1

        if self.block_size + self.y_pos > self.stream.height:
            self.y_dir = -1

        self.x_pos += self.x_dir * self.x_velocity
        self.y_pos += self.y_dir * self.y_velocity
        self.draw_object((int(255 * r), int(255 * g), int(255 * b)), draw)

        draw.text((0, 0), str(datetime.now())[0:19], (255, 255, 255), font=self.font)

        pix = np.array(pil_image)

        return pix
