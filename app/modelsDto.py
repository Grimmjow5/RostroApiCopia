from wtforms import StringField, validators, Form, FileField, PasswordField, BooleanField,IntegerField
from flask_wtf import FlaskForm


class EmpleadoDto(FlaskForm):
  id = IntegerField('id', [validators.Optional()])
  nickname = StringField('Username', validators=[validators.Length(min=4)])
  nombre = StringField('Nombre Completo', [validators.Length(min=4)])
  correo = StringField('Correo', [validators.Length(min=6,max=30)])
  nEmpleado = IntegerField('Número de Empleado',[validators.NumberRange(min=100,max=1000000)])
  telefono = StringField('Número de Telefono',[validators.Length(min=10,max=12)])
  activo = BooleanField('Activo',default=False)
  foto1 = FileField('Foto 1:')
  foto2 = FileField('Foto 2:')
  foto3 = FileField('Foto 3:')



class Verificando(Form):
  nickname = StringField('Username', [validators.Length(min=4, max=25)])
  foto = FileField('Image File')
