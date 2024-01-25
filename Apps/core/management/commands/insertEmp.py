from django.core.management.base import BaseCommand
from Apps.employee.models import EMPLOYEE, DESIGNATIONS
from faker import Faker
from random import randint
from FMS.settings import STATICFILES_DIRS
import os

class Command(BaseCommand):
    help = 'Insertion of Some random employee Data'

    def handle(self, *args, **options):
        faker = Faker()
        self.stdout.write(self.style.SUCCESS('deleting employee data ...'))
        EMPLOYEE.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('employees deleted'))
        
        self.stdout.write(self.style.SUCCESS('Inserting new employees...'))
        try:
            
            for _ in range(0,401):
            
                # Select a random designation
                index = randint(0,len(DESIGNATIONS)-1)
                designation = DESIGNATIONS[index][0]

                # same image
                image = os.path.join(STATICFILES_DIRS[0],"assets/img/img/aboutImage.png")
                
                EMPLOYEE.objects.create(
                    name=faker.name(),
                    email=faker.email(),
                    address=faker.address(),
                    image=image,
                    designation=designation
                )
        except:
            
            self.stdout.write(self.style.ERROR('Error while inserting data'))
        
        
        self.stdout.write(self.style.SUCCESS('Custom command executed successfully'))