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
        print(fecha)
        try:
            fechaHora=datetime.datetime(int(year),int(mes),int(dia))
            print('Fecha correcta')
        except ValueError:
            print('fecha Incorrecta')
        
def verificaNit(nit):
    if len(nit)>21:
        print('nit invalido')
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
        for numero in range(len(nitA)):
            sum+=int(nitA[numero])*(numero+2)
        mod=sum%11
        modR=11-mod
        modMod=modR%11
        if modMod==int(nit[len(nit)-1]):
            print('nit valido')
        else:
            print('Nit invalido')

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
        print('iva correcto '+str(ivaP))
    else:
        print('iva incorrecto '+str(ivaP))

def verificaTotal(valor, iva, valorP):
    valor=float(valor)
    iva=float(iva)
    valorP=float(valorP)

    if valorP==valor+iva:
        print('valor correcto')
    else:
        print('valor Incorrecto')

def verificaReferencia(ref):
    if len(ref)>40:
        print('referencia invalida')
    else:
        print('referencia valida')

verificaNit('99990237')