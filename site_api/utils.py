import graphene
from django.db.models import Model
from graphql import GraphQLError
from typing import Callable


def save_obj(validator: Callable[[type, list], type], model_type:Model, command:dict[str, str], input:graphene.InputObjectType, exc_info:str=None) -> type: 
    if command.get('method') == 'create':
        try:
            _object:Model = model_type.objects.get(pk=input.pk)
        except model_type.DoesNotExist as e:
            raise GraphQLError(exc_info or f" {model_type.__name__} not found.") from e
    _fields = command.get('fields')
    _object = validator(_object, _fields)
    _object.save()
    return _object