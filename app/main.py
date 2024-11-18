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
def upload_rates(rates: dict, db: Session = Depends(get_db)):
    try:
        for date, rate_data in rates.items():
            for rate_info in rate_data:
                crud.add_rate(db, date, rate_info["cargo_type"], float(rate_info["rate"]))
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
