#!/usr/bin/env python3
import sys
import os.path
import pathlib
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


def create_functions(functions, color_map, interval, data):
    global color_list
    s = start_uml
    s += scale_ratio.format(ratio="1/1")
    s += skinparam(type_name="Component", font_size=40, border_thickness=1.5)
    color = "transparent"
    s += "' components:\n"
    i = 0
    for fun in functions:
        if len(color_map) > 0:
            color = color_list[color_map[fun]]
            name = data[fun]
            s += f"""component "{name}" as c{i} #{color}\n"""
        else:
            s += f"""component "{name}" as c{i} #{color}\n"""
        i += 1
    s += "' layout:\n"
    i = 0
    while True:
        if i >= len(functions) - 1:
            break
        dots = "-" * interval
        s += f"c{i}-down[hidden]{dots}c{i+1}\n"
        i += 1
    s += end_uml
    return s


def process_functions(data):
    _data = data.get("data", [])
    if len(_data) == 0:
        return
    rewrite = data.get("rewrite", True)
    interval = data.get("interval", 2)
    groups = data.get("groups", [])
    color_map = data.get("color_map", [])
    i = 0
    fname = "functions{}"
    if len(groups) > 0:
        for grp in groups:
            if check_file_exists(fname.format(i)) and not rewrite:
                continue
            s = create_functions(grp, color_map, interval, _data)
            write_plantuml(fname.format(i), s)
            i += 1
    else:
        for i in range(len(_data)):
            if check_file_exists(fname.format(i)) and not rewrite:
                continue
            s = create_functions([i], color_map, interval, _data)
            write_plantuml(fname.format(i), s)


def _create_1d_table(data, color_map):
    global color_list
    s = ""
    compo_i = 0
    s += "' component:\n"
    for dat in data:
        color = "transparent"
        if len(color_map) > 0:
            color = color_list[color_map[compo_i]]
        text = f"{dat}"
        if dat == "OMIT":
            s += f"""rectangle "\\no\\no\\no\\n" as c{compo_i} #{color}\n"""
        else:
            s += f"""component "{text}" as c{compo_i} #{color}\n"""
        compo_i += 1
    s += "' layout:\n"
    i = 0
    while True:
        if i >= len(data) - 1:
            break
        s += f"c{i}-down[hidden]-c{i+1}\n"
        i += 1
    return s


def _create_2d_table(data, color_map):
    global color_list
    s = ""
    pack_i = 0
    for dat in data:
        pack_name = f"p{pack_i}"
        s += "card {} {{\n".format(pack_name)
        compo_i = 0
        # components
        s += "\t' components\n"
        for d in dat:
            if d == "BLANK":
                s += f"""\trectangle "blank" as {pack_name}_c{compo_i} #transparent\n"""
                compo_i += 1
                continue
            text = f"{d}"
            if len(color_map) > 0:
                color = color_list[color_map[pack_i][compo_i]]
                s += f"""\tcomponent "{text}" as {pack_name}_c{compo_i} #{color}\n"""
            else:
                s += (
                    f"""\tcomponent "{text}" as {pack_name}_c{compo_i} #transparent\n"""
                )
            compo_i += 1
        # layout
        s += "\t' layout\n"
        if len(dat) > 1:
            i = 0
            while True:
                if i >= len(dat) - 1:
                    break
                s += f"\t{pack_name}_c{i}-right[hidden]-{pack_name}_c{i+1}\n"
                i += 1
        s += "}\n\n"
        pack_i += 1
    # layout
    if len(data) > 1:
        i = 0
        while True:
            if i >= len(data) - 1:
                break
            s += f"p{i}-down[hidden]-p{i+1}\n"
            i += 1

    return s


def write_plantuml(name, s, dir_name="."):
    filename = f"{dir_name}/{name}.plantuml"
    with open(filename, "w+") as f:
        f.write(s)


def write_file(filename, s):
    with open(filename, "w+") as f:
        f.write(s)


def _create_table(data, color_map):
    if isinstance(data, list) and isinstance(data[0], list):
        return _create_2d_table(data, color_map)
    else:
        return _create_1d_table(data, color_map)


def create_table(table):
    s = start_uml
    s += scale_ratio.format(ratio="1/5")
    s += skinparam(type_name="Component", font_size=200, border_thickness=10)
    s += skinparam(type_name="Card", font_size=0, border_thickness=0)
    s += skinparam(type_name="Package", font_size=200, border_thickness=0)
    s += skinparam(
        type_name="Rectangle",
        font_size=200,
        font_color="black",
        border_thickness=0,
    )
    color_map = []
    if "color_map" in table:
        color_map = table["color_map"]
    if "name" in table:
        s += f"""package "{table['name']}" as pack_name {{\n"""
    if "data" in table:
        s += _create_table(table["data"], color_map)
    if "name" in table:
        s += "}\n"
    s += end_uml
    return s


def process_tables(tables):
    font_size = 200
    ratio = "1/5"
    align = "CENTER"
    if "data" in tables:
        for k, v in tables["data"].items():
            s = create_table(v)
            write_plantuml(k, s)


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


def create_tree(_list, color_map, connect_list):
    global color_list
    s = start_uml
    s += scale_ratio.format(ratio="2/1")
    s += skinparam(type_name="Component", font_size=20, border_thickness=1.2)
    i = 0
    color = "transparent"
    s += "' components:\n"
    for l in _list:
        if len(color_map) > 0:
            color = color_list[color_map[i]]
            s += f"""component "{l}" as c{i} #{color}\n"""
        else:
            s += f"""component "{l}" as c{i} #{color}\n"""
        i += 1
    if len(connect_list) > 0:
        s += "' layout:\n"
        for conn in connect_list:
            _from = conn[0]
            _to = conn[1:]
            for i in _to:
                s += f"c{_from}-->c{i}\n"
    s += end_uml
    return s


def process_trees(data):
    rewrite = True
    if "rewrite" in data:
        rewrite = data["rewrite"]
    if "data" in data:
        for k, v in data["data"].items():
            fname = f"{k}.plantuml"
            if os.path.exists(fname) and not rewrite:
                continue
            color_map = []
            if "color_map" in v:
                color_map = v["color_map"]
            connect_list = []
            if "connect_list" in v:
                connect_list = v["connect_list"]
            s = create_tree(v["data"], color_map, connect_list)
            write_file(fname, s)


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
    flow = data.get("control_flow", [i for i in range(len(_data))])
    color_map = data.get("color_map", [0] * len(_data))
    s = start_uml
    s += scale_ratio.format(ratio="2/1")
    s += skinparam(type_name="Activity", font_size=20, border_thickness=1.2)
    s += "skinparam ActivityFontColor<<hide>> transparent\n"
    s += "skinparam ActivityBorderThickness<<hide>> 0\n"
    s += skinparam(type_name="Note", font_size=16, border_thickness=0)
    s += skinparam(type_name="Arrow", font_size=16, border_thickness=1.2)
    s += "' start here\n"
    s += recursive_flow(flow, _data, color_map)
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


def _create_block(data):
    global color_list
    _data = data.get("data", [])
    if len(_data) == 0:
        return ""
    color_map = data.get("color_map", [0] * len(_data))
    layout = data.get("layout", [i for i in range(len(_data))])
    s = start_uml
    s += scale_ratio.format(ratio="1/5")
    s += skinparam(
        type_name="Component", font_size=200, round_corner=100, border_thickness=10
    )
    s += skinparam(type_name="Rectangle", font_size=0, border_thickness=0)
    s += skinparam(type_name="Package", font_size=200, border_thickness=0)
    i = 0
    for l in layout:
        if isinstance(l, list):
            rname = f"r{i}"
            s += f"rectangle {rname} {{\n"
            j = 0
            for _l in l:
                text = _data[_l]
                color = color_list[color_map[_l]]
                s += f"""\tcomponent "{text}" as {rname}_c{j} #{color}\n"""
                j += 1
            # layout
            j = 0
            while True:
                if j >= len(l) - 1:
                    break
                s += f"\t{rname}_c{j}-right[hidden]-{rname}_c{j+1}\n"
                j += 1
            s += "}\n"
        else:
            text = _data[l]
            color = color_list[color_map[l]]
            s += f"""\tcomponent "{text}" as r{i} #{color}\n"""
        i += 1
    # layout
    i = 0
    while True:
        if i >= len(layout) - 1:
            break
        s += f"r{i}-down[hidden]-r{i+1}\n"
        i += 1
    s += end_uml
    return s


def create_block(data, i):
    name = data.get("name", f"block{i}")
    rewrite = data.get("rewrite", True)
    if check_file_exists(name, dir_name="blocks") and not rewrite:
        return
    s = _create_block(data)
    if len(s) > 0:
        write_plantuml(name, s, dir_name="blocks")


def process_blocks(data):
    create_dir("blocks")
    for i in range(len(data)):
        create_block(data[i], i)


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


class Base:
    name = "base"

    def __init__(self, data, index, color_list) -> None:
        self.data = data
        self.index = index
        self.color_list = color_list

    def _create(self, data) -> str:
        return ""

    def check_file_exists(self, name):
        return os.path.exists(f"{self.name}/{name}.plantuml")

    def write(self, name, s):
        filename = f"{self.name}/{name}.plantuml"
        with open(filename, "w+") as f:
            f.write(s)

    def create(self, multi=False):
        _data = self.data.get("data", [])
        if len(_data) == 0:
            return
        self.color_map = self.data.get("color_map", [0] * len(_data))
        self.layout = self.data.get("layout", [i for i in range(len(_data))])
        name = self.data.get("name", f"{self.name}{self.index}")
        rewrite = self.data.get("rewrite", True)
        if not multi:
            if self.check_file_exists(name) and not rewrite:
                return
            s = self._create(_data)
            if len(s) > 0:
                self.write(name, s)
        else:
            for i in range(len(_data)):
                _name = f"{name}{i}"
                if self.check_file_exists(_name) and not rewrite:
                    continue
                s = self._create(_data[i])
                if len(s) > 0:
                    self.write(_name, s)

    @classmethod
    def process(cls, data, multi=False):
        color_list = data.get("color_list", default_colors)
        if cls.name in data:
            create_dir(cls.name)
            _data = data.get(cls.name)
            for i in range(len(_data)):
                cls(_data[i], i, color_list).create(multi=multi)


class Test(Base):
    name = "tests"

    def _create(self, data) -> str:
        print(data)
        return ''


default_colors = ["transparent"]


def main(data):
    global color_list
    color_list = data.get("color_list", default_colors)
    if "functions" in data:
        process_functions(data["functions"])
    if "tables" in data:
        process_tables(data["tables"])
    if "texts" in data:
        process_texts(data["texts"])
    if "lists" in data:
        process_lists(data["lists"])
    if "trees" in data:
        process_trees(data["trees"])
    if "flows" in data:
        process_flows(data["flows"])
    if "blocks" in data:
        process_blocks(data["blocks"])
    if "textboxes" in data:
        process_textboxes(data["textboxes"])

    Test.process(data)


if __name__ == "__main__":
    with open("config.toml", "rb") as f:
        data = tomllib.load(f)
        main(data)
