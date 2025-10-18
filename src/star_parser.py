from pathlib import Path
import zipfile
import re


def build_star_data(line_data: str):
    pattern = "".join([
        r"^\s*(\d+)\s+",
        r"(\d+:\d+:\d+\.?\d*)\s+",
        r"([+-]\d+:\d+:\d+)\s+",
        r"([+-]?\d+\.\d+)\s+",
        r"([+-]?\d+\.\d+)\s+",
        r"([VWASD ]*)\s*",
        r"([+-]?\d+\.\d+)\s+",
        r"([A-Z0-9\.\+:\-\* ]+?)\s+",
        r"([+-]\d+\.\d+)\s+",
        r"([+-]\d+\.\d+)"
    ])
    match = re.match(pattern, line_data.strip())
    if not match:
        return None

    try:
        star_data = {
            "longitude": match.group(2),
            "latitude": match.group(3),
            "galactic_lon": float(match.group(4)),
            "galactic_lat": float(match.group(5)),
            "flags": match.group(6).strip(),
            "magnitude": float(match.group(7)),
            "spectral_class": match.group(8).strip(),
            "move_longitude": float(match.group(9)),
            "move_latitude": float(match.group(10))
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
                    new_star = build_star_data(line.decode("utf-8"))
                    if new_star is not None:
                        stars.append(new_star)
    return stars
