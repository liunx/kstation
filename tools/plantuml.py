#!/usr/bin/env python3
import os.path
import pathlib
from enum import Enum
import tomli as tomllib

start_uml = """@startuml\n
skinparam ComponentStyle rectangle
hide stereotype
"""
end_uml = "\n@enduml\n"
scale_ratio = "scale {ratio}\n"

skinparam_component = """
skinparam {type_name} {{
    FontSize {font_size}
    FontColor {font_color}
    RoundCorner {round_corner}
    BorderThickness {border_thickness}
    BackgroundColor {background_color}
    BorderThickness<<text>> 0
    BackgroundColor<<text>> transparent
    FontColor<<box>> transparent
}}\n
"""

color_list = []


def skinparam(
    type_name="Component",
    font_size=20,
    font_color="black",
    round_corner=10,
    border_thickness=1.2,
    background_color="transparent",
):
    return skinparam_component.format(
        type_name=type_name,
        font_size=font_size,
        font_color=font_color,
        round_corner=round_corner,
        border_thickness=border_thickness,
        background_color=background_color,
    )


def check_file_exists(fname, dir_name="."):
    return os.path.exists(f"{dir_name}/{fname}.plantuml")


def create_dir(dir_name):
    pathlib.Path(dir_name).mkdir(parents=True, exist_ok=True)


def write_plantuml(name, s, dir_name="."):
    filename = f"{dir_name}/{name}.plantuml"
    with open(filename, "w+") as f:
        f.write(s)


def write_file(filename, s):
    with open(filename, "w+") as f:
        f.write(s)


def _create_text(text, color):
    s = start_uml
    s += scale_ratio.format(ratio="1/5")
    s += skinparam(
        type_name="Component",
        font_size=200,
        font_color=color,
        border_thickness=0,
    )
    s += f"""component cp [\n"""
    s += f"{text}\n"
    s += "]"
    s += end_uml
    return s


def create_texts(data):
    global color_list
    _data = data.get("data", [])
    if len(_data) == 0:
        return
    name = data.get("name", "text")
    rewrite = data.get("rewrite", True)
    color_map = data.get("color_map", [0] * len(_data))
    for i in range(len(_data)):
        fname = f"{name}{i}"
        color = color_list[color_map[i]]
        if check_file_exists(fname, dir_name="texts") and not rewrite:
            return
        s = _create_text(_data[i], color)
        if len(s) > 0:
            write_plantuml(fname, s, dir_name="texts")


def process_texts(data):
    create_dir("texts")
    for d in data:
        create_texts(d)


def recursive_flow(flow, data, color_map, tab_count=0):
    global color_list
    s = ""
    _tab = "\t" * tab_count
    for f in flow:
        if isinstance(f, list):
            color = color_list[color_map[f[0]]]
            s += _tab + f"""group #{color} "{data[f[0]]}" {{\n"""
            s += recursive_flow(f[1:], data, color_map, tab_count + 1)
            s += _tab + "}\n"
        else:
            color = color_list[color_map[f]]
            s += _tab + f"#{color}:{data[f]};\n"
    return s


def _create_flow(data):
    _data = data.get("data", [])
    if len(_data) == 0:
        return ""
    flow = data.get("layout", [i for i in range(len(_data))])
    color_map = data.get("color_map", [0] * len(_data))
    tail = data.get("tail", False)
    s = start_uml
    s += scale_ratio.format(ratio="2/1")
    s += skinparam(type_name="Activity", font_size=20, border_thickness=1.2)
    s += "skinparam ActivityFontColor<<hide>> transparent\n"
    s += "skinparam ActivityBorderThickness<<hide>> 0\n"
    s += skinparam(type_name="Note", font_size=16, border_thickness=0)
    s += skinparam(type_name="Arrow", font_size=16, border_thickness=1.2)
    s += "' start here\n"
    s += recursive_flow(flow, _data, color_map)
    if tail:
        s += ":return;<<hide>>\n"
    s += end_uml
    return s


def create_flow(data, i):
    name = data.get("name", f"flow{i}")
    rewrite = data.get("rewrite", True)
    if check_file_exists(name, dir_name="flows") and not rewrite:
        return
    s = _create_flow(data)
    if len(s) > 0:
        write_plantuml(name, s, dir_name="flows")


def process_flows(data):
    create_dir("flows")
    for i in range(len(data)):
        create_flow(data[i], i)


