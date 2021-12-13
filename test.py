import unittest
from datetime import datetime
import db
import main



class TestPagos(unittest.TestCase):

    def test_obtenerSocio(self):

        result = main.obtener_socios()



        plan_id = result[0]['plan_id']

        id = []
        for socio in result:
            id.append(socio['_id'])


        expect =  [{'_id':id[0],
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
            '_id':id[1],
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
            '_id':id[2],
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


        self.assertEqual(result, expect)


    def test_obtener_plan(self):
        # having (teniendo)
        socios = db.coleccionSocios.find()
        lista_socio = []

        for socio in socios:
            lista_socio.append(socio)

        plan_id = lista_socio[0]['plan_id']

        # when (cuando)

        result = main.obtener_plan(plan_id)

        # then (entonces)
        expect = {'_id':plan_id,
            'nombre': 'oro',
            'precio': 2000
        }

        self.assertEqual(result, expect)


    def test_generar_pago(self):

        # having (teniendo)
        pago = {
            'pediodo_cobrado': datetime.now().month,
            'monto_cobrado' : 1500,
            'descuentos_aplicados': [{
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
                }],
            'id_socio': 1
        }


        # when (cuando)

        result = main.generar_pago(1, 1500, pago.get('descuentos_aplicados'))

        # then (entonces)
        del(result['_id'])
        self.assertEqual(result, pago)
    # 4

    def test_obtener_descuentos_aplicables(self):

        # Having
        descuentos = []
        socio = db.coleccionSocios.find_one()

        for descuento in socio.get('discounts'):
            if(descuento.get('cantidad_de_aplicaciones') > 0):
                descuentos.append(descuento)

        # When

        result = main.obtener_descuentos_aplicables(socio)


        # Then

        self.assertEqual(descuentos, result)


    def test_calcular_descuento(self):

        # having
        #Obtengo el precio del plan
        plan = db.coleccionPlanes.find()
        planes = []
        for precio_plan in plan:
            planes.append(precio_plan)

        precio = planes[0]['precio']

        #Obtengo el descuento a aplicar
        descuentoFinal = 0

        descuentos = []
        socio = db.coleccionSocios.find_one()

        for descuento in socio.get('discounts'):
            if(descuento.get('cantidad_de_aplicaciones') > 0):
                descuentos.append(descuento)

                if(descuento.get('es_absoluto')):
                    descuentoFinal += descuento.get('monto')

                else:
                    descuentoFinal += precio * ( descuento.get('monto') / 100 )

        # When
        result = main.calcular_descuento(precio, descuentos)
        # Then

        self.assertEqual(descuentoFinal, result)


    def test_calcular_monto_a_pagar(self):
        # Having
        # Obtengo precio
        plan = db.coleccionPlanes.find()
        planes = []
        for precio_plan in plan:
            planes.append(precio_plan)

        precio = planes[0]['precio']

        # Obtengo descuento
        descuentoFinal = 0
        descuentos = []
        socio = db.coleccionSocios.find_one()

        for descuento in socio.get('discounts'):
            if(descuento.get('cantidad_de_aplicaciones') > 0):
                descuentos.append(descuento)

                if(descuento.get('es_absoluto')):
                    descuentoFinal += descuento.get('monto')

                else:
                    descuentoFinal += precio * ( descuento.get('monto') / 100 )

        # Obtengo el socio
        socio = db.coleccionSocios.find_one()
        plan_id = socio.get('plan_id')
        plan = main.obtener_plan(plan_id)

        precio = plan.get('precio')
        descuento = main.calcular_descuento(precio, descuentos)
        monto = precio - descuento

        if(monto < 0):
            monto = 0

        # When

        result = main.calcular_monto_a_pagar(socio, descuentos)

        # then

        self.assertEqual(monto, result)

    def test_disminuir_aplicaciones(self):
        # Having
        descuentos = []
        socio = db.coleccionSocios.find_one()

        for descuento in socio.get('discounts'):
            if(descuento.get('cantidad_de_aplicaciones') > 0):
                descuentos.append(descuento)

        for descuento in descuentos:
            
            descuento['cantidad_de_aplicaciones'] -= 1

            db.coleccionSocios.update_one({"_id": socio['_id'], "discounts._id": descuento  ['_id']},
                {
                "$set": { #El dolar toma el primer registro que hace match con mi busqueda
                    "discounts.$.cantidad_de_aplicaciones": descuento['cantidad_de_aplicaciones'] 
                }
                })
        
        expect = descuentos

        # When
        result = main.disminuir_aplicaciones(socio, descuentos)

        # print(result)
        # print(expect)

        # Then

        self.assertEqual(expect, result)

if __name__ == '__main__':
    db.inicializar_db(False)
    unittest.main()