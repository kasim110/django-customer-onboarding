from django.db import models
from django.contrib.auth.models import User

class CountryModel(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    class  Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Country'
        
# Extend the User model to include a country field
User.add_to_class('country', models.ForeignKey(CountryModel, null=True, on_delete=models.SET_NULL))

class DocumentSetModel(models.Model):
    name = models.CharField(max_length=255)
    countries = models.ManyToManyField(CountryModel)
    has_backside = models.BooleanField(default=False)
    ocr_labels = models.TextField()

    def __str__(self):
        return self.name
    class  Meta:
        verbose_name = 'Document Set'
        verbose_name_plural = 'Document Set'

class CustomerModel(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    surname = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    nationality = models.ForeignKey(CountryModel, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.firstname} {self.surname}'
    
    class  Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customer'

class CustomerDocumentModel(models.Model):
    customer = models.ForeignKey(CustomerModel, on_delete=models.CASCADE)
    attached_file = models.FileField(upload_to='documents/')
    extracted_json = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Document for {self.customer}'
    
    class  Meta:
        verbose_name = 'Customer Document'
        verbose_name_plural = 'Customer Document'