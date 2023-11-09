from pydantic import BaseModel, Field
from typing import Optional, List

#Field para vaidacion de datos

class movie(BaseModel):
        id: Optional[int] 
        title: str 
        overview: Optional[str] = Field(max_length=50)
        year: int = Field(le= 2023)
        rating: Optional[float] = Field(ge=0.0,le=10.0)
        category: str =Field(min_length= 3, max_length=15)

#Model_config se utiliza para dejar valores por defecto en el Basemodel
        model_config = {
           'json_schema_extra':{
                'example':{
                     "id":1,
                     'title': 'pelicula de prueba',
                     'overview': 'esta es una pelicula de prueba jeje',
                     'year': 1996,
                     'rating': 9.6,
                     'category' : 'Comedia'                
                }
           }  
        }
     
     

class movie_out(BaseModel):
        title: str
        overview: str | None
        year: int 
        rating: float | None 
        category: str