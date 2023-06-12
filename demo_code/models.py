# ruff: noqa: UP007
# ruff: noqa: UP006

import typing
import os

from sqlmodel import Field, Relationship, SQLModel, create_engine


POSTGRES_USER =  os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_DB = os.environ.get("POSTGRES_DB")

sql_url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"

if os.environ.get("RUNNING_IN_PRODUCTION", False):
    sql_url = f"{sql_url}?sslmode=require"

engine = create_engine(sql_url, echo=True)

def create_db_and_tables():
    return SQLModel.metadata.create_all(engine)

class CruiseDestinationLink(SQLModel, table=True):
    destination_id: typing.Optional[int] = Field(
        default=None,
        foreign_key="destination.id",
        primary_key=True,
    )
    cruise_id: typing.Optional[int] = Field(
        default=None,
        foreign_key="cruise.id",
        primary_key=True,
    )

class Destination(SQLModel, table=True):
    id: typing.Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: typing.Optional[str]
    cruises: typing.List["Cruise"] = Relationship(
        back_populates="destinations",
        link_model=CruiseDestinationLink,
    )

    def __str__(self):
        return f"{self.name}"

class Cruise(SQLModel, table=True):
    id: typing.Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: typing.Optional[str]
    destinations: typing.List["Destination"] = Relationship(
        back_populates="cruises",
        link_model=CruiseDestinationLink,
    )

    def __str__(self):
        return f"{self.name}"

class InfoRequest(SQLModel, table=True):
    id: typing.Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str
    notes: str
    cruise_id: int = Field (default=None, foreign_key="cruise.id")