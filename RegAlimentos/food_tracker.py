import psycopg2
from psycopg2.extras import RealDictCursor
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/food_tracker")

def get_db_connection():

    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Erro de Conexão: {e}")
        raise e

def init_db():

    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS meals (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS food_items (
            id SERIAL PRIMARY KEY,
            meal_id INTEGER,
            name TEXT NOT NULL,
            quantity REAL NOT NULL,
            unit TEXT NOT NULL,
            FOREIGN KEY (meal_id) REFERENCES meals (id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()

class FoodItemModel(BaseModel):
    name: str
    quantity: float
    unit: str

class MealCreate(BaseModel):
    title: str
    created_at: Optional[str] = None
    items: List[FoodItemModel]

class MealResponse(BaseModel):
    id: int
    title: str
    created_at: str
    items: List[FoodItemModel]

app = FastAPI(title="Diário Alimentar")

try:
    init_db()
except Exception as e:
    print(f"Aviso de Inicialização: {e}")


@app.post("/api/meals", response_model=dict)
def create_meal(meal: MealCreate):
    conn = get_db_connection()
    c = conn.cursor()
    try:

        query_meal = "INSERT INTO meals (title, created_at) VALUES (%s, %s) RETURNING id"
        

        if meal.created_at:
            f_date = meal.created_at.replace("T", " ")
            if len(f_date) == 16: f_date += ":00"
            created_at_val = f_date
        else:
            created_at_val = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        c.execute(query_meal, (meal.title, created_at_val))
        meal_id = c.fetchone()[0]

        query_item = "INSERT INTO food_items (meal_id, name, quantity, unit) VALUES (%s, %s, %s, %s)"

        for item in meal.items:
            c.execute(query_item, (meal_id, item.name, item.quantity, item.unit))
        
        conn.commit()
        return {"status": "success", "meal_id": meal_id}
        
    except Exception as e:
        conn.rollback()
        print(f"Erro ao criar registro: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao salvar dados.")
    finally:
        conn.close()

@app.get("/api/meals", response_model=List[MealResponse])
def get_meals():
    conn = get_db_connection()
    c = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        c.execute("SELECT * FROM meals ORDER BY created_at DESC")
        meals_rows = c.fetchall()
        
        result = []
        
        for meal_row in meals_rows:
            c.execute("SELECT name, quantity, unit FROM food_items WHERE meal_id = %s", (meal_row['id'],))
            items_rows = c.fetchall()
            
            items = [
                FoodItemModel(name=i['name'], quantity=i['quantity'], unit=i['unit']) 
                for i in items_rows
            ]
            
            raw_date = meal_row['created_at']
            if isinstance(raw_date, datetime):
                formatted_date = raw_date.strftime('%d/%m/%Y %H:%M')
            else:
                formatted_date = str(raw_date)

            result.append(MealResponse(
                id=meal_row['id'],
                title=meal_row['title'],
                created_at=formatted_date,
                items=items
            ))
            
        return result
    finally:
        conn.close()

@app.delete("/api/meals/{meal_id}")
def delete_meal(meal_id: int):
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute("DELETE FROM meals WHERE id = %s", (meal_id,))
        conn.commit()
        return {"status": "deleted"}
    finally:
        conn.close()

@app.get("/")
async def read_root():
    file_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    if not os.path.exists(file_path):
        return HTMLResponse(content="<h1>Frontend não encontrado. Verifique a pasta templates.</h1>", status_code=404)
    return FileResponse(file_path)

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)