from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from bson import ObjectId


class Collections(Enum):
    PRODUCTS = "products"
    USERS = "users"
    CLICKS = "clicks"


class Devices(Enum):
    SMARTPHONE = "Smartphone"
    LAPTOP = "Laptop"
    SMARTWATCH = "Smartwatch"
    TABLET = "Tablet"
    ROUTER = "Router"
    DESKTOP_PC = "Desktop PC"
    SMART_TV = "Smart TV"


@dataclass(slots=True)
class Click:
    user_id: ObjectId
    product_id: ObjectId
    timestamp: datetime
    device: Devices


@dataclass(slots=True)
class Product:
    name: str
    price: float
    _id: ObjectId = field(default_factory=ObjectId)


@dataclass(slots=True)
class User:
    name: str
    _id: ObjectId = field(default_factory=ObjectId)
