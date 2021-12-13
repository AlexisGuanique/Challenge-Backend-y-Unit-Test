from pymongo import MongoClient


MONGO_URL = 'mongodb://localhost'
prueba = MongoClient(MONGO_URL)

db = None

coleccionSocios = None
coleccionPlanes = None
coleccionDescuentos = None
coleccionPagos = None


def crear_registros(coleccion_Planes, coleccion_Socios, coleccion_Descuentos):
    coleccion_Planes.insert_one({
            'nombre': 'oro',
            'precio': 2000
        })

    # Extraigo el id del plan para vincularlo a la coleccion socio en plan_id
    plan = coleccion_Planes.find_one({'nombre':'oro'})
    plan_id = plan['_id']

    # creo una variable que contiene una lista con los socios
    socios = [{
            'nombre': 'Stalin',
            'plan_id': plan_id,
            'discounts' : [
                {
                    '_id': 1,
                    'monto': 100,
                    'es_absoluto': True,
                    'cantidad_de_aplicaciones': 5
                },
                {
                    '_id': 2,
                    'monto': 20,
                    'es_absoluto': False,
                    'cantidad_de_aplicaciones': 3
                },
                {
                    '_id': 3,
                    'monto': 200,
                    'es_absoluto': True,
                    'cantidad_de_aplicaciones': 0
                }
            ],
            'fecha_expiracion': '2021-12-31',
            'estado': 'activo'
        },

        {
            'nombre': 'Alexis',
            'plan_id': plan_id,
            'discounts' : [
                {
                    '_id': 1,
                    'monto': 100,
                    'es_absoluto': True,
                    'cantidad_de_aplicaciones': 5
                },
                {
                    '_id': 2,
                    'monto': 20,
                    'es_absoluto': False,
                    'cantidad_de_aplicaciones': 3
                },
                {
                    '_id': 3,
                    'monto': 200,
                    'es_absoluto': True,
                    'cantidad_de_aplicaciones': 0
                }
            ],
            'fecha_expiracion': '2021-09-09',
            'estado': 'activo'
        },
        {
            'nombre': 'Carlos',
            'plan_id': plan_id,
            'discounts' : [
                {
                    '_id': 1,
                    'monto': 100,
                    'es_absoluto': True,
                    'cantidad_de_aplicaciones': 1
                },
                {
                    '_id': 2,
                    'monto': 20,
                    'es_absoluto': False,
                    'cantidad_de_aplicaciones': 2
                },
                {
                    '_id': 3,
                    'monto': 200,
                    'es_absoluto': True,
                    'cantidad_de_aplicaciones': 0
                }
            ],
            'fecha_expiracion': '2021-10-16',
            'estado': 'activo'
        },

        {
            'nombre': 'Jose',
            'plan_id': plan_id,
            'discounts' : [
                {
                    '_id': 1,
                    'monto': 100,
                    'es_absoluto': True,
                    'cantidad_de_aplicaciones': 6
                },
                {
                    '_id': 2,
                    'monto': 20,
                    'es_absoluto': False,
                    'cantidad_de_aplicaciones': 6
                },
                {
                    '_id': 3,
                    'monto': 200,
                    'es_absoluto': True,
                    'cantidad_de_aplicaciones': 0
                }
            ],
            'fecha_expiracion': '2021-10-16',
            'estado': 'activo'
        }]
    
    for socio in socios:
        # En un for agrego socio por socio, iterando cada uno de elos elementos de la lista
        coleccion_Socios.insert_one(socio)
    
    coleccion_Descuentos.insert_one({
        'monto': 100,
        'es_absoluto': True,
        'cantidad_de_aplicaciones': 5
    })

def limpiar_db(coleccionPlanes, coleccionSocios, coleccionDescuentos, coleccionPagos):
    coleccionPlanes.drop()
    coleccionDescuentos.drop()
    coleccionSocios.drop()
    coleccionPagos.drop()



# Consulta a la base de datos, y si ya existen registros, no la crea de nuevo
def inicializar_db(es_real = True):
    if es_real:
        db = prueba['challenge-1']
    else:
        db = prueba['test']
        
    global coleccionSocios, coleccionPlanes, coleccionDescuentos, coleccionPagos
    coleccionSocios = db['socios']
    coleccionPlanes = db['planes']
    coleccionDescuentos = db['descuentos']
    coleccionPagos = db['pagos']

    # if es_real:

    limpiar_db(coleccionSocios, coleccionPlanes, coleccionDescuentos, coleccionPagos)
    
    crear_registros(coleccionPlanes, coleccionSocios, coleccionDescuentos)
    

inicializar_db(False)








#################################################################################

# Para observar las bases de datos
# show dbs


# para ir hacia una db
# use admin

# Para crear una collection
# db.createCollection('nombre de collection')


# Para insertar registros a una collections, en formato json

# db.clientes.insert(

#     [
#         {
#             'nombre': 'Alexis',
#             'apellido': 'Guanique',
#             'edad': 30
#         },
#         {
#             'nombre': 'Juan',
#             'apellido': 'Perez',
#             'edad': 21
#         }
#     ]
# )



# para ver las colecciones
# show collections



# para buscar un registro
# db.clientes.find({nombre: 'Alexis'})



# Para ver los registros de la coleccion de una manera mas ordenada
# db.clientes.find().pretty()


# Para actualizar un registro
# db.clientes.update({nombre:'Pedro'}, {set: {nombre:'Alexis'}})

# Para reslizar una consulta pero solo que nos muestre el primer elemento del registro
# db.clientes.find({nombre:'Alexis'}).limint(1)

# Para eliminar un registro
# db.clientes.deleteOne({nombre:'Alexis'}0)