
from pydantic import BaseModel
from typing import Union, Optional, List

class InputModel(BaseModel):
    batchid: str
    payload: List[List[int]]