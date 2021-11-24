from django.utils.translation import ugettext_lazy as _
from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard, AppIndexDashboard
from . import models
from . import views


class RecentTasks(modules.DashboardModule):
    title = 'Recent Tasks'
    template = 'pm/recent_tasks.html'

    def init_with_context(self, context):
        self.tasks = models.Task.related_tasks(context.request.user)\
            .order_by("-updated_at")[:5]


class Chat(modules.DashboardModule):
    title = 'Chat Box'
    template = 'pm/chat-container.html'

    def init_with_context(self, context):
        # self.children = Ticket.objects.order_by('-date_add')[:self.limit]
        pass


class Charts(modules.DashboardModule):
    title = 'Charts'
    template = 'pm/charts.html'

    def init_with_context(self, context):
        self.projects = views.list_projects_dict(context.request)
        print("projects:", self.projects)


class CustomIndexDashboard(Dashboard):
    columns = 2

    def init_with_context(self, context):
        # self.available_children.append(modules.LinkList)
        """
        self.children.append(modules.LinkList(
            _('Support'),
            children=[
                {
                    'title': _('Django documentation'),
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': _('Django "django-users" mailing list'),
                    'url': 'http://groups.google.com/group/django-users',
                    'external': True,
                },
                {
                    'title': _('Django irc channel'),
                    'url': 'irc://irc.freenode.net/django',
                    'external': True,
                },
            ],
            column=0,
            order=0
        ))
        self.children.append(modules.ModelList(
            _('Models'),
            exclude=('auth.*',),
            column=1,
            order=2
        ))
        """
        self.children.append(Charts(
            _('Charts'),
        ))
        self.children.append(Chat(
            _('Chat Box'),
        ))
        self.children.append(RecentTasks(
            _('Recent Tasks'),
        ))
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            exclude=('auth.*',),
        ))
        self.children.append(modules.AppList(
            _('Applications'),
            column=0,
            order=1,
        ))
