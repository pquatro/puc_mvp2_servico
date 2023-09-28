from pydantic import BaseModel
from typing import Optional, List
from model.grupo import Grupo


class GrupoSchema(BaseModel):
    """ Define como um novo grupo a ser inserido deve ser representado
    """        
    nome: str = "Cereais e derivados"
    

class GrupoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no código do grupo.
    """
    id_grupo: int = 1


class ListagemGruposSchema(BaseModel):
    """ Define como uma listagem de grupos será retornada.
    """
    grupos:List[GrupoSchema]


def apresenta_grupos(grupos: List[Grupo]):
    """ Retorna uma representação do grupo seguindo o schema definido em
        GrupoViewSchema.
    """
    result = []
    for grupo in grupos:
        result.append({
            "id": grupo.id_grupo,
            "nome": grupo.nome            
        })

    return {"grupos": result}


class GrupoViewSchema(BaseModel):
    """ Define como um grupo será retornado: grupo.
    """
    id_grupo: int = 1
    nome: str = "Cereais e derivados"    


class GrupoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_grupo(grupo: Grupo):
    """ Retorna uma representação do grupo seguindo o schema definido em
        GrupoViewSchema.
    """
    return {
        "id": grupo.id_grupo,
        "nome": grupo.nome        
    }
