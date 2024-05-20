from pydantic import BaseModel
from typing import Union, Optional, List

class OutputModel(BaseModel):
    batchid: str
    response: List[int]
    status: str
    started_at:str
    completed_at:str