from django import template


register = template.Library()


@register.simple_tag
def form_model_verbose_name(form):
    """ Returns verbose_name for a form model. """

    return form._meta.model._meta.verbose_name.title()
