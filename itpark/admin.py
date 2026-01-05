from django.contrib import admin
from .models import Course, Mentor, Student, Group


admin.site.register([Course, Mentor, Student, Group])

