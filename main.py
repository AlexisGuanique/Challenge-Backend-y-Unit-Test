import schedule
from time import sleep
from datetime import datetime
from dateutil.relativedelta import relativedelta
import db


#Obtengo los socios activos y con fecha de expiracion caducada
def obtener_socios():
    listaSocios = []
    querySocios = db.coleccionSocios.find(
        {
            'estado':'activo',
            'fecha_expiracion': {
                '$lte': datetime.now().strftime("%Y-%m-%d")
            }
        })

    # lte = less than or equal


    for x in querySocios:
        listaSocios.append(x)

    return listaSocios


# Obtengo el plan del socio, desde la coleccion planes 
def obtener_plan(plan_id):

    plan = db.coleccionPlanes.find_one({'_id':plan_id})


    return plan


# Hago una pegada a la coleccion pagos y guardo el pago a realizar 
def generar_pago(id_socio, monto, descuentos):
    pago = {
        # Con datatime.now() devuelvo el mes actual el el registro periodo cobrado
        'pediodo_cobrado': datetime.now().month,
        'monto_cobrado' : monto,
        'descuentos_aplicados': descuentos,
        'id_socio': id_socio 
    }
    #Guardar pago en base de dato con un insert into +
    db.coleccionPagos.insert_one(pago)

    return pago



def obtener_descuentos_aplicables(socio):
    descuentosAplicables = []
    
    for descuento in socio.get('discounts'):
        if(descuento.get('cantidad_de_aplicaciones') > 0):
            descuentosAplicables.append(descuento)

    return descuentosAplicables
    

def calcular_descuento(precio,descuentos):
    descuentoFinal = 0
    
    for descuento in descuentos:
        if(descuento.get('es_absoluto')):
            descuentoFinal += descuento.get('monto')
        else:
            descuentoFinal += precio * ( descuento.get('monto') / 100 )

    return descuentoFinal

def calcular_monto_a_pagar(socio, descuentos):

    plan_id = socio.get('plan_id')
    plan = obtener_plan(plan_id)
    
    precio = plan.get('precio')
    descuento = calcular_descuento(precio, descuentos)
    monto = precio - descuento

    if(monto < 0):
        monto = 0

    return monto


def aplicar_cobros():
    socios = obtener_socios()

    for socio in socios:
        descuentos = obtener_descuentos_aplicables(socio)
        monto = calcular_monto_a_pagar(socio, descuentos)        
        id_socio = socio['_id']

        generar_pago(id_socio, monto, descuentos)        
        actualizar_fecha_expiracion(socio)
        disminuir_aplicaciones(socio,descuentos)
        print('Cobro realizado a: ' + socio['nombre'] + ', próxima fecha de cobro: ' + socio['fecha_expiracion'] + ', Monto Total Cobrado: ' + str(monto))


# Agregar pegada a la base de dato para que cambie cantidad_de_apliaciones 
def disminuir_aplicaciones(socio,descuentos):
    for descuento in descuentos:
            
        descuento['cantidad_de_aplicaciones'] -= 1

        db.coleccionSocios.update_one({"_id": socio['_id'], "discounts._id": descuento['_id']},
            {
            "$set": {
                "discounts.$.cantidad_de_aplicaciones": descuento['cantidad_de_aplicaciones'] 
                }
            })
    return descuentos

# Realizar actualizacion de la fecha de expiracion
def actualizar_fecha_expiracion(socio):
    fecha_expiracion_str = socio.get('fecha_expiracion')
    fecha_expiracion = datetime.strptime(fecha_expiracion_str, "%Y-%m-%d")

    fecha_expiracion_nueva = fecha_expiracion + relativedelta(months=1)
    socio['fecha_expiracion'] = fecha_expiracion_nueva.strftime("%Y-%m-%d")

    miConsulta = { "_id": socio['_id'] }
    nuevoValor = { "$set": { "fecha_expiracion": socio['fecha_expiracion']}}

    guardado = db.coleccionSocios.update_one(miConsulta, nuevoValor)

    return guardado



def main():
    db.inicializar_db()

    schedule.every(1).day.at("16:17").do(aplicar_cobros)
    aplicar_cobros()
    while True:
        schedule.run_pending() 
        sleep(1)



if __name__ == '__main__':
    
    main()




