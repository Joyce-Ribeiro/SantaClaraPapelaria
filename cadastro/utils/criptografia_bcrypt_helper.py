import bcrypt

class CriptografiaBcryptHelper:
    @staticmethod
    def hash_senha(senha: str) -> str:
        """Criptografa a senha com bcrypt."""
        senha_bytes = senha.encode('utf-8')
        hashed = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())
        return hashed.decode('utf-8')

    @staticmethod
    def verificar_senha(senha_inserida: str, senha_hash_armazenada: str) -> bool:
        """Verifica se a senha inserida corresponde ao hash armazenado."""
        try:
            return bcrypt.checkpw(senha_inserida.encode('utf-8'), senha_hash_armazenada.encode('utf-8'))
        except ValueError:
            return False
