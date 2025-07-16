import hashlib
import re

class CriptografiaShaHelper:
    REGEX_TELEFONE = r'^\(?\d{2}\)?[\s-]?9\d{4}[-\s]?\d{4}$'

    @staticmethod
    def validar_telefone(telefone: str) -> bool:
        """Valida se o telefone tem o formato correto."""
        return re.match(CriptografiaShaHelper.REGEX_TELEFONE, telefone) is not None

    @staticmethod
    def normalizar_telefone(telefone: str) -> str:
        """Remove tudo que não for número do telefone."""
        return re.sub(r'\D', '', telefone)

    @staticmethod
    def hash_telefone(telefone: str) -> str:
        """Aplica SHA-256 ao telefone normalizado."""
        telefone_normalizado = CriptografiaShaHelper.normalizar_telefone(telefone)
        return hashlib.sha256(telefone_normalizado.encode('utf-8')).hexdigest()

    @staticmethod
    def verificar_telefone(telefone_inserido: str, telefone_hash_armazenado: str) -> bool:
        """Compara o telefone inserido com o hash armazenado."""
        telefone_normalizado = CriptografiaShaHelper.normalizar_telefone(telefone_inserido)
        rehashed = hashlib.sha256(telefone_normalizado.encode('utf-8')).hexdigest()
        return rehashed == telefone_hash_armazenado
