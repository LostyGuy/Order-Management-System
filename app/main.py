from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app import schemas, models, database

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_sales(request: Request, db: Session = Depends(database.get_db)):
    # sales = db.query(models.Sale).all()
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
async def UI(request: Request, db: Session = Depends(database.get_db)):
    menu = db.query(models.menu).filter(models.menu.position_name != None).all()
    return templates.TemplateResponse("add_order.html", {"request": request, "menu": menu})

@app.post("/weiter", response_class=HTMLResponse)
async def UI_add(request: Request, db: Session = Depends(database.get_db)):
    form_data = await request.form()
    # Process the form data and save it to the database
    # For example, you can create a new Sale object and add it to the session
    # sale = models.Sale(**form_data)
    # db.add(sale)
    # db.commit()
    return templates.TemplateResponse("add_order.html", {"request": request})