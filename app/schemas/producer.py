# backend/app/schemas/producer.py
from pydantic import BaseModel, Field
from typing import Optional, List,Dict

# --- Schemas de Cultura ---
class CultureBase(BaseModel):
    crop_year: str
    name: str

class CultureCreate(CultureBase):
    pass

class Culture(CultureBase):
    id: int # ID agora é Integer
    producer_id: int # producer_id agora é Integer

    class Config:
        from_attributes = True

# --- Schemas de Produtor ---
class ProducerBase(BaseModel):
    # O ID gerado pelo banco não é incluído na criação
    # mas o cpf_cnpj é necessário
    cpf_cnpj: str = Field(..., description="CPF ou CNPJ do produtor")
    name: str
    farm_name: str
    city: str
    state: str
    total_area: float
    agricultural_area: float
    vegetation_area: float

class ProducerCreate(ProducerBase):
    cultures: Optional[List[CultureCreate]] = None

class ProducerUpdate(BaseModel):
    # Não inclua o id nem o cpf_cnpj para atualização direta,
    # pois geralmente não são alterados.
    name: Optional[str] = None
    farm_name: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    total_area: Optional[float] = None
    agricultural_area: Optional[float] = None
    vegetation_area: Optional[float] = None

class Producer(ProducerBase):
    id: int # O ID agora é Integer e será retornado
    cultures: List[Culture] = []
    class Config:
        from_attributes = True

# --- Schemas para o Dashboard (não mudam em relação aos IDs) ---
class DashboardSummary(BaseModel):
    total_farms: int
    total_hectares: float
    farms_by_state: Dict[str, int]
    cultures_summary: Dict[str, int]
    area_by_soil_use: Dict[str, float]