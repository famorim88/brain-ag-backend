from sqlalchemy import Column,Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base # Supondo que você tenha um Base.py

class Producer(Base):
    __tablename__ = "producers"

    id = Column(Integer, primary_key=True, index=True)
    cpf_cnpj = Column(String, unique=True, index=True, nullable=False) # Adiciona um campo explícito para CPF/CNPJ

    name = Column(String, index=True)
    farm_name = Column(String)
    city = Column(String)
    state = Column(String)
    total_area = Column(Float)
    agricultural_area = Column(Float)
    vegetation_area = Column(Float)

    # Relação com Culturas (se Culturas estiverem diretamente ligadas ao Produtor)
    cultures = relationship("Culture", back_populates="producer", cascade="all, delete-orphan")

class Culture(Base):
    __tablename__ = "cultures"

    id = Column(Integer, primary_key=True, index=True)
    producer_id = Column(Integer, ForeignKey("producers.id"))
    crop_year = Column(String) # Ex: "Safra 2021"
    name = Column(String)

    producer = relationship("Producer")