from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from . import models

Admin, created = Group.objects.get_or_create(name='Admin')
Project_Manager, created = Group.objects.get_or_create(name='Project Manager')
Developer, created = Group.objects.get_or_create(name='Developer')
Client, created = Group.objects.get_or_create(name='Client')


try:
    system = models.User.objects.create_superuser(
        "system", "system@localhost", "system")
except IntegrityError:
    system = models.User.objects.get(username="system")
system.groups.add(Admin)

try:
    admin = models.User.objects.create_superuser(
        "admin", "webmaster@localhost", "admin")
except IntegrityError:
    admin = models.User.objects.get(username="admin")
admin.groups.add(Admin)

try:
    pm = models.User.objects.create_user("pm", "pm@localhost", "pm")
    pm.is_staff = True
    pm.save()
except IntegrityError:
    pm = models.User.objects.get(username="pm")
pm.groups.add(Project_Manager)

try:
    dev = models.User.objects.create_user("dev", "dev@localhost", "dev")
    dev.is_staff = True
    dev.save()
except IntegrityError:
    dev = models.User.objects.get(username="dev")
dev.groups.add(Developer)

try:
    client = models.User.objects.create_user(
        "client", "client@localhost", "client")
    client.is_staff = True
    client.save()
except IntegrityError:
    client = models.User.objects.get(username="client")
client.groups.add(Client)

permissions = {
    Project_Manager: {
        "user": ["view"],
        "employe": ["view"],
        "client": ["view"],
        "departement": ["view"],
        "jobtitle": ["view"],
        "dossieremploye": ["view"],
        "dossierclient": ["view"],
        "project": ["edit", "view", "add", "change"],
        "task": ["edit", "view", "add", "delete", "change"],
        "conge": ["edit", "view", "add", "change"],
        "formation": ["edit", "view", "add", "change"],
        "document": ["edit", "view", "add", "change"],
        "message": ["edit", "view", "add", "change"],
        "pointage": ["edit", "view", "add", "change"],
    },
    Developer: {
        "user": ["view"],
        "employe": ["view"],
        "client": [],
        "departement": ["view"],
        "jobtitle": ["view"],
        "dossieremploye": ["view"],
        "dossierclient": [],
        "project": ["view"],
        "task": ["edit", "view", "add", "change"],
        "conge": ["view", "add"],
        "formation": ["view"],
        "document": ["view", "add"],
        "message": ["view", "add"],
        "pointage": ["view", "add"],
    },
    Client: {
        "user": [],
        "employe": [],
        "client": [],
        "departement": [],
        "jobtitle": [],
        "dossieremploye": [],
        "dossierclient": [],
        "project": ["view"],
        "task": ["view"],
        "conge": [],
        "formation": [],
        "document": [],
        "message": ["view", "add"],
        "pointage": [],
    },
}

for group, config in permissions.items():
    codes = set.union(*[{ac + "_" + md for ac in actions}
                        for md, actions in config.items()])
    perms = Permission.objects.filter(codename__in=codes)
    group.permissions.set(perms)
