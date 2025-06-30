# backend/app/crud/producer.py
from sqlalchemy.orm import Session
from models.producer import Producer, Culture
from schemas.producer import ProducerCreate, ProducerUpdate, CultureCreate
from typing import List, Optional
import sqlalchemy # Importar sqlalchemy para func.sum

# --- Funções para Produtor ---
def get_producer(db: Session, producer_id: int): # ID agora é int
    return db.query(Producer).filter(Producer.id == producer_id).first()

# Nova função para buscar por CPF/CNPJ
def get_producer_by_cpf_cnpj(db: Session, cpf_cnpj: str):
    return db.query(Producer).filter(Producer.cpf_cnpj == cpf_cnpj).first()

def get_producers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Producer).offset(skip).limit(limit).all()

def create_producer(db: Session, producer: ProducerCreate) -> Producer:
    db_producer = Producer(
        # ID é auto-gerado, não passamos aqui
        cpf_cnpj=producer.cpf_cnpj, # Usamos o novo campo
        name=producer.name,
        farm_name=producer.farm_name,
        city=producer.city,
        state=producer.state,
        total_area=producer.total_area,
        agricultural_area=producer.agricultural_area,
        vegetation_area=producer.vegetation_area
    )
    db.add(db_producer)
    db.commit()
    db.refresh(db_producer)

    if producer.cultures:
        for culture_data in producer.cultures:
            db_culture = Culture(
                producer_id=db_producer.id, # O ID do produtor já estará disponível
                crop_year=culture_data.crop_year,
                name=culture_data.name
            )
            db.add(db_culture)
        db.commit()
        db.refresh(db_producer)
    return db_producer

def update_producer(db: Session, producer_id: int, producer_update: ProducerUpdate) -> Optional[Producer]:
    db_producer = db.query(Producer).filter(Producer.id == producer_id).first()
    if not db_producer:
        return None
    for field, value in producer_update.dict(exclude_unset=True).items():
        setattr(db_producer, field, value)
    db.add(db_producer)
    db.commit()
    db.refresh(db_producer)
    return db_producer

def delete_producer(db: Session, producer_id: int) -> Optional[Producer]:
    db_producer = db.query(Producer).filter(Producer.id == producer_id).first()
    if db_producer:
        db.delete(db_producer)
        db.commit()
    return db_producer


# --- Funções para Cultura ---
def create_culture_for_producer(db: Session, producer_id: int, culture: CultureCreate) -> Optional[Culture]:
    db_producer = db.query(Producer).filter(Producer.id == producer_id).first()
    if not db_producer:
        return None

    db_culture = Culture(
        # ID é auto-gerado
        producer_id=producer_id,
        crop_year=culture.crop_year,
        name=culture.name
    )
    db.add(db_culture)
    db.commit()
    db.refresh(db_culture)
    return db_culture

# --- Funções do Dashboard (não precisam de grandes mudanças nos parâmetros) ---
def get_total_farms(db: Session) -> int:
    return db.query(Producer).count()

def get_total_hectares(db: Session) -> float:
    total_area = db.query(sqlalchemy.func.sum(Producer.total_area)).scalar()
    return total_area if total_area is not None else 0.0