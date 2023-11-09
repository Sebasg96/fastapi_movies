from fastapi import FastAPI, Body #importacion
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional

class movie(BaseModel):
        id: Optional[int] 
        title: str 
        overview: Optional[str] = Field(min_length=10, max_length=50)
        year: int = Field(le= 2023)
        rating: Optional[float] = Field(default= 0.0,ge=0.0,le=10.0)
        category: str
