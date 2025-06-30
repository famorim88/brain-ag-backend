# backend/app/core/utils.py

from validate_docbr import CPF, CNPJ

def validate_cpf_cnpj(doc: str) -> bool:
    """
    Valida um número de CPF ou CNPJ.

    Args:
        doc (str): O número de CPF ou CNPJ a ser validado.

    Returns:
        bool: True se o CPF/CNPJ for válido, False caso contrário.
    """
    if not isinstance(doc, str):
        return False

    # Remove caracteres não numéricos (pontos, traços, barras)
    cleaned_doc = ''.join(filter(str.isdigit, doc))

    if len(cleaned_doc) == 11:
        # É um CPF
        cpf_validator = CPF()
        return cpf_validator.validate(cleaned_doc)
    elif len(cleaned_doc) == 14:
        # É um CNPJ
        cnpj_validator = CNPJ()
        return cnpj_validator.validate(cleaned_doc)
    else:
        # Não tem o tamanho de um CPF nem de um CNPJ
        return False

# Exemplo de uso (para teste local, pode ser removido depois)
if __name__ == "__main__":
    print(f"CPF Válido (exemplo): {validate_cpf_cnpj('111.111.111-11')}") # Este CPF é um exemplo, mas a validação dele depende dos dígitos verificadores
    print(f"CPF Inválido (exemplo): {validate_cpf_cnpj('123.456.789-00')}")
    print(f"CNPJ Válido (exemplo): {validate_cpf_cnpj('00.000.000/0001-91')}") # Este CNPJ é um exemplo
    print(f"CNPJ Inválido (exemplo): {validate_cpf_cnpj('00.000.000/0001-00')}")
    print(f"Formato Inválido: {validate_cpf_cnpj('12345')}")
    print(f"Não é string: {validate_cpf_cnpj(123)}")