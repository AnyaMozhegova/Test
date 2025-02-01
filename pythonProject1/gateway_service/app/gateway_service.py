from fastapi import FastAPI, HTTPException
from fastapi.security import HTTPBearer
import httpx
import os

from fastapi import FastAPI, HTTPException
from fastapi.security import HTTPBearer
import httpx
import os

# Импорт моделей из вашего репозитория
from gateway_service.app.Models.User import User, NewUser, EditUser
from gateway_service.app.Models.MenuRecommendation import MenuRecommendation, NewMenuRecommendation, EditMenuRecommendation
from gateway_service.app.Models.Recipe import Recipe
from gateway_service.app.Models.UserPreferences import UserPreferences, EditUserPreferences

app = FastAPI()
bearer_scheme = HTTPBearer()

# Получение URL для взаимодействующих сервисов
USER_SERVICE_URL = str(os.environ.get('USER_SERVICE_URL')) + "/user/"
MENU_SERVICE_URL = str(os.environ.get('MENU_SERVICE_URL')) + "/menu/"
RECIPE_SERVICE_URL = str(os.environ.get('RECIPE_SERVICE_URL')) + "/recipe/"
USER_PREFS_SERVICE_URL = str(os.environ.get('USER_PREFS_SERVICE_URL')) + "/preferences/"


# ----------------------------------- User -----------------------------------

@app.post("/user/", response_model=User, status_code=201)
async def create_user(new_user: NewUser):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{USER_SERVICE_URL}", json=new_user.dict())

        if response.status_code == 409:
            raise HTTPException(status_code=409, detail="Пользователь с таким именем уже существует")

        if response.status_code == 422:
            raise HTTPException(status_code=422, detail="Некорректный запрос")

        return response.json()


@app.get("/user/{user_id}", response_model=User, status_code=200)
async def read_user(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USER_SERVICE_URL}{user_id}")

        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        if response.status_code == 422:
            raise HTTPException(status_code=422, detail="Некорректный запрос")

        return response.json()


@app.put("/user/{user_id}", response_model=User, status_code=200)
async def update_user(user_id: int, edit_user: EditUser):
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{USER_SERVICE_URL}{user_id}", json=edit_user.dict())

        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        if response.status_code == 422:
            raise HTTPException(status_code=422, detail="Некорректный запрос")

        return response.json()


@app.delete("/user/{user_id}", status_code=204)
async def delete_user(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{USER_SERVICE_URL}{user_id}")

        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        if response.status_code == 422:
            raise HTTPException(status_code=422, detail="Некорректный запрос")

        return {}


# ----------------------------------- Menu Recommendation -----------------------------------

@app.post("/menu/", response_model=MenuRecommendation, status_code=201)
async def create_menu(new_menu: NewMenuRecommendation):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{MENU_SERVICE_URL}", json=new_menu.dict())

        if response.status_code == 422:
            raise HTTPException(status_code=422, detail="Некорректный запрос")

        return response.json()


@app.get("/menu/{menu_id}", response_model=MenuRecommendation, status_code=200)
async def read_menu(menu_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{MENU_SERVICE_URL}{menu_id}")

        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Меню не найдено")

        if response.status_code == 422:
            raise HTTPException(status_code=422, detail="Некорректный запрос")

        return response.json()


@app.put("/menu/{menu_id}", response_model=MenuRecommendation, status_code=200)
async def update_menu(menu_id: int, edit_menu: EditMenuRecommendation):
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{MENU_SERVICE_URL}{menu_id}", json=edit_menu.dict())

        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Меню не найдено")

        if response.status_code == 422:
            raise HTTPException(status_code=422, detail="Некорректный запрос")

        return response.json()


@app.delete("/menu/{menu_id}", status_code=204)
async def delete_menu(menu_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{MENU_SERVICE_URL}{menu_id}")

        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Меню не найдено")

        if response.status_code == 422:
            raise HTTPException(status_code=422, detail="Некорректный запрос")

        return {}


# ----------------------------------- Recipe -----------------------------------



# ----------------------------------- User Preferences -----------------------------------

@app.put("/preferences/{user_id}", response_model=UserPreferences, status_code=200)
async def update_user_preferences(user_id: int, preferences: EditUserPreferences):
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{USER_PREFS_SERVICE_URL}{user_id}", json=preferences.dict())

        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        if response.status_code == 422:
            raise HTTPException(status_code=422, detail="Некорректный запрос")

        return response.json()

