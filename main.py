from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models, schemas

Base.metadata.create_all(bind=engine)   # 모델대로 테이블 생성(없는 테이블만). 실무 변경은 5장 Alembic
app = FastAPI(title="가계부 API")

# ── 계좌 ─────────────────────────────────────
@app.post("/accounts", response_model=schemas.AccountRead, status_code=201)
def create_account(payload: schemas.AccountCreate, db: Session = Depends(get_db)):
    account = models.Account(name=payload.name, balance=payload.balance)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

@app.get("/accounts", response_model=list[schemas.AccountRead])
def list_accounts(db: Session = Depends(get_db)):
    return db.execute(
        select(models.Account).order_by(models.Account.id)
    ).scalars().all()

@app.get("/accounts/{account_id}", response_model=schemas.AccountRead)
def get_account(account_id: int, db: Session = Depends(get_db)):
    account = db.get(models.Account, account_id)
    if account is None:
        raise HTTPException(
            status_code=404,
            detail="계좌를 찾을 수 없습니다"
        )
    return account