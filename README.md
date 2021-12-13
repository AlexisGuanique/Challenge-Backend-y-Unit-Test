# Challenge Python Developer - Muvinai


## Challenge backend & unit testing

**Autor: Alexis Guanique**

El entregable consta de una aplicación automatizada de cobros, la cual utiliza MongoDb como sistema de gestión de base de datos, en el cual se almacenan tres colecciones: Socios, Descuentos, Planes y una cuarta llamada Pagos, la cual es generada al momento de generar el cobro. El cobro realizado a los socios de la tabla Socios tiene la condición de que su estado sea activo y su fecha de expiración sea menor o igual a la fecha del día en el cual se realiza la prueba; ademas se debe buscar los descuentos que tenga disponibles el cliente y una vez realizado el cobro realiza una actualización en la base de datos de: la fecha de expiracion (es aumentada un mes), la cantidad de aplicaciones que tiene disponible cada descuento (de resta 1) y es creado un registro en la colección Pagos. Es importante destacar que para realizar el cobro de manera automática, se utilizo la librería SCHEDULE, la cual permite agendar cada cuanto tiempo se realizara la ejecución del programa.

También cabe destacar que para las pruebas unitarias se utilizo la librería unittest de python.

STACK UTILIZADO: **Python, MongoDb y UnitTest**



