from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    Book_name = models.CharField(max_length=100)
    Book_id = models.CharField(max_length=20)
    Book_publisher = models.CharField(max_length=50)
    Issue_date = models.DateField()
    Due_date = models.DateField()
    Status = models.IntegerField(default=0)
    Issued_by = models.CharField(default="abc", max_length=20)

    def get_absolute_url(self):
        return reverse('book:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.Book_name

    def get_all_objects(self):
        return self.objects.all()


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Name = models.CharField(max_length=100)
    Roll_no = models.CharField(max_length=15, unique=True)
    Course = models.CharField(max_length=30)
    Department = models.CharField(max_length=100)
    Phone_no = models.CharField(max_length=10, null=False, blank=False, unique=True)
    Hostel_no = models.CharField(max_length=2)
    Room_no = models.CharField(max_length=5)
    Permanent_address = models.CharField(max_length=500)
    B1_id = models.CharField(max_length=20, default=0)
    B2_id = models.CharField(max_length=20, default=0)
    B3_id = models.CharField(max_length=20, default=0)
    fine = models.IntegerField(default=0)

    def __str__(self):
        return self.Course
