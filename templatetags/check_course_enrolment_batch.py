from django import template
from account.models import Course_Enrolment
register = template.Library()

@register.simple_tag
def get_batch_status(course, user):

    try:
        course_enrolment = Course_Enrolment.objects.get(course_id=course,user=user)
        return course_enrolment.batch

    except:
        return None
