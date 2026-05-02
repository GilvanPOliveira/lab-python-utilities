from fastapi import APIRouter

from src.modules.document_tools.schemas import DocumentRequest, DocumentResponse
from src.modules.document_tools.service import validate_cnpj, validate_cpf

router = APIRouter()


@router.post("/validate-cpf", response_model=DocumentResponse)
def validate_cpf_route(payload: DocumentRequest):
    return validate_cpf(payload)


@router.post("/validate-cnpj", response_model=DocumentResponse)
def validate_cnpj_route(payload: DocumentRequest):
    return validate_cnpj(payload)
