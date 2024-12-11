from flask import Blueprint, render_template,request, redirect
from app.modelsDto import EmpleadoDto, EmpleadoVideo, Verificando
from database.Repository import Repository
from reconocimiento.SaveImgs import SaveImgs

interfaceApi = Blueprint('interfaceApi', __name__,url_prefix='/interface')

@interfaceApi.route('/registrarV', methods=['GET', 'POST'])
async def registrarV():
    form = EmpleadoVideo(request.form)
    if request.method == 'POST' and form.validate():
      try:
        await Repository.SetEmpleadoVideo(form)
        if len(request.files) > 0:
          vifro = request.files['video']
          if vifro.filename != '':
            control = SaveImgs(form.nickname.data,"M")
            path = control.SaveFileVideo(vifro)
            control.ExtracImg(path)
            return redirect(request.url)
      except Exception as e:
        return render_template('registrar_video.html',form=form,error=e)
    else:
      empleados = await Repository.GetEmpleadosAll()
      fotos = []
      return render_template('registrar_video.html',form=form, error="", success="",empleado=empleados ,fotos=fotos )

@interfaceApi.route('/updateV/<idUser>', methods=['GET', 'POST'])
async def updatev(idUser):
    if request.method == 'GET':
      try:
        form = await Repository.GetEmpladoIdVideo(idUser)
        empleados = await Repository.GetEmpleadosAll()
        control = SaveImgs(form.nickname.data,"TMP")
        fotos = control.listarMuestrasSinPath()
        print(fotos)
        return render_template('registrar_video.html',form=form,error="", success="",empleado=empleados , fotos=fotos)
      except Exception as e:
        return render_template('registrar_video.html',form=form,error=e)

    form = EmpleadoVideo(request.form)
    if request.method == 'POST' and form.validate():
      try:
        empleados = await Repository.GetEmpleadosAll()
        await Repository.UpdateEmpleadoVideo(form)
        if len(request.files) > 0:
          vifro = request.files['video']
          if vifro.filename != '':
            control = SaveImgs(form.nickname.data,"M")
            path = control.SaveFileVideo(vifro)
            control.extract_faces_relevant_parts(path,30)
            return redirect(request.url)

        control = SaveImgs(form.nickname.data,"TMP")
        fotos = control.listarMuestrasSinPath()
        print(fotos)
        return render_template('registrar_video.html',form=form, error="", success="",empleado=empleados,fotos=fotos )
      except Exception as e:
        return render_template('registrar_video.html',form=form,error=e)
    else:
      empleados = await Repository.GetEmpleadosAll()
      return render_template('registrar_video.html',form=form, error="", success="",empleado=empleados )




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
          validacionExitosa = 0
          validaxionNoExitosa = 0
          for item in listFotos:
            result =control.Verificacion(item)
            if result == True:
              validacionExitosa = validacionExitosa + 1
            else :
              validaxionNoExitosa = validaxionNoExitosa + 1
          print("N. Exitoso "+ str(validacionExitosa))
          print("N. no Exitos0 " +str(validaxionNoExitosa))
          if validacionExitosa > validaxionNoExitosa:
            return render_template('verificacion.html',form=form, error="", success="Verificacion Exitosa")
          else:
            return render_template('verificacion.html',form=form, error="Verificacion no exitosa", success="")

      except Exception as e:
        return render_template('verificacion.html',form=form,error=e)
    else:
      return render_template('verificacion.html',form=form)