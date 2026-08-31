from typing import Callable
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from pdf_generator.services.dataRepository import DataRepository

from pdf_generator.visuals import templates
from pdf_generator.visuals import ellipses


Base = declarative_base()


class Template(Base):
    __tablename__ = "Template"

    id = Column("Id", Integer, primary_key=True)
    name = Column("Name", String(128), nullable=False)
    description = Column("Description", Text)
    wiki_page = Column("WikiPage", String(256))

    visuals = relationship("Visual", backref="template", lazy="dynamic")

    def __repr__(self):
        return f"Template(id={self.id}, name={self.name})"


class DataSource(Base):
    __tablename__ = "DataSource"

    id = Column("Id", Integer, primary_key=True)
    name = Column("Name", String(128), nullable=False)
    description = Column("Description", Text)

    visuals = relationship("Visual", backref="data_source", lazy="dynamic")

    def __repr__(self):
        return f"DataSource(id={self.id}, name={self.name})"


class Visual(Base):
    __tablename__ = "Visual"

    id = Column("Id", Integer, primary_key=True)
    name = Column("Name", String(128), nullable=False)
    data_source_args = Column("DataSourceArgs", JSON)

    template_id = Column(
        "TemplateId", Integer, ForeignKey("Template.Id"), nullable=False
    )
    data_source_id = Column(
        "DataSourceId", Integer, ForeignKey("DataSource.Id"), nullable=False
    )

    def __repr__(self):
        return f"Visual(id={self.id}, name={self.name})"

    def get_template(self) -> Callable:
        return getattr(templates, self.template.name)

    def get_data_source(self) -> Callable:
        return getattr(DataRepository, self.data_source.name)

    def get_ellipse(self) -> Callable:
        return getattr(ellipses, self.template.name)
