from django.db import models
from django.contrib.auth.models import User as DefaultUser
from ckeditor.fields import RichTextField


class User(DefaultUser):
    class Meta:
        proxy = True

    def __str__(self):
        if self.first_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.username


class Employe(User):
    class Meta:
        verbose_name = "Staff"
        proxy = True


class Client(User):
    class Meta:
        proxy = True


class Departement(models.Model):
    titre = models.CharField(max_length=120)

    def __str__(self):
        return self.titre


class JobTitle(models.Model):
    title = models.CharField(max_length=120)

    def __str__(self):
        return self.title


class DossierEmploye(models.Model):
    employe = models.OneToOneField(Employe, on_delete=models.CASCADE, related_name='employe')
    embauche = models.DateField()
    # paiement = models.FloatField()
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)
    title = models.ForeignKey(JobTitle, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12, blank=True, null=True)

    def __str__(self):
        return str(self.employe)

    class Meta:
        verbose_name = "Staff Profile"


class DossierClient(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='client')
    phone = models.CharField(max_length=12, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.client)

    class Meta:
        verbose_name = "Client Profile"


class Project(models.Model):
    PRIORITY = (
        ("H", "High"),
        ("M", "Medium"),
        ("L", "Low"),
    )

    name = models.CharField(max_length=240, unique=True)
    description = RichTextField(blank=True)
    client = models.ForeignKey(DossierClient, on_delete=models.CASCADE)
    start_at = models.DateField(blank=True, null=True)
    end_at = models.DateField(blank=True, null=True)
    priority = models.CharField(max_length=1, choices=PRIORITY, default="M")
    project_lead = models.ForeignKey(
        DossierEmploye, on_delete=models.CASCADE, related_name="projects_lead")
    team = models.ManyToManyField(DossierEmploye, related_name="projects_dev")

    def __str__(self):
        return self.name

    @staticmethod
    def related_projects(user):
        ps = Project.objects
        if user.is_superuser:
            ps = ps.all()
        else:
            ps = ps.filter(
                models.Q(team__employe=user) |
                models.Q(project_lead__employe=user) |
                models.Q(client__client=user)
            )
        return ps


class Task(models.Model):
    STATUS = (
        ('N', 'New'),
        ('W', 'Work In Progess'),
        ('D', 'Done'),
        ('C', 'Closed'),
    )
    name = models.CharField(max_length=250)
    description = RichTextField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(
        DossierEmploye, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS, default='N')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @staticmethod
    def related_tasks(user):
        ps = Task.objects
        if user.is_superuser:
            ps = ps.all()
        else:
            ps = ps.filter(
                models.Q(project__team__employe=user) |
                models.Q(project__project_lead__employe=user) |
                models.Q(project__client__client=user)
            )
        return ps

    def progress(self):
        pers = {
            "N": 0,
            "W": 30,
            "D": 80,
            "C": 100
        }
        return pers[self.status]


class Conge(models.Model):
    STATUS = (
        (0, 'Request'),
        (1, 'Confirmed'),
        (2, 'Rejected'),
    )
    employe = models.ForeignKey(DossierEmploye, on_delete=models.CASCADE)
    debut = models.DateField()
    fin = models.DateField()
    status = models.IntegerField(default=0, choices=STATUS)


class Formation(models.Model):
    name = models.CharField(max_length=200)
    description = RichTextField()
    debut = models.DateField()
    fin = models.DateField()
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Training"


class Document(models.Model):
    titre = models.CharField(max_length=80)
    description = RichTextField(blank=True, null=True)
    fichier = models.FileField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.titre


class Message(models.Model):
    MSG_TYPE = (
        ('message', 'message'),
        ('document', 'document'),
        ('notificaton', 'notification')
    )
    src = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sender")
    content = RichTextField()
    time = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=12, choices=MSG_TYPE, default="message", editable=False)
    # attachment = models.FileField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.text)


class Pointage(models.Model):
    TYPES = (
        (0, 'entre'),
        (1, 'sortie'),
        (2, 'mission'),
        (3, 'pause'),
    )
    employe = models.ForeignKey(User, on_delete=models.CASCADE)
    temp = models.DateTimeField(auto_now_add=True)
    type = models.IntegerField(choices=TYPES, default=0)

    def __str__(self):
        return str(self.temp)
