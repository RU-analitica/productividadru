import pandas as pd
import numpy as np
from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
from flask_bs4 import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_cors import CORS

app = Flask(__name__)

cors = CORS(app, resources={r"*": {"origins": "*"}})

bootstrap = Bootstrap(app)

base_excel = pd.read_excel('./data/base.xlsx', sheet_name=None)

sheet_names = ['nonEmpsG', 'nonFG', 'g3formers', 'g3Emps', 'gEmps', 'gFormers']

def create_dict(df):
    idArr = []
    nameArr = []
    for element in df['id']:
        idArr.append(element)
    for element in df['name']:
        nameArr.append(element)

    data = dict(zip(idArr, nameArr))

    return data

data_excel = {}

for sheet_name in sheet_names:
    data_excel[sheet_name] = create_dict(base_excel[sheet_name])

messages = [
    "Hemos concluido la fase  'Intensiva', del programa Acompañándote y de acuerdo con el análisis de los indicadores de productividad, muestra que tus resultados presentan áreas de oportunidad, por lo que No te graduaste y te invitamos a acercarte con tu formador de equipo, para que determinen los planes de acción a seguir.",
    "Hemos concluido con la fase 'Intensiva', del programa Acompañándote y de acuerdo al análisis de productividad de tu colaborador, muestra que los resultados presentan areas de oportunidad por que te invitamos mantengas una conversación con el para retroalimentarle. Reúnete con tu colaborador y bríndale una retroalimentación positiva, revisen el plan de acción, generen acciones le ayudaran a subir su productividad.",
    "Hemos iniciado la generación 3 del Programa Acompañándote y de acuerdo con el análisis de los indicadores de productividad de tu colaborador, muestra que sus resultados aun presentan áreas de oportunidad, por lo que deberá acompañarlo durante esta fase inicial preventiva. Reúnete con tu colaborador y bríndale una retroalimentación positiva, revisen el plan de acción, generen acciones le ayudaran a subir su productividad.",
    "Hemos iniciado la Generación 3 del Programa Acompañándote y de acuerdo con el análisis de los indicadores de productividad muestra que tus resultados  presentan áreas de oportunidad, por lo que invitamos a participar en la fase preventiva. Reúnete con tu formador de equipo y, generen acciones te ayudaran a subir tu productividad. ",
    "Hemos concluido la fase Intensiva del Programa Acompañándote y de acuerdo con el análisis de los indicadores de productividad muestra que tus resultados fueron satisfactorios, graduándote de esta fase. Reúnete con tu formador de equipo.",
    "Hemos concluido la fase intensiva del Programa Acompañándote y de acuerdo con el análisis de los indicadores de productividad de tu colaborador, te comentamos que ha sido graduado de la fase. Por favor acércate a el y ten la plantica de retroalimentación.",
]

sheet_messages = dict (zip(sheet_names, messages))

def doSomething(formid):
    text = []
    name = None
    for sheet_name, id_name in data_excel.items():
        if formid in id_name:
            msg = sheet_messages[sheet_name]
            text.append(msg)
            name = id_name[formid]
    result = '\n'.join(text)
    if result:
        return f'{name}, {result}'
    return 'No se encontró el formid'

# 873693

@app.route('/id', methods=['POST'])
def send(*args, **kwargs):
    data = request.get_json()
    formid = data.get('formid')
    if(formid.isnumeric()):
        formid = int(formid)
    else:
        return {'error': 'formid no es un número', code: 500}

    test = doSomething(formid)
    print(formid, test)
    return test

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()




