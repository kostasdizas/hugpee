# HugPee #
HugPee simplifies the creation of RESTful CRUD endpoints in hug, for peewee models.

[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://pypi.python.org/pypi/hugpee/)


# Installing Hugpee #

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
import hug, peewee
import hugpee

class Person(Model):
    name = CharField()
    birthday = DateField()
    is_relative = BooleanField()

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
