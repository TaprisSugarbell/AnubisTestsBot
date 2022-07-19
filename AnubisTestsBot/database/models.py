from tortoise import fields
from tortoise.models import Model


class UserID(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()


