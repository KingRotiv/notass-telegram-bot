import config


class ErroGenerico(Exception):

    def __init__(self, msg: str, *args) -> None:
        self.msg = msg


class ErroAutenticacao(Exception):

    def __init__(self, msg: str, *args) -> None:
        self.msg = msg + f"\n\nSe cadastre ou vincule uma conta em: {config.BASE_URL}"
