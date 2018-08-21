from datetime import datetime

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.views.generic import ListView, UpdateView

from assets.forms import TaskForm, TaskHistoryForm, TaskListFilterForm
from assets.models import Task, Status
from authentication.views.mixins import ActivatedTeamRequiredMixin


class TaskList(ActivatedTeamRequiredMixin, ListView):
    model = Task
    template_name = 'assets/task_list.html'

    def get_filter_form(self):
        if 'due_date' in self.request.GET:
            return TaskListFilterForm(self.request.GET)
        return TaskListFilterForm({'due_date': datetime.now().date()})

    def get_queryset(self):
        filters = self.get_filter_form()

        if filters.is_valid():
            queryset = Task.objects.due_by_date(
                date=filters.cleaned_data['due_date'],
                assigned_to=filters.cleaned_data.get('assigned_to')
            )
        else:
            queryset = Task.objects.due_by_date()

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'filter_form': self.get_filter_form()
        })
        return context


class TaskUpdate(ActivatedTeamRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    prefix = 'task_form'
    success_message = 'updated successfully'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related('history__user')

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
            messages.success(request, 'notes added successfully')
            return HttpResponseRedirect(self.get_success_url())

        if 'history_complete' in self.request.POST and history_form.is_valid():
            status, created = Status.objects.get_or_create(name='Completed')
            history_form.instance.status = status
            history_form.save()
            messages.success(request, 'completed successfully')
            return HttpResponseRedirect(self.get_success_url())

        context = self.get_context_data(form=form, history_form=history_form)
        return self.render_to_response(context)
