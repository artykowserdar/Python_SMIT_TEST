from sqlalchemy.orm import Session
from app.models import Rate


# Добавить тариф
def add_rate(db: Session, date: str, cargo_type: str, rate: float):
    db_rate = Rate(date=date,
                   cargo_type=cargo_type,
                   rate=rate)
    db.add(db_rate)
    db.commit()
    db.refresh(db_rate)
    return db_rate


# Получить тариф по дате и типу груза
def get_rate(db: Session, date: str, cargo_type: str):
    query = db.query(Rate) \
        .filter(Rate.date == date,
                Rate.cargo_type == cargo_type) \
        .first()
    return query.rate