def create_textbox(text, color):
    s = start_uml
    s += scale_ratio.format(ratio="1/5")
    s += "skinparam RoundCorner 100\n"
    s += skinparam(
        type_name="Component",
        font_size=200,
        border_thickness=10,
        background_color=color,
    )
    s += f"""component "{text}" as cp\n"""
    s += end_uml

    return s


def create_textboxes(data, i):
    global color_list
    _data = data.get("data", [])
    if len(_data) == 0:
        return
    color_map = data.get("color_map", [0] * len(_data))
    name = data.get("name", "textbox")
    rewrite = data.get("rewrite", True)
    for i in range(len(_data)):
        fname = f"{name}{i}"
        color = color_list[color_map[i]]
        if check_file_exists(fname, dir_name="textboxes") and not rewrite:
            continue
        s = create_textbox(_data[i], color)
        if len(s) > 0:
            write_plantuml(fname, s, dir_name="textboxes")


def process_textboxes(data):
    create_dir("textboxes")
    for i in range(len(data)):
        create_textboxes(data[i], i)


def _create_list(data):
    global color_list
    _data = data.get("data", [])
    if len(_data) == 0:
        return ""
    color_map = data.get("color_map", [0] * len(_data))
    interval = data.get("interval", 1)
    hide_line = data.get("hide_line", False)
    layout = data.get("layout", [i for i in range(len(_data))])
    s = start_uml
    s += "left to right direction\n"
    s += scale_ratio.format(ratio="1/1")
    s += skinparam(type_name="Component", font_size=40, border_thickness=2)
    if hide_line is False:
        s += skinparam(type_name="Interface", font_size=0, border_thickness=0)
        s += "skinparam ArrowThickness 2\n"
    else:
        s += "skinparam ArrowThickness 0\n"
    i = 0
    s += "' components:\n"
    if hide_line is False:
        s += f"""interface "o" as head\n"""
    for l in layout:
        color = color_list[color_map[l]]
        s += f"""component "{_data[l]}" as c{i} #{color}\n"""
        i += 1
    if hide_line is False:
        s += f"""interface "o" as tail\n"""
    s += "' layout:\n"
    i = 0
    dots = "." * interval
    if hide_line is False:
        s += f"head-down{dots}c{i}\n"
    while True:
        if i >= len(layout) - 1:
            break
        s += f"c{i}-down{dots}c{i+1}\n"
        i += 1
    if hide_line is False:
        s += f"c{i}-down{dots}tail\n"
    s += end_uml
    return s


def create_list(data, i):
    name = data.get("name", f"list{i}")
    rewrite = data.get("rewrite", True)
    if check_file_exists(name, dir_name="lists") and not rewrite:
        return
    s = _create_list(data)
    if len(s) > 0:
        write_plantuml(name, s, dir_name="lists")


def process_lists(data):
    create_dir("lists")
    for i in range(len(data)):
        create_list(data[i], i)


class Mode(Enum):
    SMALL = 1
    MIDDLE = 2
    LARGE = 3


class Base:
    name = "base"
    vertical = True  # or horizontal
    mode = Mode.SMALL

    def __init__(self, data, index, color_list) -> None:
        self.data = data
        self.index = index
        self.color_list = color_list
        if self.mode == Mode.SMALL:
            self.scale = "2/1"
        elif self.mode == Mode.MIDDLE:
            self.scale = "1/1"
        elif self.mode == Mode.LARGE:
            self.scale = "1/5"

    def create(self, data) -> str:
        raise NotImplementedError

    def component(self):
        if self.mode == Mode.SMALL:
            return skinparam(type_name="Component", font_size=20, border_thickness=1.2)
        elif self.mode == Mode.MIDDLE:
            return skinparam(type_name="Component", font_size=40, border_thickness=2)
        elif self.mode == Mode.LARGE:
            return skinparam(
                type_name="Component",
                font_size=200,
                round_corner=10,
                border_thickness=10,
            )
        else:
            raise ValueError

    def hexagon(self):
        if self.mode == Mode.SMALL:
            return skinparam(type_name="Hexagon", font_size=20, border_thickness=1.2)
        elif self.mode == Mode.MIDDLE:
            return skinparam(type_name="Hexagon", font_size=40, border_thickness=2)
        elif self.mode == Mode.LARGE:
            return skinparam(
                type_name="Hexagon",
                font_size=200,
                round_corner=10,
                border_thickness=10,
            )
        else:
            raise ValueError

    def rectangle(self):
        return skinparam(type_name="Rectangle", font_size=0, border_thickness=0)

    def package(self):
        if self.mode == Mode.SMALL:
            return skinparam(type_name="Package", font_size=20, border_thickness=0)
        elif self.mode == Mode.MIDDLE:
            return skinparam(type_name="Package", font_size=40, border_thickness=0)
        elif self.mode == Mode.LARGE:
            return skinparam(
                type_name="Package",
                font_size=200,
                round_corner=10,
                border_thickness=0,
            )
        else:
            raise ValueError

    def node(self):
        pass

    def database(self):
        if self.mode == Mode.SMALL:
            return skinparam(type_name="Database", font_size=20, border_thickness=1.2)
        elif self.mode == Mode.MIDDLE:
            return skinparam(type_name="Database", font_size=40, border_thickness=2)
        elif self.mode == Mode.LARGE:
            return skinparam(
                type_name="Database",
                font_size=200,
                round_corner=100,
                border_thickness=10,
            )
        else:
            raise ValueError

    def arrow(self):
        pass

    def __create(self, data) -> str:
        s = start_uml
        if not self.vertical:
            s += "left to right direction\n"
        s += scale_ratio.format(ratio=self.scale)
        s += self.create(data)
        s += end_uml
        return s

    def check_file_exists(self, name):
        return os.path.exists(f"{self.name}/{name}.plantuml")

    def write(self, name, s):
        filename = f"{self.name}/{name}.plantuml"
        with open(filename, "w+") as f:
            f.write(s)

    def get_color(self, i):
        return self.color_list[self.color_map[i]]

    def create_layout_block(self, name, color, text, _type, tab) -> str:
        s = ""
        s += "\t" * tab + f"""component "{text}" as {name}{_type} #{color}\n"""
        return s

    def create_layout(self, _data):
        s = ""
        i = 0
        for l in self.layout:
            rname = f"r{i}"
            if isinstance(l, list):
                s += f"rectangle {rname} {{\n"
                j = 0
                for _l in l:
                    text = _data[_l]
                    color = self.get_color(_l)
                    _name = f"r{i}_{j}"
                    _type = ""
                    if _l in self.box_only:
                        _type = "<<box>>"
                    elif _l in self.text_only:
                        _type = "<<text>>"
                    tab = 1
                    s += self.create_layout_block(_name, color, text, _type, tab)
                    j += 1
                # layout
                j = 0
                while True:
                    if j >= len(l) - 1:
                        break
                    s += f"\t{rname}_{j}-right[hidden]-{rname}_{j+1}\n"
                    j += 1
                s += "}\n"
            else:
                text = _data[l]
                color = self.get_color(l)
                _name = f"r{i}"
                _type = ""
                if l in self.box_only:
                    _type = "<<box>>"
                elif l in self.text_only:
                    _type = "<<text>>"
                tab = 0
                s += self.create_layout_block(_name, color, text, _type, tab)
            i += 1
        # layout
        i = 0
        while True:
            if i >= len(self.layout) - 1:
                break
            s += f"r{i}-down[hidden]-r{i+1}\n"
            i += 1
        return s

    def recursive_flow(self, data, tab_count=0):
        s = ""
        _tab = "\t" * tab_count
        for f in self.layout:
            if isinstance(f, list):
                color = self.get_color(f[0])
                s += _tab + f"""group #{color} "{data[f[0]]}" {{\n"""
                s += recursive_flow(f[1:], data, tab_count + 1)
                s += _tab + "}\n"
            else:
                color = self.get_color(f)
                _type = ""
                if f in self.controls:
                    _type = "<<continuous>>"
                s += _tab + f"#{color}:{data[f]};{_type}\n"
        return s

    def _create(self, multi=False):
        _data = self.data.get("data", [])
        if len(_data) == 0:
            return
        self.color_map = self.data.get("color_map", [0] * len(_data))
        self.layout = self.data.get("layout", [i for i in range(len(_data))])
        self.text_only = self.data.get("text_only", [])
        self.box_only = self.data.get("box_only", [])
        name = self.data.get("name", f"{self.name}{self.index}")
        self.data_name = self.data.get("name")
        rewrite = self.data.get("rewrite", True)
        self.tail = self.data.get("tail", False)
        self.controls = self.data.get("controls", [])
        if not multi:
            if self.check_file_exists(name) and not rewrite:
                return
            s = self.__create(_data)
            if len(s) > 0:
                self.write(name, s)
        else:
            for i in range(len(_data)):
                _name = f"{name}{i}"
                if self.check_file_exists(_name) and not rewrite:
                    continue
                s = self.__create(_data[i])
                if len(s) > 0:
                    self.write(_name, s)

    @classmethod
    def process(cls, data, multi=False):
        color_list = data.get("color_list", default_colors)
        if cls.name in data:
            create_dir(cls.name)
            _data = data.get(cls.name)
            for i in range(len(_data)):
                cls(_data[i], i, color_list)._create(multi=multi)


