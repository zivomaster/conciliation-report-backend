
from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from app.models import Datarules, DatarulesDefinition
from app import schemas
from app.crud.base import CRUDBase
import uuid

class CRUDDatarules(CRUDBase[Datarules, schemas.DatarulesDefinitionCreate, schemas.DatarulesDefinitionBase]):
    
    def get_datarules_definition(self, db: Session, datarules_definition_id=uuid):
        return db.query(DatarulesDefinition).filter(DatarulesDefinition.datarules_definition_id == datarules_definition_id).first()
    
    def get_datarules(self, db: Session, datarules_definition_id=uuid)->list[schemas.Datarules]:
        dt = db.query(Datarules).filter(Datarules.datarules_definition_id==datarules_definition_id).all()
        lst=[]
        for item in dt:
            tmp = schemas.Datarules(
                type=item.type,
                name=item.name,
                description=item.description,
                datarules_id=item.datarules_id
            )
            lst.append(tmp)

        return lst
    
    def create_datarules_definition(self, db: Session, 
                                    datarules_def: schemas.DatarulesDefinitionCreate)->schemas.DatarulesDefinition:
        datarules_def_created = DatarulesDefinition(
            name=datarules_def.name,
            description=datarules_def.description
        )
        # create datarules_definition
        db.add(datarules_def_created) 
        db.commit()
        db.refresh(datarules_def_created)
        # get it


        datarules_definition_id = datarules_def_created.datarules_definition_id
        
        datarules_list = []
        for datarules in datarules_def.datarules:
            #create datarules
            datarules_created = self.create_datarules(db,datarules=datarules,datarules_definition_id=datarules_definition_id)
            datarules_list.append(datarules_created)
    
        return schemas.DatarulesDefinition(id=datarules_definition_id,
                                           name=datarules_def_created.name,
                                           description=datarules_def_created.description,
                                           datarules=datarules_list)


    def create_datarules(self, db: Session,
                         datarules: schemas.DatarulesCreate,
                         datarules_definition_id=uuid)->schemas.Datarules:
        datarules_created =  Datarules(
           type=datarules.type,
           name=datarules.name,
           description=datarules.description,
           datarules_definition_id=datarules_definition_id
        )
        db.add(datarules_created)
        db.commit()
        db.refresh(datarules_created)
        return schemas.Datarules(
            datarules_id=datarules_created.datarules_id,
            type=datarules_created.type,
            name=datarules_created.name,
            description=datarules_created.description
        )
        
    def update_datarules_definition(self, db: Session, 
                                    updated_datarules_def: schemas.DatarulesDefinition,
                                    datarules_definition_id=uuid, 
                                   ) -> schemas.DatarulesDefinition:
      # Fetch the datarules definition by its ID
        db_datarules_upd = db.query(DatarulesDefinition).filter(DatarulesDefinition.datarules_definition_id == datarules_definition_id).first()
        if db_datarules_upd:
            # Update the datarules definition attributes
            db_datarules_upd.name=updated_datarules_def.name
            db_datarules_upd.description=updated_datarules_def.description
            db.commit()
            db.refresh(db_datarules_upd)
            print("Updated DataRulesDefinition")
            datarules_definition_id = db_datarules_upd.datarules_definition_id
        
            datarules_list = []
            for datarules in updated_datarules_def.datarules:
                #update datarules
                datarules
                datarules_up = self.update_datarules(db,
                                                     datarules=datarules,
                                                     datarules_definition_id=datarules_definition_id,
                                                     datarules_id=datarules.datarules_id)
                datarules_list.append(datarules_up)
            print("Updated DataRules")
            return schemas.DatarulesDefinition(id=datarules_definition_id,
                                           name=db_datarules_upd.name,
                                           description=db_datarules_upd.description,
                                           datarules=datarules_list)
           
        return None  # Handle the case when the datarules definition ID doesn't exist

    def update_datarules(self, db: Session,
                         datarules: schemas.DatarulesCreate,
                         datarules_definition_id=uuid,
                         datarules_id:int = 0)->schemas.Datarules:
        # Fetch the datarules by its ID
        db_datarules = db.query(Datarules).filter(Datarules.datarules_id == datarules_id and Datarules.datarules_definition_id==datarules_definition_id).first()

        if db_datarules:
            db_datarules.type=datarules.type,
            db_datarules.name=datarules.name,
            db_datarules.description=datarules.description
            db.commit()
            db.refresh(db_datarules)
            return schemas.Datarules(
                datarules_id=db_datarules.datarules_id,
                type=db_datarules.type,
                name=db_datarules.name,
                description=db_datarules.description
            )
        return None  # Handle the case when the datarules ID doesn't exist
    
    
    def get_all_datarules_definitions(self, db: Session)->list[schemas.DatarulesList]:
        # Fetch the datarules by its ID
        all_data = []
        df_all = db.query(DatarulesDefinition).all()
        for fetch in df_all:
            tmp = schemas.DatarulesList(id=fetch.datarules_definition_id,
                                           name=fetch.name,
                                           description=fetch.description)
            all_data.append(tmp)
        return all_data
    
    def get_datarules_definitions_by_id(self, db: Session,datarules_definition_id=uuid)->schemas.DatarulesDefinition:
        # Fetch the datarules by its ID
        df_search = self.get_datarules_definition(db,datarules_definition_id=datarules_definition_id)
        return schemas.DatarulesDefinition(id=df_search.datarules_definition_id,
                                           name=df_search.name,
                                           description=df_search.description,
                                           datarules=self.get_datarules(db,datarules_definition_id=df_search.datarules_definition_id))

    def delete_datarules(self, db: Session, datarules_definition_id=uuid):
        df_delete = self.get_datarules_definition(db,datarules_definition_id=datarules_definition_id)
        db.delete(df_delete)
        db.commit()
        return {"message": f"homologacion: {datarules_definition_id} eliminada correctamente."}

datarules = CRUDDatarules(Datarules)