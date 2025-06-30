# backend/app/api/producer.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.producer import Producer, ProducerCreate, ProducerUpdate, CultureCreate, Culture
from app.repository import producer as repoProducer
from app.core.utils import validate_cpf_cnpj
from typing import List

router = APIRouter(
    prefix="/producers",
    tags=["Producers"]
)

@router.post("/", response_model=Producer, status_code=status.HTTP_201_CREATED)
def create_new_producer(producer: ProducerCreate, db: Session = Depends(get_db)):
    # Validação do CPF ou CNPJ
    if not validate_cpf_cnpj(producer.cpf_cnpj): # Valida o novo campo cpf_cnpj
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CPF/CNPJ inválido.")

    # Verifica se já existe um produtor com este CPF/CNPJ
    db_producer = repoProducer.get_producer_by_cpf_cnpj(db, cpf_cnpj=producer.cpf_cnpj)
    if db_producer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Produtor com este CPF/CNPJ já cadastrado.")

    # Validação da soma das áreas
    if not (producer.agricultural_area + producer.vegetation_area <= producer.total_area):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Soma das áreas agricultável e de vegetação não pode exceder a área total da fazenda.")

    return repoProducer.create_producer(db=db, producer=producer)

@router.get("/", response_model=List[Producer])
def read_producers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    producers = repoProducer.get_producers(db, skip=skip, limit=limit)
    return producers

@router.get("/{producer_id}", response_model=Producer)
def read_producer(producer_id: int, db: Session = Depends(get_db)): # ID agora é int
    db_producer = repoProducer.get_producer(db, producer_id=producer_id)
    if db_producer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produtor não encontrado")
    return db_producer

@router.put("/{producer_id}", response_model=Producer)
def update_existing_producer(producer_id: int, producer_update: ProducerUpdate, db: Session = Depends(get_db)):
    db_producer = repoProducer.update_producer(db, producer_id=producer_id, producer_update=producer_update)
    if db_producer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produtor não encontrado")
    # Validação de área após a atualização, se os campos forem fornecidos
    if producer_update.agricultural_area is not None or producer_update.vegetation_area is not None or producer_update.total_area is not None:
        if not (db_producer.agricultural_area + db_producer.vegetation_area <= db_producer.total_area):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Soma das áreas agricultável e de vegetação não pode exceder a área total da fazenda após a atualização.")
    return db_producer

@router.delete("/{producer_id}", response_model=Producer)
def delete_existing_producer(producer_id: int, db: Session = Depends(get_db)):
    db_producer = repoProducer.delete_producer(db, producer_id=producer_id)
    if db_producer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produtor não encontrado")
    return db_producer

@router.post("/{producer_id}/cultures/", response_model=Culture, status_code=status.HTTP_201_CREATED)
def add_culture_to_producer(producer_id: int, culture: CultureCreate, db: Session = Depends(get_db)): # producer_id agora é int
    db_producer = repoProducer.get_producer(db, producer_id=producer_id)
    if not db_producer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produtor não encontrado")

    existing_culture = db.query(Culture).filter(
        Culture.producer_id == producer_id,
        Culture.crop_year == culture.crop_year,
        Culture.name == culture.name
    ).first()
    if existing_culture:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Esta cultura e safra já existem para este produtor.")

    db_culture = repoProducer.create_culture_for_producer(db=db, producer_id=producer_id, culture=culture)
    if not db_culture:
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Falha ao adicionar cultura.")
    return db_culture