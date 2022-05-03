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

gen2_excel = pd.read_excel('./data/gen2.xlsx', sheet_name=['asesorekt', 'asesorfinan'])

gen3_excel = pd.read_excel('./data/gen3.xlsx', sheet_name=['liderfinan', 'liderekt'])

pd.options.display.float_format = '{:,.1f}'.format

sheet_names = ['nonEmpsG', 'nonFG', 'g3formers', 'g3Emps', 'gEmps', 'gFormers']

def percents(number):
    return f'{number:.1%}'

def nf(number):
    return f'{number:,.0f}'

def kpis_asesorekt_gen2():
    data = gen2_excel['asesorekt'].to_dict('records')

    for i in range(len(data)):
        data[i]['Vtas_Cred_Mto'] = nf(data[i]['Vtas_Cred_Mto'])
        data[i]['Obj_Cred'] = nf(data[i]['Obj_Cred'])
        data[i]['Logro_Cred'] = percents(data[i]['Logro_Cred'])
        data[i]['Vtas_Tot_Mto'] = nf(data[i]['Vtas_Tot_Mto'])
        data[i]['Obj_Tot'] = nf(data[i]['Obj_Tot'])
        data[i]['Logro_Tot'] = percents(data[i]['Logro_Tot'])

    return data

def kpis_asesorfinan_gen2():
    data = gen2_excel['asesorfinan'].to_dict('records')

    for i in range(len(data)):
        data[i]['Colocacion'] = nf(data[i]['Colocacion'])
        data[i]['Obj_Col'] = nf(data[i]['Obj_Col'])
        data[i]['Logro_Col'] = percents(data[i]['Logro_Col'])
        data[i]['Cartera'] = nf(data[i]['Cartera'])
        data[i]['Obj_Cart'] = nf(data[i]['Obj_Cart'])
        data[i]['Logro_Cart'] = percents(data[i]['Logro_Cart'])
        data[i]['Sem_Pase_Cartera'] = nf(data[i]['Sem_Pase_Cartera'])
        data[i]['Pase'] = nf(data[i]['Pase'])
        data[i]['Sdo_Aper'] = nf(data[i]['Sdo_Aper'])
        data[i]['Obj_Sdo_Aper'] = nf(data[i]['Obj_Sdo_Aper'])
        data[i]['Logro_Sdo_Aper'] = percents(data[i]['Logro_Sdo_Aper'])
        data[i]['Num_Afil'] = nf(data[i]['Num_Afil'])
        data[i]['Obj_Afil'] = nf(data[i]['Obj_Afil'])
        data[i]['Logro_Afil'] = percents(data[i]['Logro_Afil'])
        data[i]['Num_Portas'] = nf(data[i]['Num_Portas'])
        data[i]['Obj_Portas'] = nf(data[i]['Obj_Portas'])
        data[i]['Logro_Portas'] = percents(data[i]['Logro_Portas'])

    return data

def kpis_liderekt_gen3():
    data = gen3_excel['liderekt'].to_dict('records')

    for i in range(len(data)):
        data[i]['Vtas_Cred_Mto'] = nf(data[i]['Vtas_Cred_Mto'])
        data[i]['Obj_Cred'] = nf(data[i]['Obj_Cred'])
        data[i]['Logro_Cred'] = percents(data[i]['Logro_Cred'])
        data[i]['Vtas_Tot_Mto'] = nf(data[i]['Vtas_Tot_Mto'])
        data[i]['Obj_Tot'] = nf(data[i]['Obj_Tot'])
        data[i]['Logro'] = percents(data[i]['Logro'])
        data[i]['Prom'] = percents(data[i]['Prom'])

    return data

def kpis_liderfinan_gen3():
    data = gen3_excel['liderfinan'].to_dict('records')

    for i in range(len(data)):
        data[i]['Colocacion'] = nf(data[i]['Colocacion'])
        data[i]['Obj_Col'] = nf(data[i]['Obj_Col'])
        data[i]['Logro_Col'] = percents(data[i]['Logro_Col'])
        data[i]['Cartera'] = nf(data[i]['Cartera'])
        data[i]['Obj_Cart'] = nf(data[i]['Obj_Cart'])
        data[i]['Sem_Pase_Cartera'] = nf(data[i]['Sem_Pase_Cartera'])
        data[i]['Logro_Cart'] = percents(data[i]['Logro_Cart'])
        data[i]['Pase'] = nf(data[i]['Pase'])
        data[i]['Sdo_Aper'] = nf(data[i]['Sdo_Aper'])
        data[i]['Obj_Sdo_Aper'] = nf(data[i]['Obj_Sdo_Aper'])
        data[i]['Logro_Sdo_Aper'] = percents(data[i]['Logro_Sdo_Aper'])
        data[i]['Num_Afil'] = nf(data[i]['Num_Afil'])
        data[i]['Obj_Afil'] = nf(data[i]['Obj_Afil'])
        data[i]['Logro_Afil'] = percents(data[i]['Logro_Afil'])
        data[i]['Num_Portas'] = nf(data[i]['Num_Portas'])
        data[i]['Obj_Portas'] = nf(data[i]['Obj_Portas'])
        data[i]['Logro_Portas'] = percents(data[i]['Logro_Portas'])

    return data

