import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ['DJANGO_SETTINGS_MODULE'] = 'my_library.settings'
django.setup()

from django.contrib.auth.models import Group, User, Permission
import book_catalog.models as book_catalog_models

print('Create superuser...')
superuser = User.objects.create_superuser(username='admin', email='correo@ejemplo.com', password='1234')
superuser.save()

print('Create staff group...')
Group.objects.create(name='staff')
models_list = ['author', 'book', 'book saga']
# proj_add_perm = [0]*(len(models_list)*4)
actions = ['add', 'change', 'delete', 'view']
for action in actions:
    for model in models_list:
        perm = Permission.objects.get(name=f'Can {action} {model}')
        group = Group.objects.get(name='staff')
        group.permissions.add(perm)

print('Create staff users...')
user_staff_1 = User.objects.create_user(username='staff1', first_name='Staff', last_name='One',
                                        email='staff1@myemail.com', password='staff1')
user_staff_2 = User.objects.create_user(username='staff2', first_name='Staff', last_name='Two',
                                        email='staff2@myemail.com', password='staff2')
user_staff_1.groups.add(Group.objects.get(name='staff'))
user_staff_2.groups.add(Group.objects.get(name='staff'))
user_staff_1.save()
user_staff_2.save()

print('Create users...')
user1 = User.objects.create_user(username='julio', first_name='Julio', last_name='García',
                                 email='julio@myemail.com', password='julio')
user2 = User.objects.create_user(username='teresa', first_name='Teresa', last_name='Aranda',
                                 email='teresa@myemail.com', password='teresa')
user3 = User.objects.create_user(username='luis', first_name='Luis', last_name='García',
                                 email='luis@myemail.com', password='luis')
user4 = User.objects.create_user(username='ana', first_name='Ana', last_name='Aranda',
                                 email='ana@myemail.com', password='ana')
user5 = User.objects.create_user(username='maria', first_name='María', last_name='García',
                                 email='maria@myemail.com', password='maria')

for i in range(1, 45):
    user = User.objects.create_user(username=f'user{i}', first_name='User', last_name=f'{i}',
                                    email=f'user{i}@gmail.com', password=f'user{i}')
