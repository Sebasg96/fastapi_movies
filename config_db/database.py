from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, Session, select    

#clase declarada para la creacion de la tabla movies table = True
class Movies(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key= True)
    title: str 
    overview: Optional[str] 
    year: int
    rating: Optional[float] = None
    category: str    

sqlite_file_name = 'database.db'
sqlite_url = f"sqlite:///{sqlite_file_name}"
#Echo para que todos los statemes sql se impriman en la terminal
engine = create_engine(sqlite_url, echo=True)

#Whenever you create a class that inherits from SQLModel and is configured with 
#table = True, it is registered in this metadata attribute.

# create_all -> It takes an engine and uses it to create the database and all the tables 
# registered in this MetaData object.

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_movie():
    movie_1 = Movies(title='piratas del caribe', overview='Jack Sparrow el pirata ...',year=2012,rating=9.0,category='Accion')
    movie_2 = Movies(title='Big Momma', overview='un agente secreto ...',year=2004,rating=8.0,category='Comedia')
    movie_3 = Movies(title='la Momia', overview='un explorador descubre...',year=2010,rating=7.5,category='Aventura')

    session = Session(engine)

    session.add(movie_1)
    session.add(movie_2)
    session.add(movie_3)

    session.commit()

def select_all_movies():
    with Session(engine) as session:
        all_movies = session.exec(select(Movies)).all()
    return all_movies

def main():
    create_db_and_tables()
    create_movie()
    select_all_movies()

if __name__ == "__main__":
    main()

