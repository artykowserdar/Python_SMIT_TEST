from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import engine, get_db
from app.models import Base

# Создать таблицы в базе данных
Base.metadata.create_all(bind=engine)

app = FastAPI()


# загрузить тарифы из JSON
@app.post("/upload_rates/")
def upload_rates(rates: dict, user_id: int = None, db: Session = Depends(get_db)):
    try:
        for date, rate_data in rates.items():
            for rate_info in rate_data:
                crud.add_rate(db, date, rate_info["cargo_type"], float(rate_info["rate"]), user_id)
        return {"message": "Тарифы успешно загружены"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# посчитать стоимость страхования
@app.post("/calculate_insurance/")
def calculate_insurance(request: schemas.InsuranceRequest, db: Session = Depends(get_db)):
    try:
        rate = crud.get_rate(db, request.date, request.cargo_type)
        if rate is None:
            raise HTTPException(status_code=404, detail="Тариф не найдена для указанной даты и типа груза")
        insurance_cost = request.declared_value * rate
        return {"insurance_cost": insurance_cost}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Редактировать тариф по ID
@app.put("/edit_rate/{rate_id}")
def edit_rate(rate_id: int, new_rate: float, user_id: int = None, db: Session = Depends(get_db)):
    try:
        updated_rate = crud.edit_rate(db, rate_id, new_rate, user_id)
        if not updated_rate:
            raise HTTPException(status_code=404, detail="Тариф не найден")
        return {"message": "Тариф успешно изменен", "rate": updated_rate}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Удалить тариф по ID
@app.delete("/delete_rate/{rate_id}")
def delete_rate(rate_id: int, user_id: int = None, db: Session = Depends(get_db)):
    try:
        deleted_rate = crud.delete_rate(db, rate_id, user_id)
        if not deleted_rate:
            raise HTTPException(status_code=404, detail="Тариф не найден")
        return {"message": "Тариф успешно удален"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
