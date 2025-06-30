import pytest
from app.schemas.producer import ProducerCreate
from app.repository.producer import create_producer # Para criar dados de teste no db_session

def test_dashboard_summary_empty(client):
    response = client.get("/dashboard/")
    assert response.status_code == 200
    data = response.json()
    assert data["total_farms"] == 0
    assert data["total_hectares"] == 0.0
    assert data["farms_by_state"] == {}
    assert data["cultures_summary"] == {}
    assert data["area_by_soil_use"] == {"agricultural": 0.0, "vegetation": 0.0}

def test_dashboard_summary_with_data(client, db_session):
    # Cria dados de teste diretamente no db_session para pre-popular
    # Isso evita ter que fazer multiplas chamadas POST para setup
    producer1_data = ProducerCreate(
        cpf_cnpj="11111111111", name="Produtor 1", farm_name="Fazenda A",
        city="Cidade1", state="MG", total_area=100.0, agricultural_area=70.0, vegetation_area=30.0,
        cultures=[{"crop_year": "2024", "name": "Soja"}]
    )
    create_producer(db_session, producer1_data)

    producer2_data = ProducerCreate(
        cpf_cnpj="22222222222", name="Produtor 2", farm_name="Fazenda B",
        city="Cidade2", state="SP", total_area=200.0, agricultural_area=120.0, vegetation_area=80.0,
        cultures=[{"crop_year": "2024", "name": "Milho"}, {"crop_year": "2023", "name": "Soja"}]
    )
    create_producer(db_session, producer2_data)

    response = client.get("/dashboard/")
    assert response.status_code == 200
    data = response.json()

    assert data["total_farms"] == 2
    assert data["total_hectares"] == 300.0 # 100 + 200
    assert data["farms_by_state"] == {"MG": 1, "SP": 1}
    assert data["cultures_summary"] == {"Soja": 2, "Milho": 1}
    assert data["area_by_soil_use"] == {"agricultural": 190.0, "vegetation": 110.0} # 70+120=190, 30+80=110