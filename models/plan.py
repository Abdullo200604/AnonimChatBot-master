from tortoise.models import Model
from tortoise import fields


class Plan(Model):
    id = fields.IntField(pk=True)
    user_id = fields.BigIntField()
    plan_time = fields.CharField(max_length=20, null=True)
    plan_text= fields.CharField(max_length=500, null=False)

    class Meta:
        table = "plans"