from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import RegexValidator


class Course(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'AC', 'Active'
        INACTIVE = 'INAC', 'Inactive'

    class Subject(models.TextChoices):
        PROGRAMMING = 'PROGRAM', 'Programming'
        ENGLISH = 'EN', 'English'
        DESIGN = 'DESIGN', 'Design'

    title = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, 
        choices=Status.choices,
        default=Status.INACTIVE
    )
    subject = models.CharField(
        max_length=50,
        choices=Subject.choices
    )
    duration_month = models.PositiveSmallIntegerField(
        default=6,
        validators=[MinValueValidator(1), MaxValueValidator(24)]
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        ordering = ['title']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class Mentor(models.Model):
    class Level(models.TextChoices):
        JUNIOR = 'JUNIOR', 'Junior'
        MIDDLE = 'MIDDLE', 'Middle'
        SENIOR = 'SENIOR', 'Senior'
    
    class Status(models.TextChoices):
        ACTIVE = 'AC', 'Active'
        INACTIVE = 'INAC', 'Inactive'

    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    level = models.CharField(
        max_length=20,
        choices=Level.choices,
        default=Level.JUNIOR
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.INACTIVE
    )

    course = models.ManyToManyField(
        Course,
        related_name='mentors',
        blank=True
    )

    @property
    def fullname(self):
        return f"{self.firstname} {self.lastname}".strip()

    def __str__(self):
        return self.fullname

    class Meta:
        ordering = ['firstname', 'lastname']
        verbose_name = 'Mentor'
        verbose_name_plural = 'Mentors'



class Student(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'AC', 'Active'
        INACTIVE = 'INAC', 'Inactive'

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.INACTIVE
    )

    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    birth_date = models.DateField(blank=False, null=False) 
    created_at = models.DateTimeField(auto_now_add=True)
    
    phone = models.CharField(
        max_length=9,
        validators=[
            RegexValidator(
                regex=r'^[0-9]{9}$',  
                message="Telefon raqami aynan 9 ta raqamdan iborat bo'lishi kerak."
            )
        ],
        blank=True,
        null=False
    )
    
    @property
    def fullname(self):
        return f"{self.firstname} {self.lastname}".strip()

    def __str__(self):
        return self.fullname

    class Meta:
        ordering = ['firstname', 'lastname']
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    

class Group(models.Model):
    class ScheduleType(models.TextChoices):
        ODD = 'ODD', 'Odd'
        EVEN = 'EVEN', 'Even'
        EVERYDAY = 'Every', 'Everyday'

    title = models.CharField(max_length=50, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    schedule_type = models.CharField(
        max_length=10, 
        choices=ScheduleType.choices
    )

    def __str__(self):
        return f"{self.title}-{self.schedule_type}"

    class Meta:
        ordering = ['schedule_type']
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
     

