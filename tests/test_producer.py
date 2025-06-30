import pytest
from app.schemas.producer import ProducerCreate, ProducerUpdate

def test_create_producer(client):
    producer_data = {
        "cpf_cnpj": "12345678901",
        "name": "João da Silva",
        "farm_name": "Fazenda Esperança",
        "city": "São Paulo",
        "state": "SP",
        "total_area": 1000.0,
        "agricultural_area": 700.0,
        "vegetation_area": 300.0
    }
    response = client.post("/producers/", json=producer_data)
    assert response.status_code == 201
    created_producer = response.json()
    assert created_producer["cpf_cnpj"] == producer_data["cpf_cnpj"]
    assert created_producer["name"] == producer_data["name"]
    assert created_producer["id"] is not None # ID deve ser gerado

def test_create_producer_invalid_cpf_cnpj(client):
    producer_data = {
        "cpf_cnpj": "111", # CPF/CNPJ inválido
        "name": "João da Silva",
        "farm_name": "Fazenda Teste",
        "city": "Cidade",
        "state": "UF",
        "total_area": 100.0,
        "agricultural_area": 50.0,
        "vegetation_area": 50.0
    }
    response = client.post("/producers/", json=producer_data)
    assert response.status_code == 400
    assert "CPF/CNPJ inválido" in response.json()["detail"]

def test_create_producer_invalid_area_sum(client):
    producer_data = {
        "cpf_cnpj": "12345678902",
        "name": "Maria Teste",
        "farm_name": "Fazenda Área Problema",
        "city": "Cidade",
        "state": "UF",
        "total_area": 100.0,
        "agricultural_area": 70.0,
        "vegetation_area": 40.0 # Soma (110) > Total (100)
    }
    response = client.post("/producers/", json=producer_data)
    assert response.status_code == 400
    assert "Soma das áreas agricultável e de vegetação não pode exceder a área total" in response.json()["detail"]

def test_get_producer(client):
    # Primeiro, cria um produtor para poder buscá-lo
    producer_data = {
        "cpf_cnpj": "11122233344",
        "name": "Carlos",
        "farm_name": "Sítio Alegre",
        "city": "Rio",
        "state": "RJ",
        "total_area": 200.0,
        "agricultural_area": 150.0,
        "vegetation_area": 50.0
    }
    create_response = client.post("/producers/", json=producer_data)
    assert create_response.status_code == 201
    producer_id = create_response.json()["id"]

    # Agora busca o produtor
    response = client.get(f"/producers/{producer_id}")
    assert response.status_code == 200
    retrieved_producer = response.json()
    assert retrieved_producer["cpf_cnpj"] == producer_data["cpf_cnpj"]
    assert retrieved_producer["id"] == producer_id

def test_get_non_existent_producer(client):
    response = client.get("/producers/99999") # ID que não existe
    assert response.status_code == 404
    assert "Produtor não encontrado" in response.json()["detail"]
    
#FALTA TESTE DE ADICIONAR CULTURA AO PRODUTOR, POIS METODO ESTA COM FALHA
#ALEM DE MAIS ALGUNS TESTES MAIS COMPLETOS