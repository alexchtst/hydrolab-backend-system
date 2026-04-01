import json
import math
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

with open(DATA_DIR / "infogrid.json") as f:
    grid_meta = json.load(f)

with open(DATA_DIR / "metadata.json") as f:
    all_data = json.load(f)

with open(DATA_DIR / "spliteddata.json") as f:
    splited_data = json.load(f)

with open(DATA_DIR / "pairingdata.json") as f:
    pairing_raw = json.load(f)


def get_all_data():
    return all_data

def get_paginated_data(page: int, limit: int):
    total = len(all_data)
    total_pages = math.ceil(total / limit)

    start = (page - 1) * limit
    end = start + limit

    return {
        "data": all_data[start:end],
        "total": total,
        "totalPages": total_pages,
    }
    
def get_data_by_id(station_id):
    for item in all_data:
        if item["Station_ID"] == station_id:
            return item
    return None

def get_cell_index(lat, lon):
    row = math.floor(
        (lat - grid_meta["lat_start"]) / grid_meta["lat_step"]
    )

    col = math.floor(
        (lon - grid_meta["lon_start"]) / grid_meta["lon_step"]
    )

    return row, col

def get_area_id(lat, lon):
    row, col = get_cell_index(lat, lon)

    if (
        row < 0
        or row >= grid_meta["lat_count"]
        or col < 0
        or col >= grid_meta["lon_count"]
    ):
        return None

    area_id = row * grid_meta["lon_count"] + col + 1
    return f"Area_{area_id}"

def get_neighbor_areas(lat, lon, radius=1):
    row, col = get_cell_index(lat, lon)
    result = []

    for dr in range(-radius, radius + 1):
        for dc in range(-radius, radius + 1):
            r = row + dr
            c = col + dc

            if (
                0 <= r < grid_meta["lat_count"]
                and 0 <= c < grid_meta["lon_count"]
            ):
                area_id = r * grid_meta["lon_count"] + c + 1
                result.append(f"Area_{area_id}")

    return result

def haversine(lat1, lon1, lat2, lon2):
    R = 6371

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )

    return R * 2 * math.asin(math.sqrt(a))

def search_nearest(lat, lon, radius_km=1):

    CELL_LAT_KM = 10
    CELL_LON_KM = 5

    cell_radius_lat = math.ceil(radius_km / CELL_LAT_KM)
    cell_radius_lon = math.ceil(radius_km / CELL_LON_KM)

    cell_radius = max(cell_radius_lat, cell_radius_lon)

    areas = get_neighbor_areas(lat, lon, cell_radius)

    candidates = []

    for area in areas:
        data = splited_data.get(area, [])
        candidates.extend(data)

    results = []

    for item in candidates:
        dist = haversine(
            lat,
            lon,
            item["latitude"],
            item["longitude"],
        )

        if dist <= radius_km:
            item_copy = dict(item)
            item_copy["distance"] = dist
            results.append(item_copy)

    results.sort(key=lambda x: x["distance"])

    return results

def get_pairing_data_by_id(id: str):
    data = [i for i in pairing_raw if i["Station_ID"] == int(id)]
    return data