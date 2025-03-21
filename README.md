# IOT Telemetry Prototype - README

When forced to work with [Domain specific languages (DSL)](https://en.wikipedia.org/wiki/Domain-specific_language) such as the data modeling languages [YANG](https://en.wikipedia.org/wiki/YANG) and [NETCONF](https://en.wikipedia.org/wiki/NETCONF), I was left feeling a little dirty.  Often DSL's aren't useful outside of their domain.  Before the Internet web era began, YANG and NETCONF could have been good langauges had they been developed back then and widely implemented in Internet netorking equipment.  YANG and NETCONF have not  proven to be extensible outside of switch/router configuration and they are not widely implemented.

One example of a ganeral purpose data modeling language can be found in the Python [Django Frameowrk](https://www.djangoproject.com/)'s [models](https://docs.djangoproject.com/en/2.2/topics/db/models/) subsystem.  Django declarative models are built by adding properties to a class definition to represent tables in a relational database management system (RDBMS).  The classes can then be used for a variety of other purposes including runtime user interface (UI), web view, REST API (and more) generation.  Django models are an architectural cornerstone component so you [Don't Repeat Yourself (DRY)](https://www.webforefront.com/django/designprinciples.html).  From a data model, much of an application built on the Django Framework can be automatically derived.

Not only is the Django data model extensible, the model implementation is also extensible including the ability to make runtime dynamic changes to the model when needed.  These extensibility related [non-functional requirements](https://en.wikipedia.org/wiki/Non-functional_requirement) are built into the entire framework and explains why Django is such a popular framework.

Recently, [Python Bytes](https://pythonbytes.fm/) podcast hosts Michael Kennedy and Brian Okken described [pydantic](https://pydantic-docs.helpmanual.io/), an extensible data modeling language.  In the same podcast, they described [FastAPI](https://fastapi.tiangolo.com/), an async web framework that runs on [uvicorn](https://www.uvicorn.org/), an async web server.  The FastAPI framework can use pydantic models to automatically create much of a REST API.

It occured to me that [requests](https://2.python-requests.org/en/master/), [SQLAlchemy](https://www.sqlalchemy.org/), pydantic, FastAPI and uvicorn could form the foundation for a framework that could automatically derive the following from pydantic models:

- REST clients
- REST servers with databases integration

This prototype explores the if and how this could be done.

The first step in the process has been to write a function to dynamically create SQLAlchemy [ORM](https://en.wikipedia.org/wiki/Object-relational_mapping) Table classes that can be used to create database tables from pydantic models as well as perform table operations like add, update, delete, change and join.  I'm refactoring the function and will probably continuing refactoring iteratively until it is stable.

## Run The Prototype

From the source directory, run ```pytest``` or run ```python3 test_db_factory.py```.

## Files

- model_factory.py
  contains functions needed to create [SQLAlchemy](https://www.sqlalchemy.org/) ORM table classes from [pydantic](https://pydantic-docs.helpmanual.io/) models.

- README.md
  This file.

- main.py
  [FastAPI](https://fastapi.tiangolo.com/) framework test code.  A running server can be creaated by running ```uvicorn main:app --reload```.  Swagger API can be reached at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

- server.py
  [FastAPI](https://fastapi.tiangolo.com/) framework test code for defining REST APIs generated by [pydantic](https://pydantic-docs.helpmanual.io/) models.  This is just a stub and is currently untested.

- shared.py
  [pydantic](https://pydantic-docs.helpmanual.io/) models of a portion of the expected telemetry data.

- test_db_factory.py
  [pytest](https://docs.pytest.org/en/latest/) compatible test code. 
 
- test_example1.db 
  temporary [SQLite](https://sqlite.org/index.html) database file.

- test_example2.db
  temporary [SQLite](https://sqlite.org/index.html) database file.

- test_one.db
  temporary [SQLite](https://sqlite.org/index.html) database file.

## Dependencies

The following ```pip install```s need to be done.

```bash
cd <source code directory>
pipenv shell
pipenv install pytest uvicorn fastapi pydantic SQLAlchemy num2words python-dateutil
```

## Available Under MIT License

Copyright (c) 2019 Larry B Pearson, San Antonio, Texas, USA - All Rights Reserved

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
