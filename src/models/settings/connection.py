# Arquivo que ira realizar a conexão com o banco de dados
# que esta na raiz do projeto.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#classe privada, não muito recomendado, porém quero ver como funciona
class __DBConnectionHandler:
    def __init__(self) -> None:
        self.__connection_string = "{}:///{}".format(
            "sqlite",
            "storage.db"
        )
        self.__engine = None
        self.session = None
    
    def connect_to_db(self) -> None:
        self.__engine = create_engine(self.__connection_string)
        
    def get_engine(self):
        return self.__engine
    
    def __enter__(self):
        session_maker = sessionmaker()
        self.session= session_maker(bind=self.__engine)
        return self
        
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

# Variavel que será usada para realizar a conexão do banco
# no exemplo de "from 'caminho do arquivo' import 'variavel com classe privada'"        
db_connection_handler = __DBConnectionHandler()
