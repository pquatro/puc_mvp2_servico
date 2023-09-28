from flask_openapi3 import OpenAPI, Info, Tag
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS
from flask import redirect
from model import Session, Alimento, Grupo
from schemas import *
import sqlite3

info = Info(title="API de Cadastro de Composição de Alimentos", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)


# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
alimento_tag = Tag(name="Alimento", description="Adição, Atualização, visualização e remoção de alimentos à base")
grupo_tag = Tag(name="Grupo", description="Adição, visualização e remoção de grupos à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/alimento', tags=[alimento_tag],
          responses={"200": AlimentoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_alimento(form: AlimentoSchema):
    """Adiciona um novo Alimento à base de dados

    Retorna uma representação de um alimento e grupo associado.
    """
    alimento = Alimento (        
        nome=form.nome,
        energia = form.energia,
        proteina = form.proteina,
        lipideo = form.lipideo,
        carboidrato = form.carboidrato,
        grupo = None
    )

    grupo_id = form.grupo_id
   
    

    try:
        # criando conexão com a base
        session = Session()

        # fazendo a busca do grupo pelo id informado
        grupo = session.query(Grupo).filter(Grupo.id_grupo == grupo_id).first()
        if not grupo:
            # se não existir o grupo cadastrado
            error_msg = "Grupo não cadastrado na base :/"
            return {"mesage": error_msg}, 200            
        else:
            # adiciona grupo ao alimento            
            alimento.grupo = grupo       

        # adicionando alimento
        session.add(alimento)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        return apresenta_alimento(alimento), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Alimento de mesmo nome já salvo na base :/"
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        return {"mesage": error_msg}, 400


@app.get('/alimentos', tags=[alimento_tag],
         responses={"200": ListagemAlimentosSchema, "404": ErrorSchema})
def get_alimentos():
    """Faz a busca por todos os Alimentos cadastrados

    Retorna uma representação da listagem de alimentos e grupo associado.
    """
    # criando conexão com a base
    session = Session()
    # fazendo a busca    
    alimentos = session.query(Alimento).all()
               
    if not alimentos:
        # se não há alimentos cadastrados
        return {"alimentos": []}, 200
    else:
        # retorna a representação de alimento        
        return apresenta_alimentos(alimentos), 200


@app.get('/alimento', tags=[alimento_tag],
         responses={"200": AlimentoViewSchema, "404": ErrorSchema})
def get_alimento(query: AlimentoBuscaSchema):
    """Faz a busca por um Alimento a partir do id do alimento

    Retorna uma representação dos alimentos e grupo associado.
    """
    alimento_id = query.id
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    alimento = session.query(Alimento).filter(Alimento.id == alimento_id).first()
    
    if not alimento:
        # se o alimento não foi encontrado
        error_msg = "Alimento não encontrado na base :/"
        return {"mesage": error_msg}, 404
    else:
        # retorna a representação de alimento
        return apresenta_alimento(alimento), 200


@app.delete('/alimento', tags=[alimento_tag],
            responses={"200": AlimentoDelSchema, "404": ErrorSchema})
def del_alimento(query: AlimentoBuscaSchema):
    """Deleta um Alimento a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
    alimento_id = query.id

    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Alimento).filter(Alimento.id == alimento_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        return {"mesage": "Alimento removido", "id": alimento_id}
    else:
        # se o alimento não foi encontrado
        error_msg = "Alimento não encontrado na base :/"
        return {"mesage": error_msg}, 404


@app.post('/update_alimento', tags=[alimento_tag],
          responses={"200": AlimentoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def update_alimento(form: AlimentoUpdateSchema):
    """Edita um Produto já salvo na base de dados

    Retorna uma representação dos produtos e grupo associado.
    """
    alimento_id = form.id    
    grupo_id = form.grupo_id


    try:
        # criando conexão com a base para verificar grupo
        session = Session()

        # fazendo a busca de grupo pelo id informado
        grupo = session.query(Grupo).filter(Grupo.id_grupo == grupo_id).first()
        if not grupo:
            # se não existe o grupo cadastrado
            error_msg = "Grupo não encontrado na base :/"
            return {"mesage": error_msg}, 200                    

        # criando conexão com a base para verificar alimento
        session = Session()

         # fazendo a busca do alimento pelo id informado
        query = session.query(Alimento).filter(Alimento.id == alimento_id)        
        db_alimento = query.first()      

        if not db_alimento:
            # se o alimento não foi encontrado
            error_msg = "Alimento não encontrado na base :/"            
            return {"mesage": error_msg}, 404
        else:
             # altera os campos do alimento
            if form.nome:
                db_alimento.nome = form.nome
            
            if form.energia:
                db_alimento.energia = form.energia
            
            if form.proteina:
                db_alimento.proteina = form.proteina

            if form.lipideo:
                db_alimento.lipideo = form.lipideo
            
            if form.carboidrato:
                db_alimento.carboidrato = form.carboidrato

            if form.grupo_id:
                db_alimento.grupo_id = grupo.id_grupo

            #atualiza o alimento
            session.add(db_alimento)
            session.commit()            
            return apresenta_alimento(db_alimento), 200        

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Alimento de mesmo nome já salvo na base :/"
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        return {"mesage": error_msg}, 400  
    

@app.post('/grupo', tags=[grupo_tag],
          responses={"200": GrupoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_grupo(form: GrupoSchema):
    """Adiciona um novo Grupo à base de dados

    Retorna uma representação de Grupo.
    """
    grupo = Grupo (
        nome=form.nome        
    )          

    try:
        # criando conexão com a base
        session = Session()        
        # adicionando grupo
        session.add(grupo)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        return apresenta_grupo(grupo), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Grupo de mesmo nome já salvo na base :/"
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        return {"mesage": error_msg}, 400
    

@app.get('/grupos', tags=[grupo_tag],
        responses={"200": ListagemGruposSchema, "404": ErrorSchema})
def get_grupos():
    """Faz a busca por todos os Grupos cadastrados

    Retorna uma representação da listagem de Grupos.
    """
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    grupos = session.query(Grupo).all()

    if not grupos:
        # se não há grupos cadastrados
        return {"grupos": []}, 200
    else:
        # retorna a representação de grupo
        print(grupos)
        return apresenta_grupos(grupos), 200


@app.get('/grupo', tags=[grupo_tag],
         responses={"200": GrupoViewSchema, "404": ErrorSchema})
def get_grupo(query: GrupoBuscaSchema):
    """Faz a busca por um Grupo a partir do id do grupo

    Retorna uma representação do grupo.
    """
    grupo_id = query.id_grupo
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    grupo = session.query(Grupo).filter(Grupo.id_grupo == grupo_id).first()

    if not grupo:
        # se o grupo não foi encontrado
        error_msg = "Grupo não encontrado na base :/"
        return {"mesage": error_msg}, 404
    else:
        # retorna a representação de grupo
        return apresenta_grupo(grupo), 200


@app.delete('/grupo', tags=[grupo_tag],
            responses={"200": GrupoDelSchema, "404": ErrorSchema})
def del_grupo(query: GrupoBuscaSchema):
    """Deleta um Grupo a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
    grupo_id = query.id_grupo

    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Grupo).filter(Grupo.id_grupo == grupo_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        return {"mesage": "Grupo removido", "id": grupo_id}
    else:
        # se o grupo não foi encontrado
        error_msg = "Grupo não encontrado na base :/"
        return {"mesage": error_msg}, 404
    

