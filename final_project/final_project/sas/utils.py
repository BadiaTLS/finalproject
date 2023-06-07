from .models import table_classes
from final_project.accounts.models import CustomUser

def get_all_user():
    return CustomUser.objects.all()

def get_all_class():
    return table_classes.objects.all()