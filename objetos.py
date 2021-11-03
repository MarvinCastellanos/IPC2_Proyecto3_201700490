class Autorizacion:
    def __init__(self,fecha):
        self.fecha=fecha
        self.facturasRecibidas=0
        self.errores={'Nit_Emisor':0,'Nit_Receptor':0,'Iva':0,'Total':0,'Referencia_Duplicada':0}
        self.facturasCorrectas=0
        self.cantidadEmisores=0
        self.cantidadReceptores=0
        self.listadoAutorizaciones=[]

    
    def getFecha(self):
        return self.fecha

    def getfacturasRecibidas(self):
        return self.facturasRecibidas

    def geterrores(self):
        return self.errores
    
    def getfacturasCorrectas(self):
        return self.facturasCorrectas

    def getcantidadEmisores(self):
        return self.cantidadEmisores

    def getcantidadReceptores(self):
        return self.cantidadReceptores

    def getlistadoAutorizaciones(self):
        return self.listadoAutorizaciones