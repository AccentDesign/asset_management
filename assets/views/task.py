import calendar
import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from assets.models import Task


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'assets/task_list.html'

    def get_date(self):
        year = self.request.GET.get('year')
        month = self.request.GET.get('month')
        day = self.request.GET.get('day')
        if year and month and day:
            return datetime.date(int(year), int(month), int(day))
        return datetime.datetime.today().date()

    def get_queryset(self):
        queryset = Task.objects.due_by_date(self.get_date())
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'date': self.get_date()
        })
        return context
