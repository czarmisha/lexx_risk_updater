from pydantic import BaseModel


class UpdateAccount(BaseModel):
    max_loss: int | None = None
    max_loss_close: int | None = None
    buying_power: int | None = None
    day_pos_investment: int | None = None
