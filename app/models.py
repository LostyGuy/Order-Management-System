from sqlalchemy import Column, Integer, String, Float
from app.database import Base

### TODO ---> refactor me with new db

class ingredients(Base):
    __tablename__ = "ingredients"
    ingredient_id = Column(Integer, primary_key=True, index=True)
    ingredient_name = Column(String(50), index=True)
    quantity = Column(Float, index=True)
    unit = Column(String(50), index=True)
    locked_quantity = Column(Float, index=True)

class loyalty_cards(Base):
    __tablename__ = "loyalty_cards"
    guest_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    surname = Column(String(50), index=True)
    phone_number = Column(String(15), index=True)
    discount = Column(Integer, index=True)

class menu(Base):
    __tablename__ = "menu_items"
    dish_id = Column(Integer, primary_key=True, index=True)
    dish_name = Column(String(50), index=True)
    course_cost = Column(Integer, index=True)

class orders(Base):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True, index=True)
    #table_id = Column(Integer, index=True)
    display_id = Column(Integer, index=True)
    order_status = Column(String(50), index=True)
    created_at = Column(String(50), index=True)  # Assuming this is a date string

class ordered_dishes(Base):
    __tablename__ = "ordered_dishes"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, index=True)
    dish_id = Column(Integer, index=True)
    quantity = Column(Integer, index=True)

class transactions(Base):
    __tablename__ = "transactions"
    transaction_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, index=True)
    course_names = Column(String(200), index=True)  # Assuming this is a comma-separated string
    guest_id = Column(Integer, index=True)
    total_cost = Column(Integer, index=True)
    created_at = Column(String(50), index=True)  # Assuming this is a date string