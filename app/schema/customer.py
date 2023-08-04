from pydantic import BaseModel

class GetCustomer(BaseModel):
    userId: str
    campaign: str

    class Config:
        schema_extra = {
            "example": {
                "userId": "64b8d5ece92b3b72e4b249f1",
                "campaign": "test",
            }
        }
