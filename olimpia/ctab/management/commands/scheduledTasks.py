from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User
from ctab.models import Tasks

from datetime import datetime
import re, shlex

# Importacion para llamar a comandos
from django.core.management import call_command
# 



import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)
 
class Command(BaseCommand):
    help = "Vamos a lanzar las diferentes tareas programados"
 
    def add_arguments(self, parser):
        pass
        # # Positional arguments
        # parser.add_argument('author', nargs=1, type=str)
        
        # # Named (optional) arguments
        # parser.add_argument(
        #     '--delete',
        #     action='store_true',
        #     dest='delete',
        #     help='Borramos la carpeta origen',
        # )
        # parser.add_argument(
        #     '--nomsg',
        #     action='store_true',
        #     dest='nomsg',
        #     help='No enviamos msg-telegram',
        # )
       


    def handle(self, *args, **options):
        logger.info("INICIO")
        # DEV 
        # logger.setLevel(logging.INFO)

        # Vamos a comprobar los tareas que se van a realizar
        lista_de_tareas = Tasks.objects.all().filter(activo=True)
        

        lista_de_ejecuciones=[]
        
        # Filtramos
        for task in lista_de_tareas:
            
            se_lanza = self.check_task(task)
            if (se_lanza):
                logger.debug("SIIIIII [[ {} es lanzada ]]".format(task.descrip))
                lista_de_ejecuciones.append(task)
            else:
                logger.debug("NOOOOOO [[ {} Omitida ]]".format(task.descrip))
        
        
        
        
        # Vamos a realizar las tareas que nos toca
        logger.info("Tareas {tareas},".format(tareas=lista_de_ejecuciones))
        for task_ejecutable in lista_de_ejecuciones:
            logger.info("Tarea --> {tarea},".format(tarea=task_ejecutable))
            command, tOption = task_ejecutable.task.split(" ",1)
            options = shlex.split(tOption)
            logger.debug("{} {}".format(command,options))
            try:
                call_command(command,*options)
                task_ejecutable.ultima = datetime.now()
                task_ejecutable.save()
 
            except Exception, e:
                 logger.error("ERROR EN LA TAREA {} ".format(task_ejecutable.descrip))
        
        
        logger.info('Successfully')
        
        
    def check_task(self, task):
        
        # Debemos comprobar todos los campos
        # el orden ???? TODO
        # 
        # 
        # 
        # La hora y el minuto seran los ultimos ????
        # 
        
        se_lanza = True
        if se_lanza:
            today = datetime.now()
            month = today.month
            type_field,se_lanza = self.check_data(task.mes,month)
            logger.debug("Check MES {} = {} {} tipo {}".format(task.mes,month,se_lanza,type_field))
            if se_lanza:
                dayofmonth= today.day
                type_field,se_lanza = self.check_data(task.diames,dayofmonth)
                logger.debug("Check DiaMes {} = {} {} tipo {}".format(task.diames,dayofmonth,se_lanza,type_field))
                if se_lanza:
                    weekday = int(today.weekday())
                    type_field,se_lanza = self.check_data(task.diasemana,weekday)
                    logger.debug("Check DiaSemana {} = {} {} tipo {}".format(task.diasemana,weekday,se_lanza,type_field))
                    if se_lanza:
                        hour = today.hour
                        type_field,se_lanza = self.check_data(task.hora,hour)
                        logger.debug("Check hora {} = {} {} tipo {}".format(task.hora,hour,se_lanza,type_field))
                        if se_lanza:
                            minute = today.minute
                            type_field,se_lanza = self.check_data(task.minuto,minute)
                            logger.debug("Check minute {} = {} {} tipo {}".format(task.minuto,minute,se_lanza,type_field))
        
        
        return se_lanza

    def check_data(self,data,find):
    
        type_field = ""
        today = datetime.now()
        # Posibles campos
        # * Todos
        # 0-9 Rango
        # 9 Unico
        # check type field
        cons_DEFAULT = r"(\*)"
        cons_RANGO = r"(\d{1,2}-\d{1,2})"
        cons_PARTE = r"(\d{1,2}\/\d{1,2})"
        cons_COMAS = r"(\,)"
        cons_UNICO = r"(\d{1,2})"
        
        if re.search(cons_DEFAULT,data):
            # *
            type_field = ("default");
            return type_field, True
        if re.search(cons_RANGO,data):
            # Rango
            type_field = ("rango");
            valores = data.split("-")
            if (find>valores[0] and find<valores[1]):
                return type_field, True
        if re.search(cons_PARTE,data):
            # Proprocion
            type_field = ("Parte");
            valores = data.split("/")
            if find is valores[0]:
                return type_field, True
            if find % int(valores[1]) is 0:
                return type_field, True    
        if re.search(cons_COMAS,data):
            # Comas
            type_field = ("comas");
            valores = data.split(",")
            if str(find) in valores:
                return type_field, True   
        if re.search(cons_UNICO,data):
            type_field = ("unico")
            if find == data:
                return type_field, True
        
        return type_field, False
        
        
      
 
        
        
