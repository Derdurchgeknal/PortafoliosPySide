import json
from helpers import absPath

datos = []

datos.append({
    "nombre": "Hector",
    "empleo": "Instructor",
    "email": "hektor@ejemplo.com"
})

contactos =[
    ("Manuel", "Desarrollador Web", "manuel@ejemplo.com"),
    ("Lorena", "Gestora de proyectos", "lorena@ejemplo.com"),
    ("Javier", "Analista de datos", "javier@ejemplo.com"),
    ("Marta", "Experta en Python", "marta@ejemplo.com")
]

for nombre, empleo, email in contactos:
    datos.append({
        "nombre": nombre,
        "empleo": empleo,
        "email": email
    })

with open(absPath("contactos.json"), "w") as fichero:
    json.dump(datos, fichero)

    datos = None

with open(absPath("contactos.json")) as fichero:
    datos = json.load(fichero)
    for contacto in datos:
        print(contacto["nombre"], contacto["empleo"], contacto["email"])