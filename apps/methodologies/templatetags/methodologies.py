from django import template

register = template.Library()


@register.filter
def parse_command(obj, request):
    parsed_command = obj.parse_command(target_ip=request.GET.get('target_ip'),
                                       target_port=request.GET.get('target_port'),
                                       target_domain=request.GET.get('target_domain'),
                                       target_scheme=request.GET.get('target_scheme'))
    return parsed_command
