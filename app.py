from fastapi import FastAPI, Request
from fastapi.params import Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3
import starlette.status as status
from starlette.responses import RedirectResponse  

app = FastAPI()  

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def index(request : Request):
    con = sqlite3.connect("todo.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from todo")
    items = cur.fetchall()
    con.close
    return templates.TemplateResponse("index.html",{"request" : request, "items" : items})

@app.post("/",response_class=HTMLResponse)
def addTodo(request : Request, name : str =  Form(...), desc : str = Form(...)):
    with sqlite3.connect("todo.db") as con:
        cur = con.cursor()
        cur.execute("INSERT into todo(name,desc) values(?,?)",(name,desc))
        con.commit()
    return RedirectResponse("/",status_code=status.HTTP_302_FOUND)
    #return templates.TemplateResponse("index.html",{"request" : request, "message" : "succesfully added!!" })


@app.get("/register",response_class=HTMLResponse)
def register(request : Request):
    return templates.TemplateResponse("register.html", {"request" : request})