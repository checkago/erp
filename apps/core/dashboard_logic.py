from django.contrib.auth.models import Group

def get_data_for_user(user):
    if user.groups.filter(name='Администрация').exists():
        return {
            "totals": get_totals_for_administration(user),
            "other_data": get_other_data_for_administration(user),
            "template": "general/dashboard/dashboard_administration.html",
        }
    elif user.groups.filter(name='Методисты').exists():
        return {
            "totals": get_totals_for_metodists(user),
            "other_data": get_other_data_for_metodists(user),
            "template": "general/dashboard/dashboard_metodists.html",
        }
    elif user.groups.filter(name='Сотрудники библиотек').exists():
        return {
            "totals": get_totals_for_branch_emploeeyers(user),
            "other_data": get_other_data_for_branch_emploeeyers(user),
            "template": "general/dashboard/dashboard_branch.html",
        }
    else:
        return {
            "template": "general/dashboard/blank_template.html",
        }
