class Autorizacion:
    def __init__(self,fecha,correlativo):
        self.fecha=fecha
        self.facturasRecibidas=0
        self.errores={'Nit_Emisor':0,'Nit_Receptor':0,'Iva':0,'Total':0,'Referencia_Duplicada':0}
        self.facturasCorrectas=0
        self.cantidadEmisores=0
        self.cantidadReceptores=0
        self.listadoAutorizaciones=[] #{"nitEmisor":0,NitReceptor:0,Referencia:0,CodigoAprobacion:0,valor:0}
        self.correlativo=int(correlativo)*10000000+1

    def sumaCorrelativo(self):
        self.correlativo+=1

    def getCorrelativo(self):
        return self.correlativo
        
    def sumaErrorNitEmisor(self):
        self.errores["Nit_Emisor"]+=1

    def sumaErrorNitReceptor(self):
        self.errores['Nit_Receptor']+=1
    
    def sumaErrorIva(self):
        self.errores["Iva"]+=1

    def sumaErrorTotal(self):
        self.errores["Total"]+=1

    def sumaErrorReferenciaDuplicada(self):
        self.errores['Referencia_Duplicada']+=1

    def getFecha(self):
        return self.fecha

    def getfacturasRecibidas(self):
        return self.facturasRecibidas
    
    def sumaFacturasRecividas(self):
        self.facturasRecibidas+=1

    def geterrores(self):
        return self.errores
    
    def getfacturasCorrectas(self):
        return self.facturasCorrectas
    
    def sumaFacturasCorrectas(self):
        self.facturasCorrectas+=1

    def getcantidadEmisores(self):
        return self.cantidadEmisores
    
    def sumaCantidadEmisores(self):
        self.cantidadEmisores+=1

    def getcantidadReceptores(self):
        return self.cantidadReceptores
    
    def sumaCantidadReceptores(self):
        self.cantidadReceptores+=1

    def getlistadoAutorizaciones(self):
        return self.listadoAutorizaciones

    def agregarAutorizacion(self,autorizacion):
        self.listadoAutorizaciones.append(autorizacion)