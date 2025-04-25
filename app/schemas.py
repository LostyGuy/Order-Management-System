from pydantic import BaseModel

class OrdersBase(BaseModel):
    order_id: int
    table_id: int
    positions: list[str]
    quantity: list[int]
    order_status: str

class MenuBase(BaseModel):
    menu_id: int
    position_name: str
    required_ingredients: list[str]
    course_cost: float

class IngridientsBase(BaseModel):
    ingredient_id: int
    ingredient_name: str
    quantity: list[int]
    ingredient_type: str

class Loyalty_CardsBase(BaseModel):
    guest_id: int
    name: str
    surname: str
    phone_number: int
    discount: float

class TransactionsBase(BaseModel):
    transaction_id: int
    order_id: int
    course_names: list[str]
    guest_id: int
    total_cost: float