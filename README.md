# HugPee #
HugPee simplifies the creation of RESTful CRUD endpoints in hug, for peewee models.

# Installing HugPee #

Installing Hugpee is very simple, just run:

```bash
pip3 install hugpee --upgrade
```

# Usage #

Consider a scenario where `Person` is our peewee model. Creating the CRUD endpoints for hug is very simple with HugPee:

```python
hugpee.HugPee(Person)
```

And then load them to hug.

```python
@hug.extend_api()
def get_all_hugs():
    return [modelendpoint]
```

Here is the full working example:

```python
import hug
from peewee import SqliteDatabase, Model
from peewee import PrimaryKeyField, CharField, DateField, BooleanField
import hugpee

db = SqliteDatabase(":memory:")

class Person(Model):
    ID = PrimaryKeyField()
    name = CharField()
    birthday = DateField()
    is_relative = BooleanField()
    class Meta:
        database = db

db.create_tables([Person])

hugpee.HugPee(Person)

@hug.extend_api()
def get_all_hugs():
    return [hugpee]

```

This will create the following endpoints:

| HTTP ACTION | URI(s)                 | Accepted Parameters             |
|-------------|------------------------|---------------------------------|
| POST        | /person                | name, birthday, is_relative     |
| GET         | /person , /person/{id} | id                              |
| PUT         | /person , /person/{id} | id, name, birthday, is_relative |
| DELETE      | /person , /person/{id} | id                              |

Note that the primary key, in this case the id, can be provided either as part of the URI or as a parameter.
