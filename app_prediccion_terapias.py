from pymongo import MongoClient
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from flask import Flask, request, redirect
app = Flask(__name__)
#settings
app.secret_key = "mysecretkey"
def conectarMongo():
    mongoClient = MongoClient("mongodb+srv://kevin:k171812@cluster0.hmqlq.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = mongoClient.Centro_Medico
    collection = db.Terapias
    data = pd.DataFrame(list(collection.find()))
    data.dropna()
    del data['_id']
    y = data.iloc[:, -1]
    X = data
    X = X.drop(['Diagnostico'], axis=1)
    return X,y

X,y=conectarMongo()

def entrenamiento():
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    algoritmo = SVC(kernel='linear')
    algoritmo.fit(X_train, y_train)
    return algoritmo

algoritmo_SVC_terapias=entrenamiento()


def modelo(x2):
    y_pred=algoritmo_SVC_terapias.predict(x2)
    print(y_pred[0])
    return y_pred[0]



@app.route('/', methods=["GET","POST"])
def Index():
    if request.method == 'POST':       
        sindrome_D = request.form.getlist('sin_D')
        print(sindrome_D)
        paralisis_Cer = request.form.getlist('par_C')
        parkinson = request.form.getlist('park')
        hemiplejia = request.form.getlist('hemiplejia')
        hemiparesia = request.form.getlist('hemiparesia')
        asma = request.form.getlist('asma')
        epoc = request.form.getlist('epoc')
        tuberculosis = request.form.getlist('tuber')
        fibrosis_Q = request.form.getlist('fib_Quis')
        bronquitis = request.form.getlist('bron_cron')
        luxaciones = request.form.getlist('luxaciones')
        tendinitis = request.form.getlist('tendinitis')
        esguinces = request.form.getlist('esguinces')
        desgarros = request.form.getlist('desgarros')
        fracturas = request.form.getlist('fracturas')
        
        if 'on' in sindrome_D:
            sindrome_D=1
        else:
            sindrome_D=0
     
        if 'on' in paralisis_Cer:
            paralisis_Cer=1
        else:
            paralisis_Cer=0
        
        if 'on' in parkinson:
            parkinson=1
        else:
            parkinson=0
        
        if 'on' in hemiplejia:
            hemiplejia=1
        else:
            hemiplejia=0
     
        if 'on' in hemiparesia:
            hemiparesia=1
        else:
            hemiparesia=0
        
        if 'on' in asma:
            asma=1
        else:
            asma=0
        
        if 'on' in epoc:
            epoc=1
        else:
            epoc=0
        
        if 'on' in tuberculosis:
            tuberculosis=1
        else:
            tuberculosis=0
        
        if 'on' in fibrosis_Q:
            fibrosis_Q=1
        else:
            fibrosis_Q=0

        if 'on' in bronquitis:
            bronquitis=1
        else:
            bronquitis=0
        
        if 'on' in luxaciones:
            luxaciones=1
        else:
            luxaciones=0
        
        if 'on' in tendinitis:
            tendinitis=1
        else:
            tendinitis=0
        
        if 'on' in esguinces:
            esguinces=1
        else:
            esguinces=0
        
        if 'on' in desgarros:
            desgarros=1
        else:
            desgarros=0
        
        if 'on' in fracturas:
            fracturas=1
        else:
            fracturas=0

        x_new_diagnostico=[[int(sindrome_D),int(paralisis_Cer),int(parkinson),
                        int(hemiplejia),int(hemiparesia),int(asma),int(epoc),
                        int(tuberculosis),int(fibrosis_Q),int(bronquitis),
                        int(luxaciones),int(tendinitis),int(esguinces),
                        int(desgarros),int(fracturas)]]
        print(x_new_diagnostico)
        y_pred=modelo(x_new_diagnostico)
        url="http://localhost/ejemplo_form/leer.php?y_pred="+y_pred
        return redirect(url)
if __name__ == "__main__":
	app.run(host='0.0.0.0',port = 8080)
