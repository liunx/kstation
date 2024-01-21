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
    FontColor<<trans>> transparent
    BorderThickness<<trans>> 0
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
    border_thickness=1.2,
    background_color="transparent",
):
    return skinparam_component.format(
        type_name=type_name,
        font_size=font_size,
        font_color=font_color,
        border_thickness=border_thickness,
        background_color=background_color,
    )


def create_dir(dir_name):
    pathlib.Path(dir_name).mkdir(parents=True, exist_ok=True)


class Mode(Enum):
    SMALL = 1
    MIDDLE = 2
    LARGE = 3


class Align(Enum):
    LEFT = 1
    CENTER = 2
    RIGHT = 3


class Base:
    name = "base"
    vertical = True  # or horizontal
    mode = Mode.SMALL
    align = Align.CENTER
    skin_params = [
        "font_size",
        "font_color",
        "bg_color",
        "border_color",
        "border_thickness",
    ]

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

    def create(self, data, layout) -> str:
        raise NotImplementedError

    def skinparam(self):
        pass

    def component(self, font_color="Black"):
        if self.mode == Mode.SMALL:
            return skinparam(
                type_name="Component",
                font_color=font_color,
                font_size=20,
                border_thickness=1.5,
            )
        elif self.mode == Mode.MIDDLE:
            return skinparam(
                type_name="Component",
                font_color=font_color,
                font_size=40,
                border_thickness=2,
            )
        elif self.mode == Mode.LARGE:
            return skinparam(
                type_name="Component",
                font_color=font_color,
                font_size=200,
                border_thickness=10,
            )
        else:
            raise ValueError

    def hexagon(self):
        if self.mode == Mode.SMALL:
            return skinparam(type_name="Hexagon", font_size=20, border_thickness=1.5)
        elif self.mode == Mode.MIDDLE:
            return skinparam(type_name="Hexagon", font_size=40, border_thickness=2)
        elif self.mode == Mode.LARGE:
            return skinparam(
                type_name="Hexagon",
                font_size=200,
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
                border_thickness=0,
            )
        else:
            raise ValueError

    def node(self):
        pass

    def database(self):
        if self.mode == Mode.SMALL:
            return skinparam(type_name="Database", font_size=20, border_thickness=1.5)
        elif self.mode == Mode.MIDDLE:
            return skinparam(type_name="Database", font_size=40, border_thickness=2)
        elif self.mode == Mode.LARGE:
            return skinparam(
                type_name="Database",
                font_size=200,
                border_thickness=10,
            )
        else:
            raise TypeError

    def arrow(self):
        if self.mode == Mode.SMALL:
            return "skinparam ArrowThickness 1.5\n"
        elif self.mode == Mode.MIDDLE:
            return "skinparam ArrowThickness 2\n"
        elif self.mode == Mode.LARGE:
            return "skinparam ArrowThickness 10\n"
        else:
            raise TypeError

    def get_style(self, data):
        _style = ""
        if data in self.box_only:
            _style = "<<box>>"
        elif data in self.text_only:
            _style = "<<text>>"
        elif data in self.trans_only:
            _style = "<<trans>>"
        return _style

    def __create(self, data, layout) -> str:
        s = start_uml
        if not self.vertical:
            s += "left to right direction\n"
        _align = "left"
        if self.align == Align.CENTER:
            _align = "center"
        s += f"skinparam DefaultTextAlignment {_align}\n"

        s += scale_ratio.format(ratio=self.scale)
        s += self.create(data, layout)
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

    def recursive_flow(self, flow, data, tab_count=0):
        s = ""
        _tab = "\t" * tab_count
        for f in flow:
            if isinstance(f, list):
                color = self.get_color(f[0])
                s += _tab + f"""group #{color} "{data[f[0]]}" {{\n"""
                s += self.recursive_flow(f[1:], data, tab_count + 1)
                s += _tab + "}\n"
            else:
                color = self.get_color(f)
                _type = ""
                if f in self.controls:
                    _type = "<<continuous>>"
                s += _tab + f"#{color}:{data[f]};{_type}\n"
        return s

    def register_vars(self, data):
        return

    def _create(self, multi=False):
        _data = self.data.get("data", [])
        if len(_data) == 0:
            return
        _layout = self.data.get("layout", [i for i in range(len(_data))])

        self.color_map = self.data.get("color_map", [0] * len(_data))
        self.text_only = self.data.get("text_only", [])
        self.box_only = self.data.get("box_only", [])
        self.trans_only = self.data.get("trans_only", [])
        name = self.data.get("name", f"{self.name}{self.index}")
        self.data_name = self.data.get("name")
        rewrite = self.data.get("rewrite", True)
        self.tail = self.data.get("tail", False)
        self.controls = self.data.get("controls", [])
        self.label = self.data.get("label", None)
        self.vertical = self.data.get("vertical", True)
        self.dashed = self.data.get("dashed", False)
        self.register_vars(self.data)
        if not multi:
            if self.check_file_exists(name) and not rewrite:
                return
            s = self.__create(_data, _layout)
            if len(s) > 0:
                self.write(name, s)
        else:
            for i in range(len(_layout)):
                _name = f"{name}{i}"
                if self.check_file_exists(_name) and not rewrite:
                    continue
                s = self.__create(_data, _layout[i])
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

    def register_vars(self, data):
        self.interval = data.get("interval", [])

    def create(self, data, layout) -> str:
        s = ""
        s += self.component()
        s += self.arrow()
        s += "' components:\n"
        i = 0
        for d in data:
            style = self.get_style(i)
            color = self.get_color(i)
            s += f"""component "{d}" as c{i} {style} #{color}\n"""
            i += 1
        s += "' layout:\n"
        dot = "-"
        if self.dashed:
            dot = "."
        # connect
        for conn in layout:
            _from = conn[0]
            _to = conn[1:]
            for i in _to:
                s += f"c{_from}-{dot*2}>c{i}\n"
        # intervals
        i = 0
        for l in self.interval:
            _from = l[0]
            _to = l[1]
            gaps = "\\n" * l[2]
            s += f"""component "tag{i}{gaps}" as gp{i}\n"""
            s += f"c{_from}-right[hidden]-gp{i}\n"
            s += f"gp{i}-right[hidden]-c{_to}\n"
            s += f"hide gp{i}\n"
            i += 1
        return s


class Blocks(Base):
    name = "blocks"
    mode = Mode.LARGE

    @staticmethod
    def single_type_only(list_, type_) -> bool:
        if len(list_) == 0:
            return False
        for l in list_:
            if not isinstance(l, type_):
                return False
        return True

    def recursive_layout(self, layout, data, tab_count=0, vertical=True) -> str:
        s = ""
        tab = "\t" * tab_count
        # title:[1,2,3,...]
        if (
            len(layout) == 2
            and isinstance(layout[0], int)
            and isinstance(layout[1], list)
        ):
            color = self.get_color(layout[0])
            _style = self.get_style(layout[0])
            s += (
                tab
                + f"""component "{data[layout[0]]}" as cp{self.recursive_i} {_style} #{color} {{\n"""
            )
            self.recursive_i += 1
            s += self.recursive_layout(layout[1], data, tab_count + 1, vertical)
            s += tab + "}\n"
        else:
            names = []
            for _layout in layout:
                if isinstance(_layout, list):
                    name = f"rect{self.recursive_i}"
                    self.recursive_i += 1
                    names.append(name)
                    s += tab + f"""rectangle {name} {{\n"""
                    s += self.recursive_layout(
                        _layout, data, tab_count + 1, (not vertical)
                    )
                    s += tab + "}\n"
                elif isinstance(_layout, int):
                    color = self.get_color(_layout)
                    name = f"cp{self.recursive_i}"
                    self.recursive_i += 1
                    names.append(name)
                    _style = self.get_style(_layout)
                    s += (
                        tab
                        + f"""component "{data[_layout]}" as {name} {_style} #{color}\n"""
                    )
                else:
                    raise TypeError
            # layout
            i = 0
            direct = "right"
            if vertical:
                direct = "down"
            if self.single_type_only(layout, int):
                direct = "right"
            while True:
                if i >= len(names) - 1:
                    break
                s += tab + f"{names[i]}-{direct}[hidden]-{names[i+1]}\n"
                i += 1
        return s

    def create(self, data, layout) -> str:
        s = ""
        s += self.component()
        s += self.rectangle()
        self.recursive_i = 0
        s += self.recursive_layout(layout, data)
        return s


class Tables(Base):
    name = "tables"
    mode = Mode.LARGE

    def create(self, data) -> str:
        s = ""
        s += self.component()
        s += self.package()
        if self.label:
            s += f"""component "{self.label}" as pk <<text>> {{\n"""
            s += "\tcomponent cp [\n"
            s += data + "\n"
            s += "\t]\n"
            s += "}\n"
        else:
            s += "component cp [\n"
            s += data + "\n"
            s += "]\n"
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
        s += self.recursive_flow(self.layout, data)
        if self.tail:
            s += ":return;<<hide>>\n"
        return s


