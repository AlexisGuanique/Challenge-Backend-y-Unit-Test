from pymongo import MongoClient

#CREACION DE LA BASE DE DATOS


MONGO_URL = 'mongodb://localhost'
prueba = MongoClient(MONGO_URL)

db = None

coleccionSocios = None
coleccionPlanes = None
coleccionDescuentos = None
coleccionPagos = None


def crear_registros(coleccion_Planes, coleccion_Socios, coleccion_Descuentos):
    #Insert una plan en la coleccion
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
    
        # En un for agrego socio por socio, iterando cada uno de elos elementos de la lista
    
    for socio in socios:
        coleccion_Socios.insert_one(socio)
    
    #Inserto un descuento en la coleccion
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


# Se crea dos bases de datos diferentes, una para test y otra para la app, de esta manera se evita conflictos en db
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

    if coleccionSocios.count_documents({}) > 4:
        limpiar_db(coleccionSocios, coleccionPlanes, coleccionDescuentos, coleccionPagos)
    
    limpiar_db(coleccionSocios, coleccionPlanes, coleccionDescuentos, coleccionPagos)
    crear_registros(coleccionPlanes, coleccionSocios, coleccionDescuentos)
    print('Base de datos Inicializada con Exito')
    
    

inicializar_db(False)