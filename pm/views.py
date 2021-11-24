from django.shortcuts import render
from django.contrib.humanize.templatetags.humanize import NaturalTimeFormatter
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.forms.models import model_to_dict
from django.db.models import Q, Count

from .helpers import json_view
from . import models


@csrf_exempt
@json_view()
def me(request):
    return model_to_dict(request.user, fields=(
        'first_name', 'last_name', 'username', 'email', 'id'))


def list_projects_dict(request):
    ps = models.Project.related_projects(request.user)
    ps = [
        model_to_dict(em, fields=(
            'name', 'id', 'description', 'priority', 'start_at', 'end_at'))
        for em in ps
    ]
    s = models.Task.objects\
        .filter(project_id__in=[p['id'] for p in ps])\
        .values('project_id', 'status').annotate(count=Count('status'))
    p_s = {}
    for p in ps:
        p_s[p['id']] = {
            'N': 0,
            'W': 0,
            'D': 0,
            'C': 0,
        }
    for _s in s:
        p_s[_s['project_id']][_s['status']] = _s['count']

    for p in ps:
        p['status'] = p_s[p['id']]

    return ps


@csrf_exempt
@json_view()
def list_projects(request):
    ps = list_projects_dict(request)
    return {"projects": ps}


def chat(request):

    return render(request, "pm/chat.html")


@csrf_exempt
@json_view()
def messages_list(request):
    msgs = models.Message.objects.all()
    chat = []
    for msg in msgs:
        m = {
            "from": msg.src.username,
            "content": msg.content,
            "time": NaturalTimeFormatter.string_for(msg.time),
            "id": msg.id,
            "type": msg.type,
            "project": msg.project_id,
        }
        chat.append(m)
    return {"messages": chat}


@csrf_exempt
@json_view()
def send(request):
    models.Message.objects.create(
        src=request.user,
        project_id=request.json['project'],
        content=request.json['content'],
    )
    return {}


@csrf_exempt
@json_view()
def events_list(request, employe):
    missions = Mission.objects.filter(employe__username=employe)[:]
    conges = Conge.objects.filter(employe__username=employe, status=1)[:]
    formations = Formation.objects.all()[:]
    evts = []
    for m in missions:
        evts.append({
            "type": "mission",
            "id": m.id,
            "employe": employe,
            "titre": m.titre,
            "description": m.description,
            "debut": m.debut,
            "fin": m.fin,
        })
    for c in conges:
        evts.append({
            "type": "conge",
            "id": c.id,
            "employe": employe,
            "titre": "Conge",
            "description": "Conge Confirmé",
            "debut": c.debut,
            "fin": c.fin,
        })
    for f in formations:
        evts.append({
            "type": "formation",
            "id": f.id,
            "employe": employe,
            "titre": f.titre,
            "description": f.description,
            "debut": f.debut,
            "fin": f.fin,
        })
    return {"events": evts}
