from datetime import datetime
from django.db import models
from rest_framework import serializers

class YesNoBooleanField(models.BooleanField):
    def to_python(self, value):
        if isinstance(value, str):
            value= value.lower()
            if value in ('yes', 'y', 'true'):
                return True
            elif value in ('no', 'n', 'false'):
                return False
        return super().to_python(value)
    
    def get_prep_value(self, value):
        if value is None:
            return None
        return 'Yes' if value else 'No'
        


class CustomDateFormatField(serializers.DateField):
    def to_internal_value(self, value):
        try:
            # parse the date string using the desired format
            dt = datetime.strptime(value, '%m/%d/%Y').date()
            return dt
        except ValueError:
            # raise a validation error if the date string is invalid
            raise serializers.ValidationError('Invalid date format. Use MM/DD/YYYY.')

    def to_representation(self, value):
        # format the date string using the desired format
        return value.strftime('%d/%m/%Y')

# class MyDateField(models.DateField):
#     def __init__(self, format=None, *args, **kwargs):
#         self.format = format or '%m/%d/%Y'
#         super().__init__(*args, **kwargs)

#     def from_db_value(self, value, expression, connection):
#         print('*'*50)
#         print('value inside of from_db_value', value)
#         if value is None:
#             return value
#         elif isinstance(value, str):
#             return datetime.strptime(value, self.format).date()
#         else:
#             return value
        
#     def to_python(self, value):
#         print('$'*50)
#         print('inside of to_python', value)
#         if isinstance(value, str):
#             return datetime.strptime(value, self.format).date()
#         return super().to_python(value)
        
#     def get_prep_value(self, value):
#         print('*'*50, value)
#         if value is None:
#             return value
#         elif isinstance(value, datetime):
#             return value.date().strftime(self.format)
#         elif isinstance(value, date):
#             return value.strftime(self.format)
#         else:
#             raise ValueError('Invalid date value')

        
