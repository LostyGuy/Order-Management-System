# Restaurant Order Management System (SQL Project)

This project simulates a real-world restaurant system using SQL. It includes core database design, business logic (stored procedures and triggers), and reporting views.

## Features

- Store and manage customers, menu items, and orders
- Track inventory and ingredient usage
- Automate logic with triggers and stored procedures
- Generate useful reports (top-selling items, low stock, etc.)

---

## Database Schema

### Tables

- **Customers** – Stores customer details  
  - **Loyalty Card Id**
  - **Name**
  - **Surname**
  - **Phone Number**
  - **Discount**
  - **Date Of Creation**
  - **Modified At**
  - **Status** - Active/Inactive
- **Menu_Items** – Menu of available dishes  
  - **Dish Name**
  - **Ingridient 1#**
  - **Quantity Of 1#**

  - **Ingridient 2#**
  - **Quantity Of 2#**

  - **Ingridient 3#**
  - **Quantity Of 3#**

  - **Ingridient ...#**
  - **Quantity Of ...#**

  - **Status** - If avaiable in current offer
- **Orders** – Order headers with customer and timestamp
  - **Table Id** 
  - **Ordered Dishes**
  - **Quantity**
  - **Date**
  - **Status**
  - **Enough Ingridients**
- **Order_Items** – Order details: which items and how many 
  - **Table Id** 
  - **Ordered Dishes**
  - **Quantity**
- **Inventory** – Tracks ingredients in stock
  - **Ingridient 1#**
  - **Quantity Of 1#**

  - **Ingridient 2#**
  - **Quantity Of 2#**

  - **Ingridient 3#**
  - **Quantity Of 3#**

  - **Ingridient ...#**
  - **Quantity Of ...#**
- **Recipe** – Maps menu items to required ingredients
  - **Dish Name**
  - **Ingridient 1#**
  - **Ingridient 2#**
  - **Ingridient 3#**

---

## Key SQL Concepts

### Stored Procedures
- `sp_PlaceOrder(customer_id, item_id, quantity)` – Places a new order and links order items
- `sp_RestockIngredient(ingredient_id, quantity)` – Restocks ingredients
- `sp_GenerateSalesReport(date)` – Shows sales data for a given day

### Triggers
- `trg_deduct_stock` – Automatically deducts ingredients when an item is added to an order

### Views
- `vw_specifiedOrder` - Shows details of order with given id
- `vw_TopSellingItems` – Shows top-selling dishes
- `vw_InventoryStatus` – Shows ingredient stock levels and alerts

---

## Event Processing

- **To be visualized using Graphviz library**

---
  
## Tech Stack

- SQL (MySQL)
- FastAPI / Python backend (future extension)
- Optional: Simple HTML/JS frontend 

---
