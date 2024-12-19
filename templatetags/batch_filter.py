from django import template
from account.models import Course_Enrolment
register = template.Library()


@register.simple_tag
def get_batch(course, user):
    course_enrolment=Course_Enrolment.objects.get(user=user,course=course)
    return course_enrolment