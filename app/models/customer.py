from beanie import Document
from pydantic import Extra

class Customer(Document):
    campaign: str
    sso: str
    sso_id: str
    info: dict

    class Collection:
        name = "Customer"

    class Config:
        extra = Extra.allow
