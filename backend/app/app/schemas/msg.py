import pandas as pd
from pydantic import BaseModel


class Msg(BaseModel):
    msg: str
