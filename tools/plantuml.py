#!/usr/bin/env python3
import sys
import tomli as tomllib

start_uml = """@startuml\n
skinparam ComponentStyle rectangle
"""
end_uml = "\n@enduml\n"
scale_ratio = "scale {ratio}\n"

skinparam_component = """
skinparam {type_name} {{
    FontSize {font_size}
    BorderThickness {border_thickness}
    BackgroundColor {background_color}
}}\n
"""


def skinparam(
    type_name="Component",
    font_size=20,
    border_thickness=1.2,
    background_color="transparent",
):
    return skinparam_component.format(
        type_name=type_name,
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


def _create_1d_table(data, color_map):
    s = ""
    compo_i = 0
    s += "' component:\n"
    for dat in data:
        color = "transparent"
        if len(color_map) > 0:
            color = color_map[compo_i]
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
    s = ""
    pack_i = 0
    for dat in data:
        pack_name = f"p{pack_i}"
        s += "package {} {{\n".format(pack_name)
        compo_i = 0
        # components
        s += "\t' components\n"
        for d in dat:
            text = f"{d}"
            if len(color_map) > 0:
                color = color_map[pack_i][compo_i]
                s += f"""\tcomponent "{text}" as {pack_name}_c{compo_i} #{color}\n"""
            else:
                s += f"""\tcomponent "{text}" as {pack_name}_c{compo_i} #transparent\n"""
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


def _create_table(data, color_map):
    if isinstance(data, list) and isinstance(data[0], list):
        return _create_2d_table(data, color_map)
    else:
        return _create_1d_table(data, color_map)


def create_table(table):
    s = start_uml
    s += scale_ratio.format(ratio="1/5")
    s += skinparam(type_name="Component", font_size=200, border_thickness=10)
    s += skinparam(type_name="Package", font_size=0, border_thickness=0)
    s += skinparam(type_name="Rectangle", font_size=200, border_thickness=0)
    color_map = []
    if "color_map" in table:
        color_map = table["color_map"]
    if "data" in table:
        s += _create_table(table["data"], color_map)
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


def create_text(text):
    s = start_uml
    s += scale_ratio.format(ratio="1/5")
    s += skinparam(type_name="Component", font_size=200, border_thickness=0)
    s += f'''component "{text}" as cp\n'''
    s += end_uml
    return s


def process_texts(texts):
    if "data" in texts:
        i = 0
        for l in texts["data"]:
            s = create_text(l)
            fname = f"text{i}"
            write_plantuml(fname, s)
            i += 1


def main(data):
    if "functions" in data:
        process_functions(data["functions"])
    if "tables" in data:
        process_tables(data["tables"])
    if "texts" in data:
        process_texts(data["texts"])


if __name__ == "__main__":
    with open("config.toml", "rb") as f:
        data = tomllib.load(f)
        main(data)
