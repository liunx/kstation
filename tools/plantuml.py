#!/usr/bin/env python3
import sys
import os.path
import tomli as tomllib

start_uml = """@startuml\n
skinparam ComponentStyle rectangle
"""
end_uml = "\n@enduml\n"
scale_ratio = "scale {ratio}\n"

skinparam_component = """
skinparam {type_name} {{
    FontSize {font_size}
    FontColor {font_color}
    BorderThickness {border_thickness}
    BackgroundColor {background_color}
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


def create_function_component(name, ratio="2/1", fsize=20, bg="Orange", bt=1.2):
    filename = "{}.plantuml".format(name)
    with open(filename, "w+") as f:
        s = start_uml
        s += scale_ratio.format(ratio=ratio)
        s += skinparam(font_size=fsize, background_color=bg, border_thickness=bt)
        s += f"[  {name}()  ]\n"
        s += end_uml
        f.write(s)


def process_functions(data):
    font_size = data["font_size"]
    ratio = data["ratio"]
    bt = data["border_thickness"]
    for k, v in data["bg_color"].items():
        for i in v:
            create_function_component(i, ratio=ratio, fsize=font_size, bg=k, bt=bt)


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


def write_plantuml(name, s):
    filename = f"{name}.plantuml"
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


def create_text(text, color):
    s = start_uml
    s += scale_ratio.format(ratio="1/5")
    s += skinparam(type_name="Component", font_size=200, border_thickness=0)
    s += f"""component "{text}" as cp #{color}\n"""
    s += end_uml
    return s


def process_texts(data):
    global color_list
    color_map = []
    color = 'transparent'
    if "color_map" in data:
        color_map = data['color_map']
    if "data" in data:
        i = 0
        for l in data["data"]:
            if len(color_map) > 0:
                color = color_list[color_map[i]]
            s = create_text(l, color)
            fname = f"text{i}"
            write_plantuml(fname, s)
            i += 1


def create_list(_list, color_map):
    global color_list
    s = start_uml
    s += "left to right direction\n"
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
    s += "' layout:\n"
    i = 0
    while True:
        if i >= len(_list) - 1:
            break
        s += f"c{i}-down.c{i+1}\n"
        i += 1
    s += end_uml
    return s


def process_lists(lists):
    if "data" in lists:
        for k, v in lists["data"].items():
            color_map = []
            if "color_map" in v:
                color_map = v["color_map"]
            s = create_list(v["data"], color_map)
            write_plantuml(k, s)


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


def main(data):
    global color_list
    if "color_list" in data:
        color_list = data["color_list"]
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


if __name__ == "__main__":
    with open("config.toml", "rb") as f:
        data = tomllib.load(f)
        main(data)