class Colors(Base):
    name = "colors"
    mode = Mode.LARGE

    def create_color_label(self, l, idx, text, i, tabcount=0):
        s = ""
        _tab = "\t" * tabcount
        color = self.get_color(l)
        _name = f"{idx}_r{i}"
        s += _tab + f"""rectangle {_name} {{\n"""
        s += _tab + f"""\tcomponent "P\\nG" as {_name}_pg<<box>> #{color}\n"""
        s += _tab + f"""\tcomponent "{text}" as {_name}_tx<<text>>\n"""
        s += _tab + f"""\t{_name}_pg-right[hidden]-{_name}_tx\n"""
        s += _tab + "}\n"
        return s

    def create_layout(self, _data):
        s = ""
        i = 0
        for l in self.layout:
            rname = f"r{i}"
            if isinstance(l, list):
                s += f"rectangle {rname} {{\n"
                j = 0
                for _l in l:
                    text = _data[_l]
                    s += self.create_color_label(_l, rname, text, j, 1)
                    j += 1
                # layout
                j = 0
                while True:
                    if j >= len(l) - 1:
                        break
                    s += f"\t{rname}_r{j}-right[hidden]-{rname}_r{j+1}\n"
                    j += 1
                s += "}\n"
            else:
                text = _data[l]
                s += self.create_color_label(l, rname, text, i, 0)
            i += 1
        # layout
        i = 0
        while True:
            if i >= len(self.layout) - 1:
                break
            s += f"r{i}-down[hidden]-r{i+1}\n"
            i += 1
        return s

    def create(self, data) -> str:
        s = ""
        s += self.component()
        s += self.rectangle()
        s += self.create_layout(data)

        return s


class Trees(Base):
    name = "trees"
    mode = Mode.SMALL

    def create(self, data) -> str:
        s = ""
        s += self.component()
        s += "' components:\n"
        i = 0
        for d in data:
            color = self.get_color(i)
            s += f"""component "{d}" as c{i} #{color}\n"""
            i += 1
        s += "' layout:\n"
        for conn in self.layout:
            _from = conn[0]
            _to = conn[1:]
            for i in _to:
                s += f"c{_from}-->c{i}\n"
        return s


class Blocks(Base):
    name = "blocks"
    mode = Mode.LARGE

    def create(self, data) -> str:
        s = ""
        s += self.component()
        s += self.rectangle()
        s += self.create_layout(data)
        return s


class Tables(Base):
    name = "tables"
    mode = Mode.LARGE

    def create(self, data) -> str:
        s = ""
        s += self.component()
        s += self.rectangle()
        if self.data_name:
            s += self.package()
            s += f"""package "{self.data_name}" as pack {{\n"""
            s += "}\n"
        return s


class Flows(Base):
    name = "flows"
    mode = Mode.SMALL

    def create(self, data) -> str:
        s = ""
        s += skinparam(type_name="Activity", font_size=20, border_thickness=1.2)
        s += "skinparam ActivityFontColor<<hide>> transparent\n"
        s += "skinparam ActivityBorderThickness<<hide>> 0\n"
        s += skinparam(type_name="Note", font_size=16, border_thickness=0)
        s += skinparam(type_name="Arrow", font_size=16, border_thickness=1.2)
        s += "' start here\n"
        s += self.recursive_flow(data)
        if self.tail:
            s += ":return;<<hide>>\n"
        return s


default_colors = ["transparent"]


def main(data):
    global color_list
    color_list = data.get("color_list", default_colors)
    if "texts" in data:
        process_texts(data["texts"])
    if "lists" in data:
        process_lists(data["lists"])
    # if "flows" in data:
    #     process_flows(data["flows"])
    if "textboxes" in data:
        process_textboxes(data["textboxes"])

    Colors.process(data)
    Trees.process(data)
    Blocks.process(data)
    Tables.process(data)
    Flows.process(data)


if __name__ == "__main__":
    with open("config.toml", "rb") as f:
        data = tomllib.load(f)
        main(data)
