from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session, relationship
from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime, func, or_
from app import schemas, models, database
import logging as log
import time as t
from datetime import datetime as dt
from collections import Counter

log.basicConfig(level='INFO',
                filemode='a',
                filename='app/main_log.log',
                force=True)
log.getLogger("watchfiles.main").setLevel(log.WARNING)

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/app/BI_reports", StaticFiles(directory="app/BI_reports"), name="bi_reports")
templates = Jinja2Templates(directory="templates")

### TODO ---> Loyalty_card system for discounts and Transactions after the order is placed

# Main Page
### TODO ---> Text Wrap || Report - View
### Raport Logic - Power BI
@app.get("/", response_class=HTMLResponse)
async def read_sales(request: Request, db: Session = Depends(database.get_db)): 
    if dt.now().month < 10:
        dt_month = f"0{dt.now().month}"
        log.info(f"Current Month: {dt_month}")
    ### TODO ---> A bit more complex then I thought
    ## Daily Sales [Name from Menu_items, Times Sold from ordered_dishes(count), Revenue (Times Sold * cost From Menu_items)]
    daily_sales_order_id = db.query(models.orders.order_id).filter(
        or_(models.orders.order_status == "active",
            models.orders.order_status == "completed"),
        models.orders.created_at.like(f"{dt.now().year}-{dt_month}%")
        ).all()
    log.info(f"Query Daily Sales: {daily_sales_order_id}")
    daily_sales_

    qms = db.query(models.orders).filter(models.orders.order_status == "completed").limit(10).all()
    return templates.TemplateResponse("default.html", {"request": request, "query_daily_sales": daily_sales_order_id, "query_monthly_sales": ...})

# Order Page - Add Positions Box
@app.get("/add_dish_html", response_class=HTMLResponse)
async def add_dish(request: Request, db: Session = Depends(database.get_db)):
    html_snippet = """
    {%for dish in menu%}
                        <option value="{{ dish.menu_id }}">{{ dish.position_name }}</option>
                        {% endfor %}
    """
    return templates.TemplateResponse("add_dish.html", {"request": request, "html_snippet": html_snippet})

# Order Page
@app.get("/weiter", response_class=HTMLResponse)
async def Weiter_Interface(request: Request, db: Session = Depends(database.get_db)):
    menu = db.query(models.menu).all()
    return templates.TemplateResponse("add_order.html", {"request": request, "menu": menu})

# Order Page - Get Data -> Make Transaction
### TODO ---> Make a func that will restore locked_ingredients to "0" in every cell when the next day come, Transaction making
@app.post("/weiter_p", response_class=HTMLResponse)
async def place_order(request: Request, db: Session = Depends(database.get_db)):
    menu = db.query(models.menu).all()
    form_data = await request.form()
    log.info(f"Form data: {form_data}")
    
    # table_id
    form_data_ti = form_data.get("table_number")
    log.info(f"Table ID: {form_data_ti}")

    def main_order() -> int:
        def disp_id() -> int:
            id: int = db.query(func.max(models.orders.display_id)).scalar()
            log.info(f"Display_id: {id}")
            if id == "None":
                return 1
            else:
                return (id + 1)
        core = models.orders(
            display_id = disp_id(),
            order_status = 'active'
        )
        db.add(core)
        db.commit()
        db.refresh(core)
        main_order_id: int = db.query(models.orders.order_id).filter(models.orders.display_id == core.display_id).order_by(models.orders.created_at.desc()).scalar()
        log.info(f"Main order ID: {main_order_id}")
        return main_order_id

    # ---> combined positions and quantity <---
    def get_pos_qti(form_data) -> list[int]:
        log.info("________________________________________")
        form_data_pos: list[int] = []
        form_data_qti: list[int] = []
        pos_id: int = 1
        qti_id: int = 1
        for i in form_data.keys():
            if i.endswith('d'):
                form_data_pos.append(form_data.get(i))
                pos_id += 1
            elif i.endswith('q'):
                form_data_qti.append(form_data.get(i))
                qti_id += 1
            elif i.endswith('number'):
                pass
            else:
                break
        return form_data_pos, form_data_qti

    form_data_pos, form_data_qti = get_pos_qti(form_data)
    
    log.info(f"Form data positions: {form_data_pos, form_data_qti}")

    ### TODO ---> loop for every pos and add sub order for main order
    def sub_orders(main_order_id, dish, dish_qti) -> None:
        for order in dish:
            log.info(f"sub_order: {order}")
            order_index:int = dish.index(order)
            qti_of_sub_order:int = dish_qti[order_index]
            sub_order_db = models.ordered_dishes(
                order_id = main_order_id,
                dish_id = order,
                quantity = qti_of_sub_order
                )
            db.add(sub_order_db)
            db.commit()

    def Ingredient_Trigger(main_order_id) -> None:
        list_of_sub_orders: list[int] = db.query(models.ordered_dishes).filter(models.ordered_dishes.order_id == main_order_id).all()
        for sub_order in list_of_sub_orders:
            log.info(f"Trigger sub_order: {sub_order}")
            dish_qti:int = sub_order.quantity
            ### Dish -> Ingredients
            list_of_ingredients: list[int] = db.query(models.dish_ingredients).filter(models.dish_ingredients.dish_id == sub_order.dish_id).all()
            for ingredient in list_of_ingredients:
                req_qti:float = ingredient.quantity_required
                ingredient_id = ingredient.ingredient_id
                stock = db.query(models.ingredients).filter(models.ingredients.ingredient_id == ingredient_id).first()
                stock.quantity = stock.quantity - req_qti
                stock.locked_quantity = stock.locked_quantity + req_qti
                db.commit()

    main_order_id = main_order()
    sub_orders(main_order_id, dish = form_data_pos, dish_qti = form_data_qti)
    Ingredient_Trigger(main_order_id)

    return templates.TemplateResponse("add_order.html", {"request": request, "menu": menu})

# Kitchen Page - View Orders
@app.get("/k_v", response_class=HTMLResponse)
async def kv(request: Request, db: Session = Depends(database.get_db)):
    orders_from_db = db.query(models.orders).filter(models.orders.order_status == "active").all()
    list_of_dishes_with_qti: dict[int, dict[str:int]] = {}
    log.info(f"orders: {orders_from_db}")
    for order in orders_from_db:
        list_of_dishes_with_qti[order.order_id] = {}
        log.info(f"order from list: {order.order_id}")
        dishes_in_order: list[int] = db.query(models.ordered_dishes).filter(models.ordered_dishes.order_id == order.order_id).all()
        log.info(f"dishes_in_order: {dishes_in_order}")
        for spec in dishes_in_order:
            
            dish_id:int = spec.dish_id
            qti:int = spec.quantity
            log.info(f"Dish ID: {dish_id}, Quantity: {qti}")
            dish_name:str = db.query(models.menu.dish_name).filter(models.menu.dish_id == dish_id).scalar()
            log.info(f"Dish Name: {dish_name}")
            list_of_dishes_with_qti[order.order_id][dish_name] = qti
    log.info(f"Full list to pass: {list_of_dishes_with_qti}")
    return templates.TemplateResponse("kitchen_view.html", {"request": request, "kv_order": list_of_dishes_with_qti, "id": 0})

# Kitchen Page - Remove Order
@app.post("/complete/{or_id}", response_class=HTMLResponse)
async def rm_comp_order(or_id: int, request: Request, db: Session = Depends(database.get_db)):
    remove = (db.query(models.orders).filter(models.orders.order_id == or_id).first())
    remove.order_status = "ready"
    db.commit()
    db.refresh(remove)
    log.info(f"Order ID: {or_id} is ready")
    return RedirectResponse(url="/k_v")

# Transaction Page - View Transactions
### TODO ---> Add All
@app.get("/transactions", response_class=HTMLResponse)
async def transactions(request: Request, db: Session = Depends(database.get_db)):
    pass