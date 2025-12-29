from pathlib import Path
import zipfile
import re
import json


def build_star_data(line_data: str):
    pattern = "".join([
        r"^\s*(\d+)\s+",
        r"(\d+:\s*\d+:\s*\d+\.?\d*)\s+",
        r"([+-]\s*\d+:\s*\d+:\s*\d+)\s+",
        r"([+-]?\d+\.\d+)\s+",
        r"([+-]?\d+\.\d+)\s+",
        r"[IVWASD]*\s+",
        r"([+-]?\d+\.\d+)\s+",
        r"([A-Za-z0-9\.\+:/\-\*\?,\(\) ]+?)\s+",
        r"([+-]?\d+\.\d+)\s+",
        r"([+-]?\d+\.\d+)\s+",
        r"D*\s*\d*\s*",
        r"([+-]\d+)\s+",
        r"(\d+)"
    ])
    match = re.match(pattern, line_data.strip())
    if not match:
        print("---", line_data)
        return None
    try:
        star_data = {
            "id": match.group(11),
            "longitude": match.group(2).replace(" ", ""),
            "latitude": match.group(3).replace(" ", ""),
            "galactic_lon": float(match.group(4).replace(" ", "")),  # Долгота
            "galactic_lat": float(match.group(5).replace(" ", "")),  # Широта
            "magnitude": float(match.group(6).replace(" ", "")),
            "spectral_class": match.group(7).strip(),
            "move_longitude": float(match.group(8).replace(" ", "")),
            "move_latitude": float(match.group(9).replace(" ", ""))
        }

        remaining = line_data[match.end():].replace("( ", "(").strip().split()

        star_name = None
        additional_nums = []
        for el in remaining:
            unsigned_el = (
                el.replace("-", "").replace("+", "").replace(".", "")
            )
            if unsigned_el.isdigit():
                additional_nums.append(float(el) if "." in el else int(el))
            # elif el == '999':
            #     additional_nums.append(None)
            elif star_name is None:
                star_name = el
            else:
                break

        star_data["additional_nums"] = additional_nums
        if star_name is not None:
            star_data["name"] = star_name
        else:
            star_data["name"] = "None"

        return star_data

    except (ValueError, IndexError) as e:
        print(f"Ошибка парсинга строки: {line_data.strip()}")
        print(f"Ошибка: {e}")
        return None


def parse_star_data_from_zip(path: Path) -> list[dict]:
    stars = []
    with zipfile.ZipFile(path, "r") as zip_file:
        for filename in [
            el for el in zip_file.namelist() if el.endswith(".txt")
        ]:
            with zip_file.open(filename) as file:
                for line in file:
                    new_star_data = build_star_data(line.decode("utf-8"))
                    if new_star_data is not None:
                        stars.append(new_star_data)
    return stars


def parse_constellation_data_from_json(path: Path) -> list[dict]:
    with open(path, "r", encoding="utf-8") as file:
        constellations = json.load(file)
    return constellations.values()
