from pydantic import BaseModel


class ChartDataCell(BaseModel):
    label: str
    color: str
    value: float
    