#!/usr/bin/env python3
import sys
import tomli as tomllib

start_uml = "@startuml\n"
end_uml = "@enduml\n"
scale_ratio = "scale {ratio}\n"

skinparam_component = """
skinparam {type_name} {{
    Style {style}
    FontSize {font_size}
    BorderThickness {border_thickness}
    BackgroundColor {background_color}
}}\n
"""


def skinparam(
    type_name="Component",
    style="rectangle",
    font_size=20,
    border_thickness=1.2,
    background_color="transparent",
):
    return skinparam_component.format(
        type_name=type_name,
        style=style,
        font_size=font_size,
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


def _create_1d_table(data):
    s = ""
    compo_i = 0
    s += "\t' component:\n"
    for dat in data:
        text = f"{dat}"
        s += f"""\tcomponent "{text}" as c{compo_i}\n"""
        compo_i += 1
    s += "\t' layout:\n"
    i = 0
    while True:
        if i >= len(data) - 1:
            break
        s += f"\tc{i}-down[hidden]-c{i+1}\n"
        i += 1
    return s


def _create_2d_table(data):
    s = ""
    rect_i = 0
    for dat in data:
        rect_name = f"r{rect_i}"
        s += "rectangle {} {{\n".format(rect_name)
        compo_i = 0
        # components
        s += "\t' components\n"
        for d in dat:
            text = f"{d}"
            s += f"""\tcomponent "{text}" as {rect_name}_c{compo_i}\n"""
            compo_i += 1
        # layout
        s += "\t' layout\n"
        if len(dat) > 1:
            i = 0
            while True:
                if i >= len(dat) - 1:
                    break
                s += f"\t{rect_name}_c{i}-right[hidden]-{rect_name}_c{i+1}\n"
                i += 1
        s += "}\n\n"
        rect_i += 1
    # layout
    if len(data) > 1:
        i = 0
        while True:
            if i >= len(data) - 1:
                break
            s += f"r{i}-down[hidden]-r{i+1}\n"
            i += 1

    return s


def write_plantuml(name, s):
    filename = f"{name}.plantuml"
    with open(filename, "w+") as f:
        f.write(s)


def _create_table(data):
    if isinstance(data, list) and isinstance(data[0], list):
        return _create_2d_table(data)
    else:
        return _create_1d_table(data)

def create_table(table):
    s = start_uml
    s += scale_ratio.format(ratio="1/5")
    s += skinparam(type_name="Component", font_size=200, border_thickness=10)
    s += skinparam(type_name="Rectangle", font_size=0, border_thickness=0)
    if "data" in table:
        s += _create_table(table["data"])
    s += end_uml
    return s


def process_tables(tables):
    font_size = 200
    ratio = "1/5"
    align = "CENTER"
    if "data" in tables:
        for k, v in tables["data"].items():
            # align_table(v)
            s = create_table(v)
            write_plantuml(k, s)


def main(data):
    if "functions" in data:
        process_functions(data["functions"])
    if "tables" in data:
        process_tables(data["tables"])


if __name__ == "__main__":
    with open("config.toml", "rb") as f:
        data = tomllib.load(f)
        main(data)
