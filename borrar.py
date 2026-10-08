
from typing import dataclass_transform
prompt quiero saber cual es el cuaderno mas barato

memory.md -> comportamiento de la ia : vos sos un asesor de  ventas, te van a preguntar sobre presupuesto de distintos insumos que vendemos. lee el index y andarecorriendo 
los distintos indices...
hace una sumatoria de todas las palabras que yo voy usando y hablame de la misma manera 
fijate que cosas te doy permiso, y no vuelvas a preguntarme


history.md -> historial de la conversacion

structure.md: mi organizacion de carpetas esta con un indice general, y dentro de cada carpeta un nuevo indice de la carpeta.

index.txt

nombreCarpeta - descripcion                                                   - palabras claves 
libreria      - tiene todos los precios y el stock de los insumos de libreria - libro, cuaderno, lapiz, 
indumentaria  - tiene todos los precios y el stock de los insumos de indumentaria - remera, pantalon, 
carniceria   - tiene todos los precios y el stock de los insumos de carniceria - carne, pollo, pescado, 


rta: mandame denrto de la carpeta libreria el indice. 

carpeta: libreria

    index: nombreInsumo - descripcion    - precio - stock
    texto: cuadernos    - cuadernos de dibujo    - 150 - 50 
    texto: cuadernosA4  - cuadernos A4     - 200 - 100
    texto: lapices      - lapices de colores   - 100 - 100


    mandame todos los archivos que tengan como texto en nombre de insumo la palabra cuadernos


rta: mucho gusto nosotros tenemos distitnos cuadernos. te paso la lista:


base de datos 

nombre - ID - descripcion - precio - stock - palabras relacionadas
libreria - 1 - tiene todos los precios y el stock de los insumos de libreria - 150 - 50 
indumentaria - 2 - tiene todos los precios y el stock de los insumos de indumentaria - 200 - 100
carniceria - 3 - tiene todos los precios y el stock de los insumos de carniceria - 100 - 100

carpeta: indumentaria
carpeta: carniceria

cuaderno  barato

memory asesor de ventas de una casa de libreria

//prompt para sacar el esqueleto de una base dato ¨describe"

SENTENCIA SQL

//columna  igual a cuardeno ordenados ascendente por precio , y me quedo con el primero.
producto = SELECT * FROM tabla WHERE columna = 'cuaderno' ORDER BY precio ASC LIMIT 1;


te doy el prompt del cluiente, y te paso el producto mas barato:

responda bonito