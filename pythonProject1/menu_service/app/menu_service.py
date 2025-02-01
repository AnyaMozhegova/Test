from datetime import datetime

from fastapi import FastAPI, HTTPException

from menu_service.app.Models.UserPreferences import UserPreferences, NewUserPreferences,EditUserPreferences
from menu_service.app.Models.MenuRecommendation import MenuRecommendation,NewMenuRecommendation,EditMenuRecommendation
from menu_service.app.Models.Recipe import Recipe

app = FastAPI()

user_database = {}
user_preferences_database = {}
menu_recommendation_database = {}



# MenuRecommendation
@app.post("/menu_recommendation/", response_model=MenuRecommendation, status_code=201)
async def create_menu_recommendation(new_menu: NewMenuRecommendation):
    menu_id = len(menu_recommendation_database) + 1
    # Преобразуем меню и рецепты
    menu_items = [Recipe.from_dict(item) for item in new_menu.menu_items]

    menu = MenuRecommendation(
        id=menu_id,
        generated_at=datetime.now(),
        menu_items=menu_items,
        calories=new_menu.calories,
    )

    menu_recommendation_database[menu_id] = menu

    return menu



@app.get("/menu_recommendation/{menu_id}", response_model=MenuRecommendation, status_code=200)
async def read_menu_recommendation(menu_id: int):
    if menu_id not in menu_recommendation_database:
        raise HTTPException(status_code=404, detail="Рекомендация меню не найдена")

    return menu_recommendation_database[menu_id]


@app.put("/menu_recommendation/{menu_id}", response_model=MenuRecommendation, status_code=200)
async def update_menu_recommendation(menu_id: int, edit_menu: EditMenuRecommendation):
    if menu_id not in menu_recommendation_database:
        raise HTTPException(status_code=404, detail="Рекомендация меню не найдена")

    menu = menu_recommendation_database[menu_id]

    if edit_menu.menu_items is not None:
        menu.menu_items = edit_menu.menu_items
    if edit_menu.calories is not None:
        menu.calories = edit_menu.calories

    return menu


@app.delete("/menu_recommendation/{menu_id}", status_code=204)
async def delete_menu_recommendation(menu_id: int):
    if menu_id not in menu_recommendation_database:
        raise HTTPException(status_code=404, detail="Рекомендация меню не найдена")

    menu_recommendation_database.pop(menu_id)
    return {}



