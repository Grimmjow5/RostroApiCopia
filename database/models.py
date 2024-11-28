from tortoise.models import Model
from tortoise import fields

class Empleado(Model):
  id = fields.IntField(primary_key=True)
  nickname = fields.CharField(max_length=30,unique=True)
  nombre = fields.CharField(max_length=60)
  nempleado = fields.IntField()
  correo = fields.CharField(max_length=60)
  telefono = fields.CharField(min_length=10,max_length=12)
  activo = fields.BooleanField(default=False)

  class Meta:
    table = "empleados"