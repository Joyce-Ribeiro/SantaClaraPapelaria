import hashlib

class CriptografiaShaHelper:

    @staticmethod
    def hash_senha(senha: str) -> str:
        """Criptografa a senha sem salt manual."""
        hashed_bytes = hashlib.sha256(senha.encode('utf-8')).hexdigest()
        return hashed_bytes
    
    @staticmethod
    def verificar_senha(senha_inserida: str, senha_hash_armazenada: str) -> bool:
        """Verifica se a senha inserida corresponde ao hash que foi armazenado."""
        rehashed_senha = CriptografiaShaHelper.hash_senha(senha_inserida)
        return rehashed_senha == senha_hash_armazenada