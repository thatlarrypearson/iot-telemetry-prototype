# telemetry/shared.py
# This file contains the data models for use by the telemetry application.
from datetime import datetime
from pydantic import BaseModel


class Source(BaseModel):
    id: int = None
    created: datetime = None
    name: str
    hash: str = None
    description: str = None

    # back propagation looks like a list of primary keys
    # attitudes: [int] = None

    class Meta:
        db_primary_key = 'id'
        db_autoincrement_primary_key = True
        db_indexes = ('name',)
        db_unique_indexes = ('id',)
        db_tablename_prefix = 'Orm'


# IOS Pythonista App motion library
class Gravity(BaseModel):
    id: int = None
    source: Source = ...
    created: datetime = None
    x: float
    y: float
    z: float

    class Meta:
        db_primary_key =  'id'
        db_autoincrement_primary_key = True
        db_unique_indexes = ['id',]


class UserAcceleration(BaseModel):
    id: int = None
    source: Source = ...
    created: datetime = None
    x: float
    y: float
    z: float

    class Meta:
        db_primary_key = 'id'
        db_autoincrement_primary_key = True
        db_unique_indexes = ('id',)


class Attitude(BaseModel):
    id: int = None
    source: Source = ...
    created: datetime = None
    roll: float
    pitch: float
    yaw: float

    class Meta:
        db_primary_key = 'id'
        db_autoincrement_primary_key = True
        db_unique_indexes = ('id',)


class MagneticField(BaseModel):
    id: int = None
    source: Source = ...
    created: datetime = None
    x: float
    y: float
    z: float
    accuracy: float

    class Meta:
        db_primary_key = 'id'
        db_autoincrement_primary_key = True
        db_unique_indexes = ('id',)

