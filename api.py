import hmac
import hashlib
import json
from datetime import datetime

import requests
from telebot.types import User

import config
import esquemas
import exceptions


class API:

    def __init__(self, usuario: User) -> None:
        self.url = config.API_URL
        autenticacao = dict(
            auth_date=round(datetime.now().timestamp()),
            first_name=usuario.first_name,
            id=usuario.id,
            last_name=usuario.last_name if usuario.last_name else "",
            photo_url="",
            username=usuario.username if usuario.username else "",
        )
        chave_secreta = hashlib.sha256(config.TOKEN.encode()).digest()
        _ = [f"{c}={v}" if v else None for c, v in autenticacao.items()]
        _ = list(filter(None, _))
        mensagem = "\n".join(_)
        hash_mensagem = hmac.new(
            key=chave_secreta, msg=mensagem.encode(), digestmod=hashlib.sha256
        ).hexdigest()
        autenticacao["hash"] = hash_mensagem

        url = self.url + "usuario/autenticar-telegram/"
        resposta = requests.post(url=url, data=json.dumps(autenticacao))
        resposta_json = resposta.json()
        if resposta.status_code == 200:
            self.headers = {"Authorization": f"Bearer {resposta_json.get('token')}"}
        elif resposta.status_code == 401:
            raise exceptions.ErroAutenticacao(resposta_json.get("detail"))
        else:
            raise exceptions.ErroGenerico(resposta_json.get("detail"))

    def criar_nota(self, nota: esquemas.NovaNota) -> esquemas.Nota:
        url = self.url + "nota/"
        resposta = requests.post(
            url=url, headers=self.headers, data=json.dumps(nota.model_dump())
        )
        resposta_json = resposta.json()
        if resposta.status_code == 200:
            return esquemas.Nota.model_validate(resposta_json)
        elif resposta.status_code == 401:
            raise exceptions.ErroAutenticacao(resposta_json.get("detail"))
        else:
            raise exceptions.ErroGenerico(resposta_json.get("detail"))

    def obter_notas(self) -> esquemas.ResultadoPesquisa:
        url = self.url + "nota/"
        resposta = requests.get(url=url, headers=self.headers)
        resposta_json = resposta.json()
        if resposta.status_code == 200:
            return esquemas.ResultadoPesquisa.model_validate(resposta_json).resultados
        elif resposta.status_code == 401:
            raise exceptions.ErroAutenticacao(resposta_json.get("detail"))
        else:
            raise exceptions.ErroGenerico(resposta_json.get("detail"))

    def obter_nota(self, id: str) -> esquemas.Nota:
        url = self.url + f"nota/{id}/"
        resposta = requests.get(url=url, headers=self.headers)
        resposta_json = resposta.json()
        if resposta.status_code == 200:
            return esquemas.Nota.model_validate(resposta_json)
        elif resposta.status_code == 401:
            raise exceptions.ErroAutenticacao(resposta_json.get("detail"))
        else:
            raise exceptions.ErroGenerico(resposta_json.get("detail"))

    def editar_nota(self, id: str, nota: esquemas.Nota) -> esquemas.Nota:
        url = self.url + f"nota/{id}/"
        resposta = requests.put(
            url=url, headers=self.headers, data=json.dumps(nota.model_dump())
        )
        resposta_json = resposta.json()
        if resposta.status_code == 200:
            return esquemas.Nota.model_validate(resposta_json)
        elif resposta.status_code == 401:
            raise exceptions.ErroAutenticacao(resposta_json.get("detail"))
        else:
            raise exceptions.ErroGenerico(resposta_json.get("detail"))

    def deletar_nota(self, id: str) -> esquemas.Nota:
        url = self.url + f"nota/{id}/"
        resposta = requests.delete(url=url, headers=self.headers)
        resposta_json = resposta.json()
        if resposta.status_code == 200:
            return esquemas.Nota.model_validate(resposta_json)
        elif resposta.status_code == 401:
            raise exceptions.ErroAutenticacao(resposta_json.get("detail"))
        else:
            raise exceptions.ErroGenerico(resposta_json.get("detail"))
