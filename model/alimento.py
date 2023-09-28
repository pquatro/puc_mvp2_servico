from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from model.grupo import Grupo
from  model import Base


class Alimento(Base):
    __tablename__ = 'alimento'

    id = Column("id_alimento", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    energia = Column(Integer)
    proteina = Column(Float)
    lipideo = Column(Float)
    carboidrato = Column(Float)    
    
    # Definição do relacionamento entre o grupo e um alimento.
    # Aqui está sendo definido a coluna 'grupo_id' que vai guardar
    # a referencia ao grupo, a chave estrangeira que relaciona
    # um grupo ao alimento.
    grupo_id = Column(Integer, ForeignKey("grupo.id_grupo"), nullable=False)
    
    # many-to-one 
    grupo = relationship("Grupo")

    def __init__(self, nome:str, energia:int, proteina:float, lipideo:float, carboidrato:float, grupo:Grupo):                 
        """
        Cria um Alimento

        Arguments:
            nome: nome ou descrição do alimento por 100 gramas por parte comestível.
            energia: quantidade de calorias (kcal) 
            proteína: quantidade em gramas
            lipídeo: quantidade em gramas
            carboidrato: quantidade em gramas
            grupo: grupo que o alimento pertence
        """       
        self.nome = nome
        self.energia = energia
        self.proteina = proteina
        self.lipideo = lipideo
        self.carboidrato = carboidrato        
        self.grupo = grupo
        

    def adiciona_grupo(self, grupo:Grupo):
        """ Adiciona um novo grupo ao alimento
        """
        self.grupo = grupo