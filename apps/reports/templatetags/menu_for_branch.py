from django import template
from apps.core.models import Branch, Employee

register = template.Library()


@register.simple_tag(takes_context=True)
def show_branch_menu(context):
    request = context['request']
    user = request.user
    if user.is_authenticated:
        try:
            employee = Employee.objects.get(user=user)
            branch = employee.branch
            if branch.adult and branch.child:
                return "show_both_menu"
            elif branch.adult:
                return "show_adult_menu"
            elif branch.child:
                return "show_child_menu"
            else:
                return "hide_menu"
        except Employee.DoesNotExist:
            return "hide_menu"
    else:
        return "hide_menu"