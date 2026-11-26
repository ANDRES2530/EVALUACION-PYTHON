import os
from flask import Flask, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

db=client["CURSOS_CTPI_2026-ANDRES"]
aprendices=db["APRENDICES_MONTANO"]
#10.1
@app.route('/api/cantidadAprendices')
def cantidad_aprendices():
    cantidad=aprendices.count_documents({})
    return jsonify({"CantidadAprendices":cantidad})
#10.2
@app.route("/api/cantidadAprendices/<nivel>")
def cantidadPorNivel(nivel):
    cantidad = aprendices.count_documents({"NIVEL_DE_FORMACION": nivel})
    return jsonify({"CantidadAprendices": cantidad, "Nivel de formación": nivel})

#10.3
@app.route("/api/programas/<nivel>")
def programasPorNivel(nivel):
   
    programas = aprendices.distinct("PROGRAMA", {"NIVEL_DE_FORMACION": nivel})
    return jsonify({"nivel de formación": nivel, "programas": programas})

#10.4
@app.route('/api/certificados/<programa>')
def aprendices_certificados(programa):
    filtro = {
        "PROGRAMA": programa,
        "ESTADO_APRENDIZ": "Certificado"
    }
    proyeccion = {
        "_id": 0,
        "FICHA": 1,
        "NOMBRE": 1,
        "PRIMER_APELLIDO": 1,
        "SEGUNDO_APELLIDO": 1
    }
    resultado = list(aprendices.find(filtro, proyeccion))
    return jsonify({
        "Aprendices_Certificados": resultado,
        "Programa": programa
    })

#10.5
@app.route('/api/porCertificar/<int:ficha>/<int:cantidad>')
def aprendices_por_certificar(ficha, cantidad):
    filtro = {
        "FICHA": ficha,
        "ESTADO_APRENDIZ": "Por certificar"
    }
    proyeccion = {
        "_id": 0,
        "FICHA": 1,
        "PROGRAMA": 1,
        "IDENTIFICACION": 1,
        "NOMBRE": 1,
        "PRIMER_APELLIDO": 1,
        "SEGUNDO_APELLIDO": 1
    }
    resultado = list(
        aprendices.find(filtro, proyeccion)
        .sort("PRIMER_APELLIDO", -1)
        .limit(cantidad)
    )
    return jsonify({"Cantidad de Aprendices por Certificar": resultado})

#10.6
@app.route('/api/terminadaUnificacion/<programa>')
def terminada_unificacion(programa):
    filtro = {
        "PROGRAMA": programa,
        "ESTADO_FICHA": "Terminada por unificación"
    }
    proyeccion = {
        "_id": 0,
        "FICHA": 1,
        "IDENTIFICACION": 1,
        "NOMBRE": 1,
        "PRIMER_APELLIDO": 1,
        "SEGUNDO_APELLIDO": 1
    }
    resultado = list(aprendices.find(filtro, proyeccion))
    return jsonify({
        "Programa": programa,
        "Aprendices": resultado
    })

#10.7
@app.route('/api/aprendicesPowerBI')
def aprendices_power_bi():
    filtro = {"PROGRAMA": "VISUALIZACION DE DATOS USANDO POWER BI"}
    proyeccion = {
        "_id": 0,
        "PROGRAMA": 1,
        "FICHA": 1,
        "NOMBRE": 1,
        "PRIMER_APELLIDO": 1,
        "SEGUNDO_APELLIDO": 1
    }
    resultado = list(aprendices.find(filtro, proyeccion))
    return jsonify({"Aprendices": resultado})

if __name__ == '__main__':
    app.run(debug=True, port=8000)