from dataclasses import dataclass
from typing import List, Any
from datetime import datetime
from menu_service.app.Models.Recipe import Recipe  # Убедитесь, что путь правильный
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
class MenuRecommendation:
    id: int
    user_id: int
    generated_at: datetime
    menu_items: List[Recipe]  # Используем List вместо Set для объектов Recipe
    calories: float

    def __hash__(self):
        # Hashing based on 'id' to make the object hashable
        return hash((self.id, self.user_id))

    def __eq__(self, other):
        # Compare based on 'id' and 'user_id'
        if isinstance(other, MenuRecommendation):
            return self.id == other.id and self.user_id == other.user_id
        return False
    @staticmethod
    def from_dict(obj: Any) -> 'MenuRecommendation':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        user_id = from_int(obj.get("user_id"))
        generated_at = datetime.fromisoformat(from_str(obj.get("generated_at")))
        # Преобразуем элементы menu_items в объекты Recipe
        menu_items = from_list(Recipe.from_dict, obj.get("menu_items"))
        calories = from_float(obj.get("calories"))
        return MenuRecommendation(id, user_id, generated_at, menu_items, calories)

    def to_dict(self) -> dict:
        return {
            "id": from_int(self.id),
            "user_id": from_int(self.user_id),
            "generated_at": self.generated_at.isoformat(),
            # Преобразуем объекты Recipe обратно в словари
            "menu_items": [recipe.to_dict() for recipe in self.menu_items],
            "calories": from_float(self.calories),
        }


@dataclass
class NewMenuRecommendation:
    menu_items: List[Recipe]  # Используем List вместо Set
    calories: float

    @staticmethod
    def from_dict(obj: Any) -> 'NewMenuRecommendation':
        assert isinstance(obj, dict)
        # Преобразуем элементы menu_items в объекты Recipe
        menu_items = from_list(Recipe.from_dict, obj.get("menu_items"))
        calories = from_float(obj.get("calories"))
        return NewMenuRecommendation(menu_items, calories)

    def to_dict(self) -> dict:
        return {
            # Преобразуем объекты Recipe в словари
            "menu_items": [recipe.to_dict() for recipe in self.menu_items],
            "calories": from_float(self.calories),
        }
def new_menu_recommendation_from_dict(s: Any) -> NewMenuRecommendation:
    return NewMenuRecommendation.from_dict(s)


def new_menu_recommendation_to_dict(x: NewMenuRecommendation) -> Any:
    return to_class(NewMenuRecommendation, x)

@dataclass
class EditMenuRecommendation:
    menu_items: List[Recipe] | None = None  # Используем List вместо Set
    calories: float | None = None

    @staticmethod
    def from_dict(obj: Any) -> 'EditMenuRecommendation':
        assert isinstance(obj, dict)
        # Преобразуем элементы menu_items в объекты Recipe, если они присутствуют
        menu_items = from_list(Recipe.from_dict, obj.get("menu_items")) if obj.get("menu_items") else None
        calories = from_float(obj.get("calories")) if obj.get("calories") is not None else None
        return EditMenuRecommendation(menu_items, calories)

    def to_dict(self) -> dict:
        return {
            # Преобразуем объекты Recipe в словари, если menu_items не пусто
            "menu_items": [recipe.to_dict() for recipe in self.menu_items] if self.menu_items else None,
            "calories": from_float(self.calories) if self.calories is not None else None,
        }
def new_menu_recommendation_from_dict(s: Any) -> NewMenuRecommendation:
    return NewMenuRecommendation.from_dict(s)


def new_menu_recommendation_to_dict(x: NewMenuRecommendation) -> Any:
    return to_class(NewMenuRecommendation, x)



