from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import (
    User, DossierEmploye, Pointage, Message, Document, Formation, Conge,
    Task
)
from .permissions import system


@receiver(post_save, sender=Task)
def post_task(sender, instance, created, raw, using, **kwargs):
    print("post_task:", kwargs)
    if created:
        Message.objects.create(
            src=system,
            project=instance.project,
            content=f"{instance.assigned_to} got new task: {instance.name}",
            type="notification",
        )
    else:
        Message.objects.create(
            src=system,
            project=instance.project,
            content=f"Task updated: {instance.name}",
            type="notification",
        )


@receiver(post_save, sender=Document)
def post_document(sender, instance, created, raw, using, **kwargs):
    print("post_task:", kwargs)
    if created:
        Message.objects.create(
            src=system,
            project=instance.project,
            type="document",
            content=f"""\
<i class="fa fa-file"></i> <a href="http://localhost:8000/upload/{instance.fichier}" target="_blank">{instance.titre}</a><br>
{instance.description}\
""",
            )



'''
@receiver(post_save, sender=Conge)
def post_conge(sender, instance, created, raw, using, **kwargs):
    if created:
        for rh in User.objects.filter(groups=RH):
            Message.objects.create(
                enoyeur=instance.employe,
                destinaire=rh,
                text=f"""
<b>Demande Conge:</b><br>
User: {instance.employe}<br>
Debut: {instance.debut}<br>
Fin: {instance.fin}<br>
""",
            )
    else:
        Message.objects.create(
            enoyeur=system,
            destinaire=instance.employe,
            text=f"""
<b>Conge etat change:</b><br>
Debut: {instance.debut}<br>
Fin: {instance.fin}<br>
Etat: {instance.get_status_display()}<br>
"""
        )
'''