kpis_asesorekt_gen2 = kpis_asesorekt_gen2()
kpis_asesorfinan_gen2 = kpis_asesorfinan_gen2()
kpis_liderekt_gen3 = kpis_liderekt_gen3()
kpis_liderfinan_gen3 = kpis_liderfinan_gen3()

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
    "Hemos concluido la fase  'Intensiva', del programa Acompañándote y de acuerdo con el análisis de los indicadores de productividad, muestra que tus resultados presentan áreas de oportunidad, por lo que No te graduaste y te invitamos a acercarte con tu formador de equipo, para que determinen los planes de acción a seguir.                                                                                                           ",
    "Hemos concluido con la fase 'Intensiva', del programa Acompañándote y de acuerdo al análisis de productividad de tu colaborador, muestra que los resultados presentan areas de oportunidad por que te invitamos mantengas una conversación con el para retroalimentarle. Reúnete con tu colaborador y bríndale una retroalimentación positiva, revisen el plan de acción, generen acciones le ayudaran a subir su productividad.                                                                                                            ",
    "Hemos iniciado la generación 3 del Programa Acompañándote y de acuerdo con el análisis de los indicadores de productividad de tu colaborador, muestra que sus resultados aun presentan áreas de oportunidad, por lo que deberá acompañarlo durante esta fase inicial preventiva. Reúnete con tu colaborador y bríndale una retroalimentación positiva, revisen el plan de acción, generen acciones le ayudaran a subir su productividad.                                                                                                            ",
    "Hemos iniciado la Generación 3 del Programa Acompañándote y de acuerdo con el análisis de los indicadores de productividad muestra que tus resultados  presentan áreas de oportunidad, por lo que invitamos a participar en la fase preventiva. Reúnete con tu formador de equipo y, generen acciones que te ayudaran a subir tu productividad.                                                                                                            ",
    "Hemos concluido la fase Intensiva del Programa Acompañándote y de acuerdo con el análisis de los indicadores de productividad muestra que tus resultados fueron satisfactorios, graduándote de esta fase. Reúnete con tu formador de equipo.                                                                                        ",
    "Hemos concluido la fase intensiva del Programa Acompañándote y de acuerdo con el análisis de los indicadores de productividad de tu colaborador, te comentamos que ha sido graduado de la fase. Por favor acércate a el y ten la plantica de retroalimentación.                                                                                                            ",
]

sheet_messages = dict (zip(sheet_names, messages))

def doSomething(formid):
    try:
        text = []
        name = None
        for sheet_name, id_name in data_excel.items():
            if formid in id_name:
                msg = sheet_messages[sheet_name]
                text.append(msg)
                name = id_name[formid]
        result = '\n'.join(text)
        if result:
            return f'{name}                                                                                                                            {result}'
        return 'No se encontró el numero de empleado.'
    except Exception as e:
        return f'Error: {e}'

def doSomething2(formid):
    try:
        for element in kpis_asesorekt_gen2:
            for id_name in element.items():
                if formid in id_name:
                    return element
                else:
                    continue

        for element in kpis_asesorfinan_gen2:
            for id_name in element.items():
                if formid in id_name:
                    return element
                else:
                    continue

        for element in kpis_liderekt_gen3:
            for id_name in element.items():
                if formid in id_name:
                    return element
                else:
                    continue

        for element in kpis_liderfinan_gen3:
            for id_name in element.items():
                if formid in id_name:
                    return element

        return 'No se encontró el numero de empleado.'

    except Exception as e:
        return f'Error: {e}'

@app.route('/id', methods=['POST'])
def send(*args, **kwargs):
    data = request.get_json()
    formid = data.get('formid')
    if(formid.isnumeric()):
        formid = int(formid)
    else:
        return 'Ingrese un numero valido por favor'

    test = doSomething(formid)
    print(formid, test)
    return test

@app.route('/kpis', methods=['POST'])
def send2(*args, **kwargs):
    data = request.get_json()
    formid = data.get('formid')
    if(formid.isnumeric()):
        formid = int(formid)
    else:
        return 'Ingrese un numero valido por favor'

    test = doSomething2(formid)
    print(formid, test)
    return test

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()
    # app.run(host='0.0.0.0', port=5000)