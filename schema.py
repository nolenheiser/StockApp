#Imports

from pydantic import BaseModel

#CONSTANTS


#Functions

class PriceNormalized(BaseModel):
    date: str
    close: float
