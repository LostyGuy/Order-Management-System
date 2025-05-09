from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class ingredients(Base):
    __tablename__ = "ingredients"
    ingredient_id = Column(Integer, primary_key=True, index=True)
    ingredient_name = Column(String(50), index=True)
    quantity = Column(Float, index=True)
    ingredient_type = Column(String(50), index=True)
    locked_quantity = Column(Float, index=True)

class loyalty_cards(Base):
    __tablename__ = "loyalty_cards"
    guest_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    surname = Column(String(50), index=True)
    phone_number = Column(String(15), index=True)
    discount = Column(Integer, index=True)

class menu(Base):
    __tablename__ = "menu"
    menu_id = Column(Integer, primary_key=True, index=True)
    position_name = Column(String(50), index=True)
    quantity = Column(Integer, index=True)
    required_ingredients = Column(String(200), index=True)  # Assuming this is a comma-separated string
    course_cost = Column(Integer, index=True)

class orders(Base):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True, index=True)
    table_id = Column(Integer, index=True)
    positions = Column(String(200), index=True)  # Assuming this is a comma-separated string
    quantity = Column(String(200), index=True)  # Assuming this is a comma-separated string
    order_status = Column(String(50), index=True)

class transactions(Base):
    __tablename__ = "transactions"
    transaction_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, index=True)
    course_names = Column(String(200), index=True)  # Assuming this is a comma-separated string
    guest_id = Column(Integer, index=True)
    total_cost = Column(Integer, index=True)
    created_at = Column(String(50), index=True)  # Assuming this is a date string