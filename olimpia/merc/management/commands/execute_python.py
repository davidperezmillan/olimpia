from django.core.management.base import BaseCommand
import os
 
 
class Command(BaseCommand):
    help = "Ejecuta archivo python archivo_a_ejecutar.py"
 
    def handle(self, *args, **options):
        
        
        self.stdout.write('Ejecutando comando')
        os.system("python archivo_a_ejecutar.py")