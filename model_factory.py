# Model Factory
# telemetry/model_factory.py
# Dynamic SqlAlchemy Table Class Generator
# Meta Class Object
#
# Copyright (c) 2019 Larry B Pearson, San Antonio, Texas, USA - All Rights Reserved
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from datetime import datetime
from dateutil import parser
from inspect import getmro, isclass
from imp import new_module
from pydantic import BaseModel
from sqlalchemy import Table, Column, Sequence, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

def pluralize(s):
  from inflection import pluralize as p
  
  return_value = p(s)
  if return_value == s:
    return_value = return_value + "es"
  
  return return_value

def is_list(obj):
  if isinstance(obj, list):
    return True
  return False

def is_string(obj):
  if isinstance(obj, str):
    return True
  return False

def is_pydantic_model_class(cls):
  if not isclass(cls):
    return False
  if BaseModel not in getmro(cls):
    return False
  return True

def is_pydantic_model_instance(obj):
  if isinstance(obj, BaseModel):
    return True
  return False

def get_column_type(pydantic_type):
  if pydantic_type == int:
    return Integer
  elif pydantic_type == float:
    return Float
  elif pydantic_type == str:
    return String
  elif pydantic_type == datetime:
    return DateTime
  elif is_pydantic_model_class(pydantic_type):
    # Foreign Key data type
    return get_column_type(pydantic_type.__annotations__[pydantic_type.Meta.db_primary_key])

  return None

def generic_class_init_method(self, *args, **kwargs):

  if len(args) == 1:

    if not is_pydantic_model_instance(args[0]):
      raise TypeError("%s.__init__(): first positional argument must be a subclass of pydantic.BaseModel" % (self.__name__, ))

    pydantic_model_instance = args[0]
    for k, v in self.Meta.__annotations__.items():
      setattr(self, k, getattr(pydantic_model_instance, k, getattr(self, k, None)))

  else:

    for k in (self.Meta.schema())['required']:

      if k not in kwargs:
        cls = self.Meta.__annotations__[k]

        if is_pydantic_model_class(cls):
          # FK reference
          fk_column_name = (k + "_" + cls.Meta.db_primary_key).lower()
          if fk_column_name not in kwargs:
            raise ValueError("%s.__init__(): missing required FK named argument %s or %s" % (self.__class__.__name__, k, fk_column_name, ))

        else:

            raise ValueError("%s.__init__(): missing required named argument %s" % (self.__class__.__name__, k, ))

    for k, v in kwargs.items():
      setattr(self, k, v)

def generate_table_class(cls, Base, pk = None, cls_name_prefix = 'orm_'):
  if not is_pydantic_model_class(cls):
    raise TypeError('Class must inherit pydantic.BaseModel')
  
  pk = cls.Meta.db_primary_key
  schema = cls.schema()
  
  d = {
    '__tablename__': (cls_name_prefix + cls.__name__).lower(),
    '__init__': generic_class_init_method,
    'Meta': cls,
  }

  # Pydantic BaseModel class has 'schema' method returning a dictionary reflecting the model's information.
  # Class.schema()
  # Class.__annotations__ is a list of dictionaries containing keys representing
  # the field name and a Class identifying the field type
  #   {"key": Class}
  for k, v in cls.__annotations__.items():

    column_type = get_column_type(v)
    required = False
    if k in schema['required']:
      required = True

    if pk and pk == k and v is int and cls.Meta.db_autoincrement_primary_key:
      d[k] = Column(column_type, Sequence("%s_%s_seq" % (d['__tablename__'], k, )), primary_key = True)

    elif pk and pk == k and is_pydantic_model_class(v):
      raise ValueError("Pydantic Models can\'t be primary keys")

    elif pk and pk == k:
      if required:
        d[k] = Column(get_column_type(v), primary_key=True, nullable=False)
      else:
        d[k] = Column(get_column_type(v), primary_key=True)

    elif is_pydantic_model_class(v):
      # foreign key reference
      # https://docs.sqlalchemy.org/en/13/orm/tutorial.html
      # See 'Building a Relationship'
      fk_column_name = (k + "_" + v.Meta.db_primary_key).lower()
      if required:
        d[fk_column_name] = Column(get_column_type(v), ForeignKey("%s.%s" % ((cls_name_prefix + v.__name__).lower(), v.Meta.db_primary_key, )), nullable=False)
      else:
        d[fk_column_name] = Column(get_column_type(v), ForeignKey("%s.%s" % ((cls_name_prefix + v.__name__).lower(), v.Meta.db_primary_key, )))
      
      # https://docs.sqlalchemy.org/en/13/orm/relationship_api.html#sqlalchemy.orm.relationship
      # sqlalchemy.orm.relationship(argument, secondary=None, primaryjoin=None, secondaryjoin=None, foreign_keys=None, uselist=None, order_by=False, 
      #                             backref=None, 
      #                             back_populates=None, post_update=False, cascade=False, extension=None, viewonly=False, lazy='select', collection_class=None, 
      #                             passive_deletes=False, passive_updates=True, remote_side=None, enable_typechecks=True, join_depth=None, comparator_factory=None, 
      #                             single_parent=False, innerjoin=False, distinct_target_key=None, doc=None, active_history=False, cascade_backrefs=True, 
      #                             load_on_pending=False, bake_queries=True, _local_remote_pairs=None, query_class=None, info=None, omit_join=None)
      # d[k] = relationship((cls_name_prefix + v.__name__), back_populates=pluralize(cls_name_prefix + v.__name__).lower())
      d[k] = relationship((cls_name_prefix + v.__name__))

    else:

      if required:
        d[k] = Column(get_column_type(v), nullable=False)
      else:
        d[k] = Column(get_column_type(v))


  # https://medium.freecodecamp.org/dynamic-class-definition-in-python-3e6f7d20a381
  # But, with three arguments, type() returns a whole new type object. This is equivalent to defining a new class.
  # NewClass = type('NewClass', (object,), {})
  # The first argument is a string that gives the new class a name
  # The next is a tuple, which contains any base classes the new class should inherit from
  # The final argument is a dictionary of attributes specific to this class
  NewClass = type(cls_name_prefix + cls.__name__, (Base,), d)

  return NewClass

