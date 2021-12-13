# Challenge Python Developer - Muvinai


## Challenge backend & unit testing

**Autor: Alexis Guanique**

El entregable consta de una aplicacion automatizada de cobros, la cual utiliza MongoDb como sistema de gestion de base de datos, en el cual se almacenan tres colecciones: Socios, Descuentos, Planes y una cuarta llamada Pagos, la cual es generada al momento de generar el cobro. El cobro realizado a los socios de la tabla Socios tiene la condicion de que su estado sea activo y su fecha de expiracion sea menor o igual a la fecha del dia en el cual se realiza la prueba; ademas se debe buscar los descuentos que tenga disponibles el cliente y una vez realizado el cobro realiza una actualizacion en la base de datos de: la fecha de expiracion (es aumentada un mes), la cantidad de aplicaciones que tiene disponible cada descuento (de resta 1) y es creado un registro en la coleccion Pagos. Es importante destacar que para realizar el cobro de manera automatica, se utilizo la libreria SCHEDULE, la cual permite agendar cada cuanto tiempo se realizara la ejecucion del programa.

Tambien cabe destacar que para las pruebas unitarias se utilizo la libreria unittest de python.

STACK UTILIZADO: **Python, MongoDb y UnitTest**


![alt text](muvinai.jpg)


