from django import template


register = template.Library()


@register.simple_tag
def form_model_verbose_name(form):
    """ Returns verbose_name for a form model. """

    return form._meta.model._meta.verbose_name.title()


@register.simple_tag(takes_context=True)
def section_name(context):
    """ Finds the section name for a given url """

    url_name_suffixes = ['{}-list', '{}-create', '{}-update', '{}-delete', '{}-list-nodes', '{}-copy']
    url_name = context['request'].resolver_match.url_name

    if url_name in [s.format('asset') for s in url_name_suffixes]:
        return 'asset'

    if url_name in [s.format('contact') for s in url_name_suffixes]:
        return 'contact'

    if url_name in [s.format('file') for s in url_name_suffixes]:
        return 'file'

    if url_name in [s.format('note') for s in url_name_suffixes]:
        return 'note'

    if url_name in [s.format('task') for s in url_name_suffixes]:
        return 'task'


@register.filter()
def klass(value):
    return value.__class__.__name__