class Lists(Base):
    name = "lists"
    mode = Mode.MIDDLE
    vertical = False

    def register_vars(self, data):
        self.vertical = False
        self.interval = data.get("interval", 1)
        self.hide_line = data.get("hide_line", False)

    def create(self, data, layout) -> str:
        s = ""
        s += self.component()
        if self.hide_line:
            s += "skinparam ArrowThickness 0\n"
        else:
            s += skinparam(type_name="Interface", font_size=0, border_thickness=0)
            s += self.arrow()
        i = 0
        s += "' components:\n"
        dots = []
        for l in layout:
            if l < 0:
                s += f"interface c{i}\n"
                dots.append(abs(l) * self.interval)
                i += 1
                continue
            color = self.get_color(l)
            dots.append(self.interval)
            _type = ""
            if l in self.box_only:
                _type = "<<box>>"
            s += f"""component "{data[l]}" as c{i} {_type} #{color}\n"""
            i += 1
        s += "' layout:\n"
        i = 0
        dot = "."
        while True:
            if i >= len(layout) - 1:
                break
            s += f"c{i}-down{dot * dots[i+1]}c{i+1}\n"
            i += 1
        return s


class TextBoxes(Base):
    name = "textboxes"
    mode = Mode.LARGE

    def register_vars(self, data):
        pass

    def create(self, data, layout) -> str:
        s = ""
        s += "skinparam RoundCorner 100\n"
        s += self.component()
        text = data[layout]
        color = self.get_color(layout)
        s += f"""component "  {text}  " as cp #{color}\n"""
        return s


class Texts(Base):
    name = "texts"
    mode = Mode.LARGE

    def create(self, data, layout) -> str:
        s = ""
        color = self.get_color(layout)
        s += self.component(font_color=color)
        text = data[layout]
        s += f"""component "{text}" as cp <<text>>\n"""
        return s


class Experiments(Base):
    name = "experiments"
    mode = Mode.LARGE

    def component(self, **args) -> str:
        s = "skinparam Component {\n"
        # configs
        s += f'''\tFontSize {args.get("font_size", 20)}\n'''
        s += f'''\tFontColor {args.get("font_color", "black")}\n'''
        s += f'''\tBackgroundColor {args.get("bg_color", "transparent")}\n'''
        s += f'''\tBorderThickness {args.get("bd_thickness", 1.5)}\n'''
        # trans_only
        s += "\tFontColor<<trans>> transparent\n"
        s += "\tBorderThickness<<trans>> 0\n"
        # text_only
        s += "\tBorderThickness<<text>> 0\n"
        s += "\tBackgroundColor<<text>> transparent\n"
        # box_only
        s += "\tFontColor<<box>> transparent\n"
        s += "}\n"
        return s

    def rectangle(self, **args):
        s = "skinparam Rectangle {\n"
        # configs
        s += "\tFontSize 0\n"
        s += "\tFontColor transparent\n"
        s += "\tBorderThickness 1.5\n"
        s += "\tBackgroundColor transparent\n"
        # align
        s += f'''\tFontSize<<align>> {args.get("font_size", 20)}\n'''
        s += f'''\tBorderThickness<<align>> {args.get("bd_thickness", 1.5)}\n'''
        s += "}\n"
        return s

    def get_align_size(self, data):
        return "m" * max([len(i) for i in data]) * 8

    def create(self, data, layout) -> str:
        s = ""
        s += self.component(font_size=20, bd_thickness=0)
        s += self.rectangle(font_size=2, bd_thickness=1)
        _align = self.get_align_size(data)
        i = 0
        for l in layout:
            _text = data[l]
            s += f'''rectangle "{_align}" as r{i} <<align>> {{\n'''
            s += f'''\tcomponent c{i} [\n'''
            s += f"\t\t{_text}\n"
            s += "\t]\n"
            s += "}\n"
            i += 1
            j = 0
        i = 0
        while True:
            if i >= len(layout) - 1:
                break
            s += f"r{i}-down-->r{i+1}\n"
            i += 1
        return s


default_colors = ["transparent"]


def main(data):
    global color_list
    color_list = data.get("color_list", default_colors)
    Colors.process(data)
    Trees.process(data)
    Blocks.process(data)
    Tables.process(data)
    Flows.process(data)
    Lists.process(data, multi=True)
    TextBoxes.process(data, multi=True)
    Texts.process(data, multi=True)
    Experiments.process(data)


if __name__ == "__main__":
    with open("config.toml", "rb") as f:
        data = tomllib.load(f)
        main(data)
