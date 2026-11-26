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

@app.route('/api/cantidadAprendices')
def cantidad_aprendices():
    cantidad=aprendices.count_documents({})
    return jsonify({"CantidadAprendices":cantidad})

@app.route("/api/cantidadAprendices/<nivel>")
def cantidadPorNivel(nivel):
    cantidad = aprendices.count_documents({"NIVEL_DE_FORMACION": nivel})
    return jsonify({"CantidadAprendices": cantidad, "Nivel de formación": nivel})


@app.route("/api/programas/<nivel>")
def programasPorNivel(nivel):
    # distinct trae los nombres sin repetir
    programas = aprendices.distinct("PROGRAMA", {"NIVEL_DE_FORMACION": nivel})
    return jsonify({"nivel de formación": nivel, "programas": programas})

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

if __name__ == '__main__':
    app.run(debug=True, port=8000)