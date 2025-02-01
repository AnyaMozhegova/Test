from dataclasses import dataclass
from typing import Set, Any
from datetime import datetime
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
class UserPreferences:
    id: int
    user_id: int  # Идентификатор пользователя, с которым связаны предпочтения
    budget: float
    dietary_preferences: Set[str]
    allergies: Set[str]
    created_at: datetime

    def __eq__(self, other):
        if not isinstance(other, UserPreferences):
            return False
        return self.user_id == other.user_id and self.created_at == other.created_at

    def __hash__(self):
        return hash((self.user_id, self.created_at))
    @staticmethod
    def from_dict(obj: Any) -> 'UserPreferences':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        user_id = from_int(obj.get("user_id"))
        budget = from_float(obj.get("budget"))
        dietary_preferences = from_set(from_str, obj.get("dietary_preferences"))
        allergies = from_set(from_str, obj.get("allergies"))
        created_at = datetime.fromisoformat(from_str(obj.get("created_at")))
        return UserPreferences(id, user_id, budget, dietary_preferences, allergies, created_at)

    def to_dict(self) -> dict:
        return {
            "id": from_int(self.id),
            "user_id": from_int(self.user_id),
            "budget": from_float(self.budget),
            "dietary_preferences": list(self.dietary_preferences),
            "allergies": list(self.allergies),
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class NewUserPreferences:
    budget: float
    dietary_preferences: Set[str]
    allergies: Set[str]

    @staticmethod
    def from_dict(obj: Any) -> 'NewUserPreferences':
        assert isinstance(obj, dict)
        budget = from_float(obj.get("budget"))
        dietary_preferences = from_set(from_str, obj.get("dietary_preferences"))
        allergies = from_set(from_str, obj.get("allergies"))
        return NewUserPreferences(budget, dietary_preferences, allergies)

    def to_dict(self) -> dict:
        return {
            "budget": from_float(self.budget),
            "dietary_preferences": list(self.dietary_preferences),
            "allergies": list(self.allergies),
        }


def new_user_preferences_from_dict(s: Any) -> NewUserPreferences:
    return NewUserPreferences.from_dict(s)


def new_user_preferences_to_dict(x: NewUserPreferences) -> Any:
    return to_class(NewUserPreferences, x)


@dataclass
class EditUserPreferences:
    budget: float | None = None
    dietary_preferences: Set[str] | None = None
    allergies: Set[str] | None = None

    @staticmethod
    def from_dict(obj: Any) -> 'EditUserPreferences':
        assert isinstance(obj, dict)
        budget = from_float(obj.get("budget"))
        dietary_preferences = from_set(from_str, obj.get("dietary_preferences"))
        allergies = from_set(from_str, obj.get("allergies"))
        return EditUserPreferences(budget, dietary_preferences, allergies)

    def to_dict(self) -> dict:
        return {
            "budget": from_float(self.budget) if self.budget is not None else None,
            "dietary_preferences": list(self.dietary_preferences) if self.dietary_preferences else None,
            "allergies": list(self.allergies) if self.allergies else None,
        }


def edit_user_preferences_from_dict(s: Any) -> EditUserPreferences:
    return EditUserPreferences.from_dict(s)


def edit_user_preferences_to_dict(x: EditUserPreferences) -> Any:
    return to_class(EditUserPreferences, x)
