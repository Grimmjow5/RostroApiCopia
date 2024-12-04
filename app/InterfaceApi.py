from flask import Blueprint, render_template,request, redirect
from app.modelsDto import EmpleadoDto, Verificando
from database.Repository import Repository
from reconocimiento.SaveImgs import SaveImgs

interfaceApi = Blueprint('interfaceApi', __name__,url_prefix='/interface')


@interfaceApi.route('/registrar', methods=['GET', 'POST'])
async def registrar():
    form = EmpleadoDto(request.form)
    if request.method == 'POST' and form.validate():
        try:
          await Repository.SetEmpleado(form)
          if len(request.files) >= 1:
            for i in range(len(request.files)):
              img = request.files[f"foto{i+1}"]
              if img.filename != '':
                control = SaveImgs(form.nickname.data,"M")
                path = control.SaveFile(img,i)
                print(path)
                control.FormatImg(path,i)
          clean= EmpleadoDto()
          return redirect(request.url)
        except Exception as e:
          return render_template('registrar.html',form=form,error=e)

    else:
      empleados = await Repository.GetEmpleadosAll()
      return render_template('registrar.html',form=form, error="", success="",empleado=empleados )

@interfaceApi.route('/update/<idUser>', methods=['GET', 'POST'])
async def update(idUser):
    if request.method == 'GET':
      try:
        form = await Repository.GetEmpladoId(idUser)
        empleados = await Repository.GetEmpleadosAll()

        return render_template('registrar.html',form=form,error="", success="",empleado=empleados )
      except Exception as e:
        return render_template('registrar.html',form=form,error=e)

    form = EmpleadoDto(request.form)
    if request.method == 'POST' and form.validate():
      try:
        empleados = await Repository.GetEmpleadosAll()
        await Repository.UpdateEmpleado(form)
        if len(request.files) >= 1:
          for i in range(len(request.files)):
            img = request.files[f"foto{i+1}"]
            if img.filename != '':
              control = SaveImgs(form.nickname.data,"M")
              path = control.SaveFile(img,i)
              print(path)
              control.FormatImg(path,i)

        return render_template('registrar.html',form=form, error="", success="",empleado=empleados )
      except Exception as e:
        return render_template('registrar.html',form=form,error=e)
    else:
      empleados = await Repository.GetEmpleadosAll()
      return render_template('registrar.html',form=form, error="", success="",empleado=empleados )


@interfaceApi.route('/verificar', methods=['GET', 'POST'])
async def verificar():
  if request.method == 'GET':
    form = Verificando()
    return render_template('verificacion.html',form=form, error="", success="")
  if request.method == 'POST':
    form = Verificando(request.form)
    if form.validate():
      try:
        valida = await  Repository.GetExistEmpleado(form.nickname.data)
        if valida == True:
          control = SaveImgs(form.nickname.data,"TMP")
          foto = request.files['foto']
          if foto.filename == "":
            raise Exception("No se ha seleccionado ninguna imagen")
          path = control.SaveFileTemp(foto)
          control.FormatImg(path,0)#Ya se guardo en tmp
          #Ahora hay que obtener todas las fotos ya guardadas en la base y sobre de este comparar, con las nuevas
          listFotos = control.listarMuestras()
          validacion = 0
          for item in listFotos:
            result =control.Verificacion(item)
            if result == True:
              validacion = validacion + 1
          if validacion >= 2:
            return render_template('verificacion.html',form=form, error="", success="Verificacion Exitosa")
          else:
            return render_template('verificacion.html',form=form, error="Verificacion no exitosa", success="")

      except Exception as e:
        return render_template('verificacion.html',form=form,error=e)
    else:
      return render_template('verificacion.html',form=form)