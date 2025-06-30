# backend/app/api/dashboard.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.repository import producer as repoProducer # Renomeei para evitar conflito com model
from app.schemas.producer import DashboardSummary

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/", response_model=DashboardSummary)
def get_dashboard_data(db: Session = Depends(get_db)):
    """
    Retorna dados sumários e para gráficos para o dashboard.
    """
    total_farms = repoProducer.get_total_farms(db)
    total_hectares = repoProducer.get_total_hectares(db)
    farms_by_state = repoProducer.get_farms_by_state_summary(db)
    cultures_summary = repoProducer.get_cultures_summary(db)
    area_by_soil_use = repoProducer.get_area_by_soil_use_summary(db)

    return DashboardSummary(
        total_farms=total_farms,
        total_hectares=total_hectares,
        farms_by_state=farms_by_state,
        cultures_summary=cultures_summary,
        area_by_soil_use=area_by_soil_use
    )