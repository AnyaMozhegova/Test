from dataclasses import dataclass
from typing import Set, Any
from utils.serialization import from_int, from_str, from_float, from_set

@dataclass
class Recipe:
    id: int  # Уникальный идентификатор рецепта
    name: str  # Название рецепта
    description: str  # Описание рецепта
    ingredients: str  # Ингредиенты рецепта в виде строки
    calories: float  # Количество калорий в рецепте
    tags: Set[str]  # Набор тегов, описывающих рецепт

    @staticmethod
    def from_dict(obj: Any) -> 'Recipe':
        """
        Статический метод для создания экземпляра Recipe из словаря.
        Проверяет тип входного объекта и конвертирует его в соответствующие типы.
        """
        if isinstance(obj, Recipe):
            obj = obj.to_dict()  # Преобразование экземпляра Recipe в словарь
        if not isinstance(obj, dict):
            raise ValueError(f"Expected dict, got {type(obj)}. Received object: {obj}")

        # Извлечение и валидация данных из словаря
        id = from_int(obj.get("id"))
        name = from_str(obj.get("name"))
        description = from_str(obj.get("description"))
        ingredients = from_str(obj.get("ingredients"))
        calories = from_float(obj.get("calories"))
        tags = from_set(from_str, obj.get("tags"))

        return Recipe(id, name, description, ingredients, calories, tags)

    def to_dict(self) -> dict:
        """
        Метод для преобразования экземпляра Recipe в словарь.
        """
        return {
            "id": from_int(self.id),  # Преобразование id в целое число
            "name": from_str(self.name),  # Преобразование имени в строку
            "description": from_str(self.description),  # Преобразование описания в строку
            "ingredients": from_str(self.ingredients),  # Преобразование ингредиентов в строку
            "calories": from_float(self.calories),  # Преобразование калорий в число с плавающей точкой
            "tags": list(self.tags),  # Преобразование набора тегов в список
        }
