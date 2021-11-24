from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib import admin, messages
from django.contrib.admin.options import IS_POPUP_VAR
from django.contrib.admin.utils import unquote
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import PermissionDenied
from django.db import router, transaction
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.utils.translation import gettext, gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from jet.admin import CompactInline
from .helpers import in_group
from . import models
from . import notifications


from django.contrib.auth.models import User, Group
admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.site_header = "HR"
admin.site.site_title = "HR"
admin.site.index_title = "Bienvenue à HR Portail"


class CongeInline(admin.TabularInline):
    model = models.Conge
    extra = 1


class UserInline(admin.StackedInline):
    model = models.User


class TaskInline(admin.TabularInline):
    model = models.Task
    fields = ("name", "assigned_to", "status")
    extra = 1


class DossierEmployeInline(admin.StackedInline):
    model = models.DossierEmploye
    fields = ('phone', ('departement', 'title'), 'embauche')
    inlines = (
        CongeInline,
        TaskInline,
    )


class DossierClientInline(admin.StackedInline):
    model = models.DossierClient


@admin.register(models.Employe)
class EmployeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'username', 'last_name', 'email')
    inlines = [
        DossierEmployeInline,
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.is_staff = True
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)

    def get_fields(self, request, obj=None):
        if obj:
            return (('first_name', 'last_name'), ('username', 'email'),
                    'groups')
        else:
            return (('first_name', 'last_name'), ('username', 'email'),
                    'groups', 'password')

    def get_changeform_initial_data(self, request):
        return {
            'is_active': True,
            'is_staff': True,
        }

    def get_queryset(self, request):
        from .permissions import Developer, Project_Manager
        qs = super().get_queryset(request).filter(
            groups__in=(Developer, Project_Manager))
        return qs

    class Media:
        js = (
            '//unpkg.com/push.js@1.0.9/bin/push.min.js',
            'pm/js/notificaitons.js',
        )


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'username', 'last_name', 'email')
    inlines = [
        DossierClientInline,
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.is_staff = True
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)

    def get_changeform_initial_data(self, request):
        return {
            'is_active': True,
            'is_staff': True,
        }

    def get_fields(self, request, obj=None):
        if obj:
            return (('first_name', 'last_name'), ('username', 'email'),
                    'groups', 'is_active')
        else:
            return (('first_name', 'last_name'), ('username', 'email'),
                    'groups', 'is_active', 'password')

    def get_queryset(self, request):
        from .permissions import Client
        qs = super().get_queryset(request).filter(groups=Client)
        return qs

    class Media:
        js = (
            '//unpkg.com/push.js@1.0.9/bin/push.min.js',
            'pm/js/notificaitons.js',
        )


@admin.register(models.Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ('name', 'departement', 'debut', 'fin')

    class Media:
        js = (
            '//unpkg.com/push.js@1.0.9/bin/push.min.js',
            'pm/js/notificaitons.js',
        )


'''
@admin.register(models.Conge)
class CongeAdmin(admin.ModelAdmin):
    list_display = ('employe', 'debut', 'fin', 'status')
    fields = ('debut', 'fin', 'status', 'employe')
    readonly_fields = ('status', 'employe')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or RH in request.user.groups.all():
            return qs
        return qs.filter(employe=request.user)

    def get_changeform_initial_data(self, request):
        return {
            'employe': request.user,
        }

    def get_readonly_fields(self, request, obj=None):
        if not obj and (
                request.user.is_superuser or RH in request.user.groups.all()):
            return []
        return ['status', 'employe']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.employe = request.user
        super().save_model(request, obj, form, change)
'''


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'priority', 'project_lead', 'progress')
    readonly_fields = ('progress', )
    fields = ('name', 'description', 'client', 'project_lead', 'team',
              'priority', 'start_at', 'end_at')
    inlines = [
        TaskInline,
    ]

    def progress(self, obj):
        # print(obj.task_set.all().values('status').annotate(count=Count('status')))
        done = obj.task_set.filter(status='C').count()
        all = obj.task_set.count()
        if all:
            per = int((done / all) * 100)
        else:
            per = 0
        return format_html(f'''
            <progress value="{per}" max="100" readonly></progress>
            <span style="font-weight:bold">{per}%</span>
        ''')
    progress.allow_tags = True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if in_group(request.user, ["admin", "pm"]):
            return qs
        elif in_group(request.user, ["dev"]):
            return qs.filter(team__employe=request.user)
        elif in_group(request.user, ["client"]):
            return qs.filter(client__client=request.user)

    class Media:
        js = (
            '//unpkg.com/push.js@1.0.9/bin/push.min.js',
            'pm/js/notificaitons.js',
        )


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'assigned_to', 'status', 'project')
    list_editable = ('status',)
    search_fields = ('name', 'description')
    # list_filter = ('project__name', 'assigned_to__employe__username', 'status')

    def mark_completed(self, obj):
        act = obj.status == "D"
        if act:
            return format_html(f"""
                <a class="button" href="{obj.id}/completed">Confirm Completed</a>
            """)

    def get_list_display(self, request):
        if in_group(request.user, ["client"]):
            return ('name', 'assigned_to', 'status', 'project', 'progress', 'mark_completed')
        else:
            return ('name', 'assigned_to', 'status', 'project', 'progress')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if in_group(request.user, ["admin", "pm"]):
            return qs
        elif in_group(request.user, ["dev"]):
            return qs.filter(assigned_to__employe=request.user)
        elif in_group(request.user, ["client"]):
            return qs.filter(project__client__client=request.user)

    def get_urls(self):
        urls = super().get_urls()
        return [
            path('<int:task_id>/completed/', self.set_completed, name="completed"),
        ] + urls

    def set_completed(self, request, task_id):
        models.Task.objects.filter(id=task_id).update(status="C")
        return redirect("../..")

    def progress(self, obj):
        per = obj.progress()
        return format_html(f'''
            <progress value="{per}" max="100" readonly></progress>
            <span style="font-weight:bold">{per}%</span>
        ''')
    progress.allow_tags = True

    class Media:
        js = (
            '//unpkg.com/push.js@1.0.9/bin/push.min.js',
            'pm/js/notificaitons.js',
        )



'''
@admin.register(models.Pointage)
class PointageAdmin(admin.ModelAdmin):
    list_display = ('employe', 'type', 'temp')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or RH in request.user.groups.all():
            return qs
        return qs.filter(employe=request.user)
'''

admin.site.register(models.Departement)
admin.site.register(models.JobTitle)

admin.site.register(models.Document)

# admin.site.register(models.Message)
