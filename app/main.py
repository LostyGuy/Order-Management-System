from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session, relationship
from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime
from app import schemas, models, database
import logging as log
import time as t

log.basicConfig(level='INFO',
                filemode='a',
                filename='app/main_log.log',
                force=True)
log.getLogger("watchfiles.main").setLevel(log.WARNING)

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="templates")

# Main Page
### TODO ---> Text Wrap || Report - View || Finished Transactions - View Endpoint
@app.get("/", response_class=HTMLResponse)
async def read_sales(request: Request, db: Session = Depends(database.get_db)):
    return templates.TemplateResponse("default.html", {"request": request})

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
    menu = db.query(models.menu).filter(models.menu.position_name != None).all()
    return templates.TemplateResponse("add_order.html", {"request": request, "menu": menu})

# Order Page - Get Data
### TODO ---> Make a func that will restore locked_ingredients to "0" in every cell when the next day come
@app.post("/weiter_p", response_class=HTMLResponse)
async def place_order(request: Request, db: Session = Depends(database.get_db)):
    menu = db.query(models.menu).filter(models.menu.position_name != None).all()
    form_data = await request.form()
    log.info(f"Form data: {form_data}")
    
    # table_id
    form_data_ti = form_data.get("table_number")
    log.info(f"Table ID: {form_data_ti}")
    
    # ---> combined positions and quantity <---
    def get_pos_qti(form_data) -> list[int]:
        log.info("________________________________________")
        form_data_pos: list[int] = []
        form_data_qti: list[int] = []
        pos_id: int = 1
        qti_id: int = 1
        for i in form_data.keys():
            log.info(f"Key: {i}")
            log.info(f"Value: {form_data.get(i)}")
            
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
    
    placed_order = models.orders(
        table_id=form_data_ti,
        positions=",".join(form_data_pos),
        quantity=",".join(form_data_qti),
        order_status="Active"
    )
    db.add(placed_order)
    db.commit()
    
    def Ingredient_Trigger(form_data_pos, form_data_qti, db: Session = Depends(database.get_db)) -> None:
        for dish in form_data_pos:
            # ex. fries
            qti: float = float(form_data_qti[form_data_pos.index(dish)])
            # each ingredient of fries
            for ingredients in db.query(models.menu.required_ingredients).filter(models.menu.menu_id == dish).all():
                # ex. potatoes, oil, salt
                ingredients: list[str] = ingredients[0].split(",")
                qti_ingredient: list[float] = list(map(float, ((db.query(models.menu.quantity).filter(models.menu.menu_id == dish).all())[0])[0].split(",")))
                log.info(f"Ingredient separated: {ingredients}, Quantity: {qti_ingredient}")

                for ingredient in ingredients:
                    # get the quantity of each ingredient and multiply
                    ingredient_index: int = ingredients.index(ingredient)
                    ingredient_quantity: float = qti * qti_ingredient[ingredient_index]
                    log.info(f"Ingridient Index: {ingredient_index}, Ingredient quantity: {ingredient_quantity}, Name: {ingredient}")
                    
                    current_locked_quantity = db.query(models.ingredients.locked_quantity).filter(models.ingredients.ingredient_name == ingredient).all()
                    log.info(f"Current locked quantity: {current_locked_quantity}")
                    
                    current_ingredient_quantity = db.query(models.ingredients.quantity).filter(models.ingredients.ingredient_name == ingredient).all()
                    log.info(f"Current ingredient quantity: {current_ingredient_quantity}")

                    db.query(models.ingredients).filter(models.ingredients.ingredient_name == ingredient).update({"locked_quantity": current_locked_quantity[0][0] + ingredient_quantity})
                    
                    db.query(models.ingredients).filter(models.ingredients.ingredient_name == ingredient).update({"quantity": current_ingredient_quantity[0][0] - ingredient_quantity})
                    
                    db.commit()

    Ingredient_Trigger(form_data_pos, form_data_qti,db)
    db.refresh(placed_order)
    log.info(f"Placed order: {placed_order}")
    return templates.TemplateResponse("add_order.html", {"request": request, "menu": menu})

# Kitchen Page - View Orders
### TODO ---> Complete the Button Functionality
@app.get("/k_v", response_class=HTMLResponse)
async def kv(request: Request, db: Session = Depends(database.get_db)):
    # log.info("________________________________________")
    orders_from_db = db.query(models.orders).filter(models.orders.order_status == "Active").all()

    temp_orders: dict[int,list[str, str]] = {}
    list_of_dishes: dict[int, dict[str, str]] = {}

    for order in orders_from_db: # Single Order
        # log.info(f"order.positions: {order.positions}, order.quantity: {order.quantity}")
        
        order.positions = order.positions.split(",") # More readable
        order.quantity = order.quantity.split(",")

        # replace number with name
        op_iteration = 0
        for operation in order.positions:
            menu = db.query(models.menu.position_name).filter(models.menu.menu_id == operation).all()
            order.positions[op_iteration] = menu[0][0]
            op_iteration += 1
        
        temp_orders[order.order_id] = {
            "positions": order.positions,
            "quantity": order.quantity
        }
        # log.info(f"temp_orders: {temp_orders[order.order_id]}")
        list_of_dishes[order.order_id] = {}
        for i in range(len(temp_orders[order.order_id]["positions"])):
            
            list_of_dishes[order.order_id].update({temp_orders[order.order_id]["positions"][i] : temp_orders[order.order_id]["quantity"][i]})
            
            # log.info(f"list_of_dishes: {list_of_dishes[order.order_id]}")
        # log.info(F"list_of_dishes: {list_of_dishes}")
        
    return templates.TemplateResponse("kitchen_view.html", {"request": request, "kv_order": list_of_dishes, "id": 0})

@app.post("/k_v_b", response_class=HTMLResponse)
async def rm_comp_order(request: Request, db: Session = Depends(database.get_db)):
    
    return RedirectResponse(url="/k_v")