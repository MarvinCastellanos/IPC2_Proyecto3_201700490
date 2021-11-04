from flask import Flask, Response, request
from flask_cors import CORS
from xml.etree import ElementTree as ET
import re
import datetime
from objetos import Autorizacion

autorizaciones=[]

def verificaFecha(tiempo):
    
    fecha=re.findall('\d\d/\d\d/\d\d\d\d',tiempo)
    if fecha==None:
        print('fecha Incorrecta')
    else:
        dia=fecha[0][0]+fecha[0][1]
        mes=fecha[0][3]+fecha[0][4]
        year=fecha[0][6]+fecha[0][7]+fecha[0][8]+fecha[0][9]
        #print(fecha)
        correlativo=year+mes+dia
        try:
            fechaHora=datetime.datetime(int(year),int(mes),int(dia))
            #print('Fecha correcta')
            return fecha[0],correlativo
        except ValueError:
            print('fecha Incorrecta')
        
def verificaNit(nit):
    nit=re.findall('\d+',nit)
    nit=nit[0]
    if len(nit)>21:
        return 0
    else:
        nitA=''
        n=len(nit)
        for numero in range(len(nit)):
            if n==len(nit):
                n=n-1
                continue
            else:
                nitA+=nit[n-1]
                n=n-1
        sum=0
        #print(nitA)
        for numero in range(len(nitA)):
            sum+=int(nitA[numero])*(numero+2)
        mod=sum%11
        modR=11-mod
        modMod=modR%11
        if modMod==int(nit[len(nit)-1]):
            return nit
        else:
            return 0

def verificaValor(valor):
    num=re.match('^[\d]+.?[\d]*$',valor)
    if num==None:
        print('Valor Invalido')
    else:
        numero=float(num[0])
        numero=round(numero,2)
        print(numero)

def verificaIva(valor,iva):
    valor=float(valor)
    iva=float(iva)

    ivaP=round(valor*0.12,2)

    if ivaP==iva:
        return iva
    else:
        return 0

def verificaTotal(valor, iva, total):
    valor=float(valor)
    iva=float(iva)
    total=float(total)

    if total==valor+iva:
        return total
    else:
        return 0

def verificaReferencia(ref):
    if len(ref)>40:
        return 0
    else:
        for ref in autorizaciones:
            for auto in ref.getlistadoAutorizaciones():
                if auto['Referencia']==ref:
                    return 0
        return ref

app=Flask(__name__)
cors = CORS(app, resources={r"/*": {"origin": "*"}})

@app.route('/datos',methods=['POST'])
def index():
    archivo= request.data.decode('utf8')
    print(archivo)
    return str(archivo)

@app.route('/procesa', methods=['POST'])
def proceso():
    archivo=request.data.decode('utf-8')
    root=ET.fromstring(archivo)
    for child in root:
        fecha1=verificaFecha(child[0].text)
        if fecha1 != 0:
            fecha=fecha1[0]
            correlativo=fecha1[1]
        referencia= verificaReferencia( child[1].text)
        nitEmisor= verificaNit(child[2].text) 
        nitReceptor= verificaNit(child[3].text) 
        valor=child[4].text
        iva= verificaIva(valor,child[5].text) 
        total= verificaTotal(valor,iva,child[6].text) 

        if len(autorizaciones)==0:
            autorizaciones.append(Autorizacion(fecha,correlativo))
        else:
            n=1
            for auto in autorizaciones:
                if auto.getFecha()==fecha:
                    break
                else:
                    if n==len(autorizaciones):
                        autorizaciones.append(Autorizacion(fecha,correlativo))
                        break
                    n+=1
            for auto in autorizaciones:
                if auto.getFecha()==fecha:
                    auto.sumaFacturasRecividas()
                    if referencia != 0:
                        if nitEmisor != 0:
                            if nitReceptor != 0:
                                if iva != 0:
                                    if total != 0:
                                        auto.sumaFacturasCorrectas()
                                        auto.agregarAutorizacion({'NitEmisor':nitEmisor,'NitReceptor':nitReceptor,'Referencia':referencia,'valor':valor,'codigoAutorizacion':auto.getCorrelativo()})
                                        auto.sumaCorrelativo()
                                        print(auto.getCorrelativo())
                                    else:
                                        auto.sumaErrorTotal()
                                else:
                                    auto.sumaErrorIva()
                                    if total==0:
                                        auto.sumaErrorTotal()
                            else:
                                auto.sumaErrorNitReceptor()
                                if iva==0:
                                    auto.sumaErrorIva()
                                if total==0:
                                    auto.sumaErrorTotal()
                        else:
                            auto.sumaErrorNitEmisor()
                            if nitReceptor==0:
                                auto.sumaErrorNitReceptor()
                            if iva==0:
                                auto.sumaErrorIva()
                            if total==0:
                                auto.sumaErrorTotal()

                    else:
                        auto.sumaErrorReferenciaDuplicada()
                        if nitEmisor==0:
                            auto.sumaErrorNitEmisor()
                        if nitReceptor==0:
                            auto.sumaErrorNitReceptor()
                        if iva==0:
                            auto.sumaErrorIva()
                        if total==0:
                            auto.sumaErrorTotal()
                else:
                    continue
    print(len(autorizaciones))
    return 'Datos cargados con exito'



if __name__=='__main__':
    app.run(debug=True)