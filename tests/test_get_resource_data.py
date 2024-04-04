import httpx
from jsonschema import validate
from core.contracts import RESOURCE_DATA_SCHEMA

BASE_URL = "https://reqres.in/api/unknown"
SINGLE_RESOURCE = "/2"
COLOR_BEGINNING = "#"
PER_PAGE = 6
RESOURCE_NOT_FOUND = "/23"


def test_list_resource():
    response = httpx.get(BASE_URL)
    assert response.status_code == 200

    resource_data = response.json()["data"]
    for item in resource_data:
        validate(item, RESOURCE_DATA_SCHEMA)
        assert item["id"] >= 1 and item["id"] <= PER_PAGE  # проверка id
        assert item["year"] >= 2000  # проверка year
        assert item["color"].startswith(COLOR_BEGINNING)  # проверка color


def test_single_resource():
    response = httpx.get(BASE_URL + SINGLE_RESOURCE)
    assert response.status_code == 200

    resource_data = response.json()["data"]
    validate(resource_data, RESOURCE_DATA_SCHEMA)
    assert resource_data["id"] >= 1 and resource_data["id"] <= PER_PAGE  # проверка id
    assert resource_data["year"] >= 2000  # проверка year
    assert resource_data["color"].startswith(COLOR_BEGINNING)  # проверка color


def test_resource_not_found():
    response = httpx.get(BASE_URL + RESOURCE_NOT_FOUND)
    assert response.status_code == 404