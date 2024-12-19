from mcq_test.models import Response
from django.template import Library
from datetime import datetime

 
register = Library()
 
@register.simple_tag
def check_answer(question_id, user, attempt):
    try:
        response = Response.objects.get(question=question_id,attempt=attempt,user=user)
        return response
    except:
        status =[]
        return status