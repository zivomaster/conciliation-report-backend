from pydantic import BaseModel, UUID4
from typing import List, Optional


# Datarules Schema
class DatarulesBase(BaseModel):
    type: str
    name: str
    description: str

class Datarules(DatarulesBase):
    datarules_id: Optional[UUID4] = None

class DatarulesCreate(DatarulesBase):
    datarules_id: Optional[UUID4] = None



# DatarulesDefinition Schema
class DatarulesDefinitionBase(BaseModel):
    id: Optional[UUID4]
    name: str
    description: str
    datarules: List[Datarules]

class DatarulesDefinitionCreate(DatarulesDefinitionBase):
    pass

class DatarulesDefinition(DatarulesDefinitionBase):
    pass

class DatarulesList(BaseModel):
    id: Optional[UUID4]
    name: str
    description: str