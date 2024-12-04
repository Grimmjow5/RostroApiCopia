from flask import Flask, render_template, request, Blueprint

from app.modelsDto import Verificando
from database.Repository import Repository
from reconocimiento.SaveImgs import SaveImgs


api = Blueprint('api', __name__,url_prefix='/api')

@api.post('/verificar')
async def verificarface():
  try:
    form = Verificando(request.form)
    if form.validate():
      existe = await Repository.GetExistEmpleado(form.nickname.data)
      if existe == False:
        return "no existe, usuario",404
      control = SaveImgs(form.nickname.data,"TMP")
      foto = request.files['foto']
      path = control.SaveFileTemp(foto)
      control.FormatImg(path,0)#Ya se guardo en tmp
      #Ahora hay que obtener todas las fotos ya guardadas en la base y sobre de este comparar, con las nuevas
      listFotos = control.listarMuestras()
      print(listFotos)
      validacion = 0
      for item in listFotos:
        result =control.Verificacion(item)
        if result == True:
          validacion = validacion + 1
      if validacion >= 2:
        return "success",200
      else:
        return "no autorizado",401
  except Exception as e:
    return e
