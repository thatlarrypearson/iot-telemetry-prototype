# test_db_factory.py
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

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from shared import Source, Gravity
from model_factory import generate_table_class
from sqlalchemy import Table, Column, Integer, String, DateTime, Float, MetaData, ForeignKey
from num2words import num2words
from datetime import datetime


class TestExample(object):
    def test_example1(self):
        # engine = create_engine('sqlite:///:memory:')
        engine = create_engine('sqlite:///test_example1.db', echo=True)
        Base = declarative_base()
        Session = sessionmaker(bind=engine)

        user = Table('user', Base.metadata,
            Column('user_id', Integer, primary_key=True),
            Column('user_name', String(16), nullable=False),
            Column('email_address', String(60), key='email'),
            Column('nickname', String(50), nullable=False)
        )

        user_prefs = Table('user_prefs', Base.metadata,
            Column('pref_id', Integer, primary_key=True),
            Column('user_id', Integer, ForeignKey("user.user_id"), nullable=False),
            Column('pref_name', String(40), nullable=False),
            Column('pref_value', String(100))
        )

        Base.metadata.create_all(engine)
    
    def test_example2(self):
        engine = create_engine('sqlite:///test_example2.db', echo=True)
        Base = declarative_base()
        Session = sessionmaker(bind=engine)


        class School(Base):
            __tablename__ = "woot"
            id = Column(Integer, primary_key=True)
            name = Column(String)  

            def __init__(self, id, name):
                self.id = id
                self.name = name


        Base.metadata.create_all(engine)
        s1 = School(id=1, name='first')
        s2 = School(id=2, name='second')
        s3 = School(id=3, name='third')
        s4 = School(id=4, name='fourth')
        session = Session()
        session.add(s1)
        session.add_all([s2, s3, s4])
        session.commit()
        for row in session.query(School).order_by(School.name):
            print(row.id, row.name)


class TestModelFactory(object):
    def test_one(self):
        from model_factory import is_list, is_string
        assert(is_list([]))
        assert(not is_list(9))
        assert(not is_list(None))
        assert(is_list([1,2,3,4,]))
        assert(not is_list("this is a string"))
        assert(is_string(u"this is a string"))
        assert(is_string(r"this is a string"))
        assert(is_string("this is a string"))
        assert(not is_string(1))
    
    def test_two(self):
        from pydantic import BaseModel

        right_now = datetime.utcnow()

        class Source(BaseModel):
            id: int = None
            created: datetime = None
            name: str
            hash: str = None
            description: str = None

            # back propagation looks like a list of primary keys
            # attitudes: [int] = None
            # attitudes: list(int) = None
            # attitudes: list()
            # attitudes: []
            # attitudes: int

            class Meta:
                db_primary_key = 'id'
                db_autoincrement_primary_key = True
                db_indexes = ('name',)
                db_unique_indexes = ('id',)
                db_tablename_prefix = 'Orm'


        class Attitude(BaseModel):
            id: int = None
            source: Source = ...
            created: datetime = right_now
            roll: float
            pitch: float = 0.0
            yaw: float = 0.0

            class Meta:
                db_primary_key = 'id'
                db_autoincrement_primary_key = True
                db_unique_indexes = ('id',)
                db_tablename_prefix = 'Orm'
                # db_back_populate_relations = [['Source','attitudes'], ]


        engine = create_engine('sqlite:///test_two.db', echo=True)
        Session = sessionmaker(bind=engine)
        Base = declarative_base()

        source_table_class = generate_table_class(Source, Base)
        Base.metadata.create_all(engine)

        attitude_table_class = generate_table_class(Attitude, Base)
        Base.metadata.create_all(engine)

        session = Session()
        source_table_row = source_table_class(name='test row')
        session.add(source_table_row)
        session.commit()

        attitude_table_row = attitude_table_class(source_id=source_table_row.id, roll=1.0, pitch=2.0, yaw=2.0)
        session.add(attitude_table_row)
        session.commit()
        attitude_table_row.yaw = 3.0
        session.commit()
 

if __name__ == '__main__':
    t = TestModelFactory()
    t.test_one()
    t.test_two()
    # t.test_three()
    # t.test_four()
