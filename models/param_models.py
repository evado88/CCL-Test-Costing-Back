
from typing import List, Optional
from pydantic import BaseModel

from models.instrument_model import Instrument
from models.reagent_model import Reagent
from models.test_model import TestWithDetail

class ParamTestDetail(BaseModel):
    reagents: List[Reagent]
    instruments: List[Instrument]
    test: Optional[TestWithDetail] = None

    class Config:
        orm_mode = True
