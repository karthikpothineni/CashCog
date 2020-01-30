from __future__ import unicode_literals

from django.db import models

EXPENSE_APPROVAL_CHOICES = [
    ("NA", "NA"),
    ("Approved", "Approved"),
    ("Declined", "Declined"),
]

class Employee(models.Model):

    uuid = models.UUIDField(primary_key=True, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        app_label = 'cash_cog'
        db_table = 'employee'

    def __str__(self):
        return str(self.uuid)


class Expense(models.Model):

    uuid = models.UUIDField(primary_key=True, editable=False)
    description = models.TextField()
    created_at = models.DateTimeField('date joined')
    amount = models.IntegerField()
    currency = models.CharField(max_length=3)
    employee = models.ForeignKey(Employee, db_column='employee')
    is_approved = models.CharField(max_length=8, default='NA', choices=EXPENSE_APPROVAL_CHOICES)

    class Meta:
        app_label = 'cash_cog'
        db_table = 'expense'

    def __str__(self):
        return str(self.uuid)
