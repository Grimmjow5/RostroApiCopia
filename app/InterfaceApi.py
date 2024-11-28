from flask import Blueprint, render_template,request, redirect
from app.modelsDto import EmpleadoDto
from database.Repository import Repository

interfaceApi = Blueprint('interfaceApi', __name__,url_prefix='/interface')


@interfaceApi.route('/registrar', methods=['GET', 'POST'])
async def registrar():
    form = EmpleadoDto(request.form)
    if request.method == 'POST' and form.validate():
        try:
          await Repository.SetEmpleado(form)
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
        return render_template('registrar.html',form=form, error="", success="",empleado=empleados )
      except Exception as e:
        return render_template('registrar.html',form=form,error=e)
    else:
      empleados = await Repository.GetEmpleadosAll()
      return render_template('registrar.html',form=form, error="", success="",empleado=empleados )