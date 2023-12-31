from fastapi import FastAPI, Path, Query, status, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Any, Coroutine, Optional, List
from starlette.requests import Request
from config import create_fastapi_config
from data import movies
from models import User, movie,movie_out
from JWTmanager import create_token, validate_token
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from auth import JWTBearer
from config_db.database import select_all_movies
app = FastAPI() #Instancia de fastAPI
create_fastapi_config(app)


@app.get('/', tags=['Home']) #parametro tags para agrupar rutas en la app diferencia en Swagger
def message():
    return HTMLResponse('<head> <title>Mi página de ejemplo</title> </head><body>Aquí va el contenido</body>')

#status_code para asignar un codigo HTTP especifico
#dependencies, es una lista de clases dependientes para que se corra este endpoint -> JWTbearer fue nuestra funcion creada para validar ver auth
'''response_model= List[movie_out]'''
@app.get('/movies', tags=['movies'],status_code=status.HTTP_202_ACCEPTED,
          dependencies=[Depends(JWTBearer())]) #List importado para retomar una lista de los modelos de salida
async def get_movies(): #->  List[movie_out]: #tambien podemos declarar el modelo de salida en la funcion
    
    return select_all_movies()

#pamaetro de ruta {id} #basemodel nos puede ayudar a crear un tipo de respusta
@app.get('/movies/{id}', tags=['movies'])
def get_movie(id:int =Path(ge=1,le=2000)) -> movie_out: #declarar modelo de respuesta en la funcion o en el decorador
    for movie in movies:
        if movie['id'] == id:
            return movie
    return JSONResponse('la pelicula no existe',status_code=status.HTTP_404_NOT_FOUND)

#parametro query al no informar en la ruta del endpoint
#cuando vamos a recibir un query param agregar / al final
#para agregar mas params, los asociamos en la funcion , 
# el : despues del param especifica el tipo 
#Query para validacion de parametros
@app.get('/movies/', tags=['movies'])
def get_movie_by_category(category:str = Query(min_length=5,max_length=15))->  List[movie_out]:
    return [movie for movie in movies if movie['category'] == category]

@app.post('/movies', tags=['movies'])
def create_new_movie(movie: movie) -> dict:
     movies.append(dict(movie)) #model_dummp transforma el objeto en diccionario
     return {'content':'se ha registrado la peli con exito'}


@app.put('/movies/{id}', tags=['movies'])
async def update_movie(id:int,movie: movie_out) -> List[movie_out]:
     for  item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
        return movies    

@app.delete('/movies/{id}', tags=['movies'])
def delete_movie(id:int):
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
    return movies


#Metodo login que crea un token bearer, para autenticarse en endpoints que lo requieran
@app.post('/login', tags=['auth'])
def login(user:User):
    if user.email == 'admin@jep.gov.co' and user.password == 'admin123':
        token : str = create_token(user.dict())
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED,content=token) 

