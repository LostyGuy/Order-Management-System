from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
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

@app.get("/", response_class=HTMLResponse)
async def read_sales(request: Request, db: Session = Depends(database.get_db)):
    return templates.TemplateResponse("default.html", {"request": request})

@app.get("/add_dish_html", response_class=HTMLResponse)
async def add_dish(request: Request, db: Session = Depends(database.get_db)):
    html_snippet = """
    {%for dish in menu%}
                        <option value="{{ dish.menu_id }}">{{ dish.position_name }}</option>
                        {% endfor %}
    """
    return templates.TemplateResponse("add_dish.html", {"request": request, "html_snippet": html_snippet})

@app.get("/weiter", response_class=HTMLResponse)
async def Weiter_Interface(request: Request, db: Session = Depends(database.get_db)):
    menu = db.query(models.menu).filter(models.menu.position_name != None).all()
    return templates.TemplateResponse("add_order.html", {"request": request, "menu": menu})

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
    db.refresh(placed_order)
    log.info(f"Placed order: {placed_order}")
    return templates.TemplateResponse("add_order.html", {"request": request, "menu": menu})

# TODO: pass name of the dish instead of intigers
@app.get("/k_v", response_class=HTMLResponse)
async def kv(request: Request, db: Session = Depends(database.get_db)):
    orders = db.query(models.orders).filter(models.orders.order_status == "Active").all()
    k_orders: dict[int,list[str, str]] = {}
    list_of_dishes = {}
    for order in orders:
        order.positions = order.positions.split(",")
        order.quantity = order.quantity.split(",")
        # log.info(order.positions, order.quantity)
        k_orders[order.order_id] = {
            "positions": order.positions,
            "quantity": order.quantity
        }
        # log.info(k_orders[order.order_id].values())
        kv_order: dict[str,str]= {}
        # log.info(range(len(k_orders[order.order_id]["positions"])))
        
        for i in range(len(k_orders[order.order_id]["positions"])):
            kv_order[k_orders[order.order_id]["positions"][i]] = k_orders[order.order_id]["quantity"][i]
            list_of_dishes[order.order_id] = kv_order
        # log.info(kv_order)
        log.info(list_of_dishes)
        
    return templates.TemplateResponse("kitchen_view.html", {"request": request, "kv_order": list_of_dishes, "id": 0})
