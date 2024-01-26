#!/usr/bin/env python3
import pathlib
import os.path
from PIL import Image, ImageDraw, ImageFont
import tomli as tomllib

ttf_path = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"


def create_dir(dir_name):
    pathlib.Path(dir_name).mkdir(parents=True, exist_ok=True)


class Base:
    name = "base"

    def __init__(self, data, index, color_list) -> None:
        self.data = data
        self.index = index
        self.color_list = color_list

    def draw_block(
        self,
        text,
        bg_color="white",
        font_size=20,
        font_color="black",
        border_color="black",
        border_thickness=1,
        padding=100,
        width=0,
        height=0,
        alpha=200,
    ):
        ttf = ImageFont.truetype(ttf_path, font_size)
        left, top, right, bottom = ttf.getbbox(text)
        _, descent = ttf.getmetrics()
        w = right - left + padding
        if w < width:
            w = width
        h = bottom - top + descent
        if h < height:
            h = height
        img = Image.new("RGB", (w, h), color=bg_color)
        img.putalpha(alpha)
        img_draw = ImageDraw.Draw(img)
        img_draw.text((w // 2, h // 2), text, anchor="mm", font=ttf, fill=font_color)
        img_draw.rectangle(
            (0, 0, w - 1, h - 1),
            fill=None,
            outline=border_color,
            width=border_thickness,
        )

        return img

    @classmethod
    def process(cls, data, multi=False):
        color_list = data.get("color_list", ["transparent"])
        if cls.name in data:
            create_dir(cls.name)
            _data = data.get(cls.name)
            for i in range(len(_data)):
                cls(_data[i], i, color_list)._create(multi=multi)

    def register_vars(self, data):
        raise NotImplementedError

    def create(self, data, layout):
        raise NotImplementedError

    def check_file_exists(self, name):
        return os.path.exists(f"{self.name}/{name}.png")

    def write(self, name, img):
        img.save(f"{self.name}/{name}.png")

    def get_color(self, i):
        return self.color_list[self.color_map[i]]

    def _create(self, multi=False):
        _data = self.data.get("data", [])
        if len(_data) == 0:
            return
        layout = self.data.get("layout", [i for i in range(len(_data))])
        name = self.data.get("name", f"{self.name}{self.index}")
        self.color_map = self.data.get("color_map", [0] * len(_data))
        rewrite = self.data.get("rewrite", True)
        self.register_vars(self.data)
        if not multi:
            if self.check_file_exists(name) and not rewrite:
                return
            img = self.create(_data, layout)
            self.write(name, img)
        else:
            for i in range(len(layout)):
                _name = f"{name}{i}"
                if self.check_file_exists(_name) and not rewrite:
                    continue
                img = self.create(_data, layout[i])
                self.write(_name, img)


class Blocks(Base):
    name = "blocks"
    font_size = 40
    border_thickness = 1

    def register_vars(self, data):
        self.height_map = data.get("height_map", [1] * len(data.get("data")))

    def do_layout(self, data, layout):
        x = 0
        y = 0
        self.raw_data = []
        for l in layout:
            if isinstance(l, list):
                # find max align width
                w_max = 0
                for _l in l:
                    w, _ = self.rendered_sizes[_l]
                    if w_max < w:
                        w_max = w
                # collect x, y, w, h
                _x = x
                _y = y
                for _l in l:
                    w, h = self.rendered_sizes[_l]
                    text = data[_l]
                    color = self.get_color(_l)
                    height = self.height_map[_l]
                    h = h * height
                    self.raw_data.append([text, color, _x, _y, w_max, h])
                    _y += h
                x += w_max
            elif isinstance(l, int):
                w, h = self.rendered_sizes[l]
                text = data[l]
                color = self.get_color(l)
                height = self.height_map[l]
                h = h * height
                self.raw_data.append([text, color, x, y, w, h])
                x += w
            else:
                raise TypeError

    def eval_rendered_sizes(self, data):
        self.rendered_sizes = []
        for text in data:
            img = self.draw_block(
                text,
                font_size=self.font_size,
                height=self.font_size * 2,
                border_thickness=self.border_thickness,
            )
            self.rendered_sizes.append(img.size)

    def get_render_size(self):
        x, y, w, h = (0, 0, 0, 0)
        for data in self.raw_data:
            if x <= data[2]:
                x = data[2]
                w = data[4]
            if y <= data[3]:
                y = data[3]
                h = data[5]
        return (x + w, y + h)

    def render_data(self, size):
        w, h = size
        img = Image.new("RGB", (w, h), color="white")
        img.putalpha(0)
        for data in self.raw_data:
            text, color, _w, _h = (data[0], data[1], data[4], data[5])
            _img = self.draw_block(
                text,
                bg_color=color,
                font_size=self.font_size,
                border_thickness=self.border_thickness,
                width=_w,
                height=_h,
            )
            img.paste(_img, (data[2], data[3]))
        return img

    def create(self, data, layout):
        self.eval_rendered_sizes(data)
        self.do_layout(data, layout)
        render_size = self.get_render_size()
        return self.render_data(render_size)


def main(data):
    Blocks.process(data)


if __name__ == "__main__":
    with open("config.toml", "rb") as f:
        data = tomllib.load(f)
        main(data)
