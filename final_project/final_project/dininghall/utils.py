from .models import table_session, table_time

def get_all_session_objects():
    return table_session.objects.all()

def get_time_objects(session_id):
    return table_time.objects.filter(session_id=session_id)

def save_session_and_times(form_session, form_time):
    session = form_session.save()
    times = form_time.save(commit=False)
    for time in times:
        time.session = session
        time.available_seat = time.limit_seat
        time.save()

def get_session_by_id(session_id):
    return table_session.objects.get(pk=session_id)

def update_session(form):
    form.save()
    
def delete_session_object(menu):
    menu.delete()
