import httpx
from jsonschema import validate
from core.contracts import RESOURCE_DATA_SCHEMA
import allure

BASE_URL = "https://reqres.in/api/unknown"
SINGLE_RESOURCE = "/2"
COLOR_BEGINNING = "#"
PER_PAGE = 6
RESOURCE_NOT_FOUND = "/23"


@allure.suite("Получение различных данных ресурсов")
@allure.title("Получение списка ресурсов")
def test_list_resource():
    with allure.step(f"Отправляем запрос по адресу: {BASE_URL}"):
        response = httpx.get(BASE_URL)
    with allure.step("Проверяем код ответа"):
        assert response.status_code == 200

    resource_data = response.json()["data"]
    for item in resource_data:
        with allure.step(f"Проверяем структуру объекта с id: {item['id']}"):
            validate(item, RESOURCE_DATA_SCHEMA)
            with allure.step(f"Проверяем что id >= 1 или <= {PER_PAGE}"):
                assert item["id"] >= 1 and item["id"] <= PER_PAGE  # проверка id
            with allure.step("Проверяем что year >= 2000"):
                assert item["year"] >= 2000  # проверка year
            with allure.step(f"Проверяем что color начинается с: {COLOR_BEGINNING}"):
                assert item["color"].startswith(COLOR_BEGINNING)  # проверка color


@allure.suite("Получение различных данных ресурсов")
@allure.title("Получение данных по одному ресурсу")
def test_single_resource():
    with allure.step(f"Отправляем запрос по адресу: {BASE_URL + SINGLE_RESOURCE}"):
        response = httpx.get(BASE_URL + SINGLE_RESOURCE)
    with allure.step("Проверяем код ответа"):
        assert response.status_code == 200
    resource_data = response.json()["data"]
    validate(resource_data, RESOURCE_DATA_SCHEMA)
    with allure.step(f"Проверяем что id == 2"):
        assert resource_data["id"] == 2
    with allure.step("Проверяем что year >= 2000"):
        assert resource_data["year"] >= 2000  # проверка year
    with allure.step(f"Проверяем что color начинается с: {COLOR_BEGINNING}"):
        assert resource_data["color"].startswith(COLOR_BEGINNING)  # проверка color


@allure.suite("Получение различных данных ресурсов")
@allure.title("Попытка получить данные по несуществующему ресурсу")
def test_resource_not_found():
    with allure.step(f"Отправляем запрос по адресу: {BASE_URL + RESOURCE_NOT_FOUND}"):
        response = httpx.get(BASE_URL + RESOURCE_NOT_FOUND)
    with allure.step("Проверяем код ответа"):
        assert response.status_code == 404
