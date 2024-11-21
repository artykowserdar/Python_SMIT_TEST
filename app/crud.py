from sqlalchemy.orm import Session

from app.kafka_prod import log_to_kafka
from app.models import Rate


# Добавить тариф
def add_rate(db: Session, date: str, cargo_type: str, rate: float, user_id: int = None):
    db_rate = Rate(date=date,
                   cargo_type=cargo_type,
                   rate=rate)
    db.add(db_rate)
    db.commit()
    db.refresh(db_rate)
    log_to_kafka(
        user_id,
        "ADD_RATE",
        f"Rate added: {rate} for {cargo_type} on {date}",
    )
    return db_rate


# Получить тариф по дате и типу груза
def get_rate(db: Session, date: str, cargo_type: str):
    db_rate = db.query(Rate) \
        .filter(Rate.date == date,
                Rate.cargo_type == cargo_type).first()
    return db_rate.rate


# Редактировать тариф по ID
def edit_rate(db: Session, id: int, new_rate: float, user_id: int = None):
    db_rate = db.query(Rate) \
        .filter(Rate.id == id).first()
    if db_rate:
        db_rate_old = db_rate.rate
        db_rate.rate = new_rate
        db.commit()
        log_to_kafka(
            user_id,
            "EDIT_RATE",
            f"Rate edited ID {id}: {db_rate_old} -> {new_rate}",
        )
        return db_rate
    return None


# Удалить тариф по ID
def delete_rate(db: Session, id: int, user_id: int = None):
    db_rate = db.query(Rate) \
        .filter(Rate.id == id).first()
    if db_rate:
        db.delete(db_rate)
        db.commit()
        log_to_kafka(
            user_id,
            "DELETE_RATE",
            f"Rate deleted ID {id}",
        )
        return db_rate
    return None
