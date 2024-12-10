import asyncio
from tortoise import Tortoise,run_async


async def init():
  await Tortoise.init(
    db_url='psycopg://root:YjKaPOA96Hx5QLjMeLJ4mNsHBpWPlDFu@dpg-ctc70utumphs73b20m60-a/empleados_eju9',
    #db_url='mysql://root:@localhost:3306/empleados',
    modules={"models": ['database.models']}
  )
  await Tortoise.generate_schemas()
  #No recuerdo para que es esta linea
  Tortoise.init_models(['database.models'],'models')
  await Tortoise.close_connections()


asyncio.run(init())
#run_async(init())