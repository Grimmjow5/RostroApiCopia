import asyncio
from tortoise import Tortoise,run_async


async def init():
  await Tortoise.init(
    db_url='mysql://root:@localhost:3306/RostrosEmpleados',
    modules={"models": ['database.models']}
  )
  await Tortoise.generate_schemas()
  #No recuerdo para que es esta linea
  Tortoise.init_models(['database.models'],'models')
  await Tortoise.close_connections()


asyncio.run(init())
#run_async(init())