"""
HugPee simplifies the creation of RESTful CRUD endpoints in hug, for peewee models.
"""

from functools import wraps
import hug

from peewee import DoesNotExist, IntegrityError
from playhouse.shortcuts import model_to_dict


def cpartial(func, *a, **k):
    @wraps(func)
    def partial_func(*args, **kwargs):
        return func(*(a + args), **dict(k, **kwargs))
    return partial_func


class HugPee(object):

    def __init__(self, model, base=None):
        self.model = model
        self.base = model.__name__.lower() if not base else base
        # retrieve primary key and fields
        self.all = [field for field in self.model._meta.fields]
        self.pk_n = self.model._meta.primary_key.name
        self.pk = [self.pk_n]
        self.pk_d = {self.pk_n: None}
        self.fields = [field for field in self.all if field not in self.pk]
        self.fields_d = {field: None for field in self.fields}
        # use skeletons to create crud methods for model
        self._make_methods()
        # register endpoints
        self._register_endpoints()

    def _make_methods(self):
        """Using the skeleton methods, generate methods with the required parameters"""
        self.create = cpartial(self.create_skeleton, *self.fields)
        self.read = cpartial(self.read_skeleton, self.pk)
        self.update = cpartial(self.update_skeleton, *self.all)
        self.delete = cpartial(self.delete_skeleton, *self.pk)

    def _register_endpoints(self):
        """Manually call the decorator function to register the generated CRUD methods."""
        hug.call(accept=['post'],
                 urls=["/{0}".format(self.base)],
                 parameters=self.fields
                 )(self.create)
        hug.call(accept=['get'],
                 urls=["/{0}".format(self.base), "/{0}/{{{1}}}".format(self.base, self.pk_n)],
                 parameters=self.pk,
                 defaults=self.pk_d,
                 )(self.read_skeleton)
        hug.call(accept=['put'],
                 urls=["/{0}".format(self.base), "/{0}/{{{1}}}".format(self.base, self.pk_n)],
                 parameters=self.all,
                 defaults=self.fields_d,
                 )(self.update)
        hug.call(accept=['delete'],
                 urls=["/{0}".format(self.base), "/{0}/{{{1}}}".format(self.base, self.pk_n)],
                 parameters=self.pk
                 )(self.delete)

    def create_skeleton(self, *args, **kwargs):
        """Create a new record"""
        # check that FK constraints are met
        error = False
        error_messages = []
        # check foreign key constraints
        for key in kwargs:
            if key in self.model._meta.rel:
                # make sure other model exists
                x = self.model._meta.rel[key].model_class
                try:
                    print("trying to find {0} with id: {1}".format(key, kwargs[key]))
                    y = x.get(x._meta.primary_key == kwargs[key])
                    kwargs[key] = y  # optional, but since the object was retrieved, it can be used as reference.
                except x.DoesNotExist:
                    error = True
                    error_messages.append({
                                          "message": "{0} with id: {1} was not found".format(key, kwargs[key]),
                                          "code": 404
                                          })
        try:
            new = self.model.create(**kwargs)
        except IntegrityError:
            error = True
            error_messages.append({
                                  "message": "{0} could not be created. Bad foreign key?".format(self.model.__name__),
                                  "code": 404
                                  })

        # make new entry based on model
        if not error:
            message = {"success": "created new entry", "model": model_to_dict(new)}
        else:
            message = {"errors": error_messages}
        #
        return {self.base: message}

    def read_skeleton(self, *args, **kwargs):
        """Retrieve a record"""
        key = kwargs[self.pk_n] if self.pk_n in kwargs else args[0] if len(args) > 0 else None
        if key:
            x = self.model.get(self.model._meta.fields[self.pk_n] == key)
            result = {self.base: model_to_dict(x)}
        else:
            x = self.model.select()
            result = {self.base: [model_to_dict(r) for r in x]}
        return {self.base: result}

    def update_skeleton(self, *args, **kwargs):
        """Update an existing record"""
        key = kwargs[self.pk_n] if self.pk_n in kwargs else args[0] if len(args) > 0 else None
        error = False
        error_messages = []
        # check foreign key constraints
        for keyy in kwargs:
            if keyy in self.model._meta.rel:
                # make sure other model exists
                x = self.model._meta.rel[keyy].model_class
                try:
                    print("trying to find {0} with id: {1}".format(keyy, kwargs[keyy]))
                    y = x.get(x._meta.primary_key == kwargs[keyy])
                    kwargs[keyy] = y  # optional, but since the object was retrieved, it can be used as reference.
                except x.DoesNotExist:
                    error = True
                    error_messages.append({
                                          "message": "{0} with id: {1} was not found".format(keyy, kwargs[keyy]),
                                          "code": 404
                                          })
        try:
            x = self.model.get(self.model._meta.fields[self.pk_n] == key)
            for field in self.fields:
                if field in kwargs and kwargs[field]:
                    x._data[field] = kwargs[field]
            x.save()
        except DoesNotExist:
            error = True
            error_messages.append({
                                  "message": "{0} with key: {1} was not found".format(self.model.__name__, key),
                                  "code": 404
                                  })
        #
        if not error:
            message = {"success": "updated entry", "model": model_to_dict(x)}
        else:
            message = {"errors": error_messages}
        #
        return {self.base: message}

    def delete_skeleton(self, *args, **kwargs):
        """Delete an existing record"""
        key = kwargs[self.pk_n] if self.pk_n in kwargs else args[0] if len(args) > 0 else None
        error = False
        error_messages = []
        try:
            x = self.model.get(self.model._meta.fields[self.pk_n] == key)
            x.delete_instance()
        except DoesNotExist:
            error = True
            error_messages.append({
                                  "message": "{0} with key: {1} was not found".format(self.model.__name__, key),
                                  "code": 404
                                  })
        except IntegrityError:
            error = True
            error_messages.append({
                                  "message": "{0} with key: {1} could not be deleted".format(self.model.__name__, key),
                                  "code": 404})
        #
        if not error:
            message = {"success": "deleted entry", "model": model_to_dict(x)}
        else:
            message = {"errors": error_messages}
        #
        return {self.base: message}
