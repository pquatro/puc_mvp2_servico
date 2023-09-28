from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from  model import Base


class Grupo(Base):
    __tablename__ = 'grupo'
    
    id_grupo = Column("id_grupo", Integer, primary_key=True)
    nome = Column(String(4000))
    
    # Definição do relacionamento entre o alimento e o grupo.    
    alimentos = relationship("Alimento")    

    def __init__(self, nome:str):                
        """
        Cria um Grupo de alimento

        Arguments:
            nome: o nome de um grupo.            
        """
        self.nome = nome
       

    