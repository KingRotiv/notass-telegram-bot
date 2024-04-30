from datetime import datetime

from pydantic import BaseModel


class Nota(BaseModel):

    id: int
    id_usuario: int
    titulo: str
    texto: str
    data_registro: datetime
    data_alteracao: datetime


class NovaNota(BaseModel):

    titulo: str
    texto: str


class EditarNota(NovaNota): ...


class ResultadoPesquisa(BaseModel):

    resultados: list[Nota]
