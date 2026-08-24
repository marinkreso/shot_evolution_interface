from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from pdf_generator.models.db_models import Base, DataSource, Template, Visual


class ReportMetaDataRepository:
    def __init__(self, connection_str: str):
        self.connection_str = connection_str
        self.binded = False

    def establish_db_connection(self):
        self._engine = create_engine(self.connection_str)

        # Creates a database if it doesn't exist
        Base.metadata.create_all(self._engine)

        self._session = Session(self._engine)
        self.binded = True

    def get_object(self, model: Base, pk: int) -> Optional[Base]:
        """
        Fetch objects from the database by it's primary key
        """
        if not self.binded:
            self.establish_db_connection()

        fetched_object = self._session.query(model).get(pk)
        return fetched_object

    def get_all_visuals(self):
        if not self.binded:
            self.establish_db_connection()

        return self._session.query(Visual).all()

    def get_visual_by_id(self, id: int):
        visual = self.get_object(Visual, id)
        return visual

    def get_template_by_id(self, id: int):
        template = self.get_object(Template, id)
        return template

    def get_datasource_by_id(self, id: int):
        datasource = self.get_object(DataSource, id)
        return datasource
