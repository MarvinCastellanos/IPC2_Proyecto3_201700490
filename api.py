from flask import Flask, Response, request
from flask_cors import CORS
from xml.etree import ElementTree as ET
from xml.dom import minidom
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
        return 0
    else:
        numero=float(num[0])
        numero=round(numero,2)
        return(str(numero))

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

    if round(total,2)==round(valor+iva,2):
        return total
    else:
        return 0

def verificaReferencia(refe):
    if len(refe)>40:
        return 0
    else:
        for ref in autorizaciones:
            for auto in ref.getlistadoAutorizaciones():
                if auto['Referencia']==refe:
                    return 0
        return str(refe)

def generaXMLSalida():
    document=minidom.Document()
    root=document.createElement('LISTAAUTORIZACIONES')

    for autoriza in autorizaciones:
        autorizacion=document.createElement('AUTORIZACION')
        #fecha
        fecha=document.createElement('FECHA')
        fecha.appendChild(document.createTextNode(autoriza.getFecha()))
        autorizacion.appendChild(fecha) 
        #facturas recividas
        facReciv=document.createElement('FACTURAS_RECIBIDAS')
        facReciv.appendChild(document.createTextNode(str(autoriza.getfacturasRecibidas())))
        autorizacion.appendChild(facReciv)
        #errores
        errores=document.createElement('ERRORES')
        NEmisor=document.createElement('NIT_EMISOR')
        NEmisor.appendChild(document.createTextNode(str(autoriza.geterrores()['Nit_Emisor'])))
        errores.appendChild(NEmisor)
        #----------------
        NReceptor=document.createElement('NIT_RECEPTOR')
        NReceptor.appendChild(document.createTextNode(str(autoriza.geterrores()['Nit_Receptor'])))
        errores.appendChild(NReceptor)
        #----------------
        EIva=document.createElement('IVA')
        EIva.appendChild(document.createTextNode(str(autoriza.geterrores()['Iva'])))
        errores.appendChild(EIva)
        #----------------
        ETotal=document.createElement('TOTAL')
        ETotal.appendChild(document.createTextNode(str(autoriza.geterrores()['Total'])))
        errores.appendChild(ETotal)
        #----------------
        RDuplicada=document.createElement('REFERENCIA_DUPLICADA')
        RDuplicada.appendChild(document.createTextNode(str(autoriza.geterrores()['Referencia_Duplicada'])))
        errores.appendChild(RDuplicada)
        autorizacion.appendChild(errores)

        #facturas correctas
        facCorrectas=document.createElement('FACTURAS_CORRECTAS')
        facCorrectas.appendChild(document.createTextNode(str(autoriza.getfacturasCorrectas())))
        autorizacion.appendChild(facCorrectas)

        #listado autorizaciones
        LAutorizacion=document.createElement('LISTADO_AUTORIZACIONES')
        for apr in autoriza.getlistadoAutorizaciones():
            aprobacion=document.createElement('APROBACION')

            NCEmisor=document.createElement('NIT_EMISOR')
            NCEmisor.setAttribute('ref', str(apr['Referencia']))
            NCEmisor.appendChild(document.createTextNode(str(apr['NitEmisor'])))
            aprobacion.appendChild(NCEmisor)

            NCReceptor=document.createElement('NIT_RECEPTOR')
            NCReceptor.appendChild(document.createTextNode(str(apr['NitReceptor'])))
            aprobacion.appendChild(NCReceptor)

            CodAprobacion=document.createElement('CODIGO_APROBACION')
            CodAprobacion.appendChild(document.createTextNode(str(apr['codigoAutorizacion'])))
            aprobacion.appendChild(CodAprobacion)

            ValorC=document.createElement('VALOR')
            ValorC.appendChild(document.createTextNode(str(apr['valor'])))
            aprobacion.appendChild(ValorC)

            LAutorizacion.appendChild(aprobacion)

            autorizacion.appendChild(LAutorizacion)

        TAprobaciones=document.createElement('TOTAL_APROBACIONES')
        TAprobaciones.appendChild(document.createTextNode(str(len(autoriza.getlistadoAutorizaciones()))))
        LAutorizacion.appendChild(TAprobaciones)

        root.appendChild(autorizacion)
    xmlSalida=root.toprettyxml(indent='\t',encoding='utf8')
    return xmlSalida

def generaXMLFechaNit(fecha,nit):
    document=minidom.Document()
    root=document.createElement('FECHA')
    root.setAttribute('fecha', fecha)

    print(autorizaciones[0].getFecha()==fecha)
    


    for auto in autorizaciones:
        autorizacion=document.createElement('AUTORIZACION')

        if auto.getFecha()==fecha:
            for dato in auto.getlistadoAutorizaciones():
                if dato['NitEmisor']==nit:
                    nit_=document.createElement('NIT')
                    nit_.appendChild(document.createTextNode(nit))
                    autorizacion.appendChild(nit_)

                    ivaE_=document.createElement('IVAEMITIDO')
                    ivaE_.appendChild(document.createTextNode(str(int(dato['valor'])*0.12)))
                    autorizacion.appendChild(ivaE_)
                    

                elif dato['NitReceptor']==nit:
                    nit_=document.createElement('NIT')
                    nit_.appendChild(document.createTextNode(nit))
                    autorizacion.appendChild(nit_)

                    ivaR_=document.createElement('IVARECIBIDO')
                    ivaR_.appendChild(document.createTextNode(str(int(dato['valor'])*0.12)))
                    autorizacion.appendChild(ivaR_)
            break
        root.appendChild(autorizacion)
    xmlSalida=root.toprettyxml(indent='\t',encoding='utf8')
    return xmlSalida


app=Flask(__name__)
cors = CORS(app, resources={r"/*": {"origin": "*"}})

@app.route('/datos',methods=['GET'])
def index():
    archivo= request.data.decode('utf8')
    return str(archivo)

@app.route('/fecha-nit', methods=['GET'])
def ivaNit():
    fecha = request.args.get('fecha')
    nit = request.args.get('nit')

    return generaXMLFechaNit(fecha,nit)
    


    return str(fecha)

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
        valor=verificaValor(child[4].text)
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
                                        auto.agregarAutorizacion({'NitEmisor':nitEmisor,'NitReceptor':nitReceptor,'Referencia':str(referencia),'valor':valor,'codigoAutorizacion':auto.getCorrelativo()})
                                        auto.sumaCorrelativo()
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
    
    return generaXMLSalida()



if __name__=='__main__':
    app.run(debug=True)