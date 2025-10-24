from  datetime import datetime, timezone

class CUtil:

    def __init__(self):
        None
    
    def DataHoraIsoBuscar(self, ano, mes, dia, hora, minuto, segundo):
        
        retorno = datetime(year=ano, month=mes,day=dia, hour=hora, minute=minuto, second=segundo)
        retorno = retorno.isoformat(timespec='milliseconds') + 'Z'    
        return retorno        
    
    def DataHoraBuscar(self):
        
        agora = datetime.now()
        retorno =     self.DataHoraIsoBuscar(ano=agora.year, mes=agora.month, dia=agora.day, hora=agora.hour, minuto=agora.minute, segundo=agora.second)
        return retorno

