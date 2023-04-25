from django.db import models
from .custom_field import YesNoBooleanField

#Province
class Province(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name


#District
class District(models.Model):
    name = models.CharField(max_length=30)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


#Municipality
class Municipality(models.Model):
    name = models.CharField(max_length=30)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


#Projects
class Project(models.Model):
    
    # STATUS_CHOICES = (
    #     ('On-Going', 'On-Going'),
    #     ('Completed', 'Completed')
    # )
    # TYPES_OF_ASSISTANCE = (
    #     ('TA', 'TA'),
    #     ('GRANT', 'GRANT'),
    #     ('GRANT, LOAN', 'GRANT, LOAN'),
    #     ('GRANT, TA', 'GRANT, TA')
    # )
    BUDGET_TYPE = (
        ('Off Budget', 'Off Budget'),
        ('On Budget', 'On Budget')
    )
    # IS_HUMANITARIAN = (
    #     (True, 'Yes'),
    #     (False, 'No')
    # )

    title = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=30, blank=True, null=True)
    donor = models.CharField(max_length=255, blank=True, null=True)
    executing_agency = models.CharField(max_length=255, blank=True, null=True)
    implementing_partner = models.TextField( blank=True, null=True)
    counterpart_ministry  = models.CharField(max_length=255, blank=True, null=True)
    type_of_assistance = models.CharField(max_length=50, blank=True, null=True)
    budget_type = models.CharField(max_length=15, choices=BUDGET_TYPE, default='Off Budget')
    is_humanitarian = YesNoBooleanField()
    sector = models.CharField(max_length=200)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE)
    commitments = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    agreement_date = models.DateField(null=True, blank=True)
    disbursement = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    disbursement_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title








