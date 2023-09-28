from pydantic import BaseModel
from typing import Optional, List
from model.alimento import Alimento
from schemas import GrupoSchema


class AlimentoSchema(BaseModel):
    """ Define como um novo alimento a ser inserido deve ser representado
    """    
    nome: str = "Arroz, integral, cozido"
    energia: int = 124
    proteina: Optional[float] = 2.6
    lipideo: Optional[float] = 1.0
    carboidrato: Optional[float] = 25.8
    grupo_id: int = 1


class AlimentoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no código do alimento.
    """
    id: int = 1


class ListagemAlimentosSchema(BaseModel):
    """ Define como uma listagem de alimentos será retornada.
    """
    alimentos:List[AlimentoSchema]


def apresenta_alimentos(alimentos: List[Alimento]):
    """ Retorna uma representação do alimento seguindo o schema definido em
        AlimentoViewSchema.
    """
    result = []
    for alimento in alimentos:
        result.append({
            "id": alimento.id,
            "nome": alimento.nome,
            "energia": alimento.energia,
            "proteina": alimento.proteina,
            "lipideo": alimento.lipideo,
            "carboidrato": alimento.carboidrato,
            "grupo": alimento.grupo.nome
        })

    return {"alimentos": result}


class AlimentoViewSchema(BaseModel):
    """ Define como um alimento será retornado: alimento + grupo.
    """         
    nome: str = "Arroz, integral, cozido"
    energia: int = 124
    proteina: Optional[float] = 2.6
    lipideo: Optional[float] = 1.0
    carboidrato: Optional[float] = 25.8
    grupo: GrupoSchema = {"id": 1,"nome": "Cereais e derivados"}   


class AlimentoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str


def apresenta_alimento(alimento: Alimento):
    """ Retorna uma representação do alimento seguindo o schema definido em
        AlimentoViewSchema.
    """
    return {     
        "id": alimento.id,   
        "nome": alimento.nome,
        "energia": alimento.energia,
        "proteina": alimento.proteina,
        "lipideo": alimento.lipideo,
        "carboidrato": alimento.carboidrato,        
        "grupo":  {"id": alimento.grupo.id_grupo,"nome": alimento.grupo.nome}    
    }


class AlimentoUpdateSchema(BaseModel):
    """ Define como um novo alimento pode ser atualizado.
    """
    id: int = 1
    nome: str = "Arroz, integral, cozido"
    energia: int = 124
    proteina: Optional[float] = 2.6
    lipideo: Optional[float] = 1.0
    carboidrato: Optional[float] = 25.8    
    grupo_id: int = 1