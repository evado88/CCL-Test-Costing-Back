
from typing import Any, List, Optional
from pydantic import BaseModel

from models.instrument_model import Instrument
from models.lab_model import Lab
from models.reagent_model import Reagent
from models.test_model import TestWithDetail

class ParamTestDetail(BaseModel):
    labs: List[Lab]
    reagents: List[Reagent]
    instruments: List[Instrument]
    test: Optional[TestWithDetail] = None

    class Config:
        orm_mode = True
        
class ParamTestComponentDetail(BaseModel):
    component: str
    cost: float
    items: list[dict[str, Any]]=[]

    class Config:
        orm_mode = True    
        
class ParamTestCost(BaseModel):
    name: str
    lab: str
    total_cost: float
    components: list[ParamTestComponentDetail]=[]
    
    class Config:
        orm_mode = True
        
class ParamDashboard(BaseModel): 
    total_tests: int
    total_labs: int
    total_instruments: int
    total_reagents: int
    total_users: int
    tests: List[ParamTestCost] = []
    
    class Config:
        orm_mode = True
