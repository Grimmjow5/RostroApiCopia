from app.modelsDto import EmpleadoDto
from .models import Empleado
from tortoise import Tortoise

class Repository:

  async def SetEmpleado(empleado:EmpleadoDto):
    try:
      print(empleado.nEmpleado.data)
      try:
        pp = int(empleado.telefono.data)
      except:
        raise Exception("Telefono no valido, solo debe de tener 10 digitos, númericos")
      emplado = Empleado(
        nickname=empleado.nickname.data.lower().strip(),
        nombre=empleado.nombre.data,
        correo=empleado.correo.data,
        nempleado=empleado.nEmpleado.data,
        telefono=empleado.telefono.data,
        activo=empleado.activo.data
      )
      await emplado.save()
      await Tortoise.close_connections()
    except Exception as e:
      await Tortoise.close_connections()
      raise Exception(e)

  async def UpdateEmpleado(empleado:EmpleadoDto):
    try:
      try:
        pp = int(empleado.telefono.data)
      except Exception as e:
        raise Exception("Telefono no valido, solo debe de tener 10 digitos, númericos")

      await Empleado.filter(id=empleado.id.data).update(
        nickname=empleado.nickname.data,
        nombre=empleado.nombre.data,
        correo=empleado.correo.data,
        nempleado=empleado.nEmpleado.data,
        telefono=empleado.telefono.data,
        activo=empleado.activo.data
      )
      await Tortoise.close_connections()
    except Exception as e:
      await Tortoise.close_connections()
      raise Exception(e)


  async def GetExistEmpleado(nickname:str)->bool:
    try:
      print("Buscando un empleado")
      empleado = await Empleado.filter(nickname=nickname).first()
      await Tortoise.close_connections()
      if empleado == None:
        print("No existe empleado")
        return False
      print("Existe empleado")
      return True
    except Exception as e:
      await Tortoise.close_connections()
      return False
  async def GetEmpladoId(id:int)->EmpleadoDto:
    try:
      empleado = await Empleado.get(id=id)
      await Tortoise.close_connections()
      empleadoDto = EmpleadoDto(
        id=empleado.id,
        nickname=empleado.nickname,
        nombre=empleado.nombre,
        correo=empleado.correo,
        nEmpleado=empleado.nempleado,
        telefono=empleado.telefono,
        activo=empleado.activo
      )
      return empleadoDto
    except Exception as e:
      await Tortoise.close_connections()
      raise Exception(e)

  async def GetEmpleadosAll():
    try:
      empleados = await Empleado.all()
      await Tortoise.close_connections()
      return empleados
    except Exception as e:
      await Tortoise.close_connections()
      raise Exception(e)