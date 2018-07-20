import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import ListView, UpdateView

from assets.forms import TaskForm, TaskHistoryForm
from assets.models import Task, TaskStatus


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


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    prefix = 'task_form'

    def get_history_form(self):
        if self.request.method == 'POST':
            return TaskHistoryForm(self.request.POST, prefix='history_form')
        return TaskHistoryForm(initial={'task': self.object}, prefix='history_form')

    def get_context_data(self, **kwargs):
        if 'history_form' not in kwargs:
            kwargs['history_form'] = self.get_history_form()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.get_form()
        history_form = self.get_history_form()

        if 'task_update' in self.request.POST and form.is_valid():
            return self.form_valid(form)

        if 'history_notes' in self.request.POST and history_form.is_valid():
            history_form.save()
            return HttpResponseRedirect(self.get_success_url())

        if 'history_complete' in self.request.POST and history_form.is_valid():
            status, created = TaskStatus.objects.get_or_create(name='Completed')
            history_form.instance.status = status
            history_form.save()
            return HttpResponseRedirect(self.get_success_url())

        context = self.get_context_data(form=form, history_form=history_form)
        return self.render_to_response(context)
