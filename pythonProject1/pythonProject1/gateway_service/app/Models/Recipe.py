from dataclasses import dataclass
from typing import Any, TypeVar, Callable, Set, List, Type

T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int))
    return float(x)


def from_set(f: Callable[[Any], T], x: Any) -> Set[T]:
    assert isinstance(x, list)
    return {f(y) for y in x}


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return x.to_dict()

def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    """
    Преобразует список данных в список объектов типа T, применяя функцию f для каждого элемента.
    """
    assert isinstance(x, list)
    return [f(y) for y in x]

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
