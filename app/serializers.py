from rest_framework import serializers

from .models import Province, District, Municipality, Project
from .custom_field import CustomDateFormatField


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'

    def create(self, validated_data):
        province, _ = Province.objects.get_or_create(**validated_data)
        return province
    
class DistrictSerializer(serializers.ModelSerializer):
    province = ProvinceSerializer()

    class Meta:
        model = District
        fields = ('id', 'name', 'province')

    def create(self, validated_data):
        province_data = validated_data.pop('province')
        p_serializer = ProvinceSerializer(data=province_data)
        p_serializer.is_valid()
        province = p_serializer.save()
        district, _ = District.objects.get_or_create(province=province, **validated_data)
        return district 
    
class MunicipalitySerializer(serializers.ModelSerializer):
    district = DistrictSerializer()

    class Meta:
        model = Municipality
        fields = '__all__'

    def create(self, validated_data):
        district_data = validated_data.pop('district')
        d_serializer = DistrictSerializer(data=district_data)
        d_serializer.is_valid(raise_exception=True)
        district = d_serializer.save()
        municipality, _ = Municipality.objects.get_or_create(district=district, **validated_data)
        return municipality


class ProjectSerializer(serializers.ModelSerializer):
    municipality = MunicipalitySerializer()
    agreement_date = CustomDateFormatField(allow_null=True, required=False)
    disbursement_date = CustomDateFormatField(allow_null=True, required=False)

    class Meta:
        model = Project
        fields = '__all__'

    def create(self, validated_data):
        municipality_data = validated_data.pop('municipality')
        m_serializer = MunicipalitySerializer(data=municipality_data)
        m_serializer.is_valid(raise_exception=True)
        municipality = m_serializer.save()
        
        project, _ = Project.objects.get_or_create(municipality=municipality, **validated_data)
        return project
    

class ProjectSummarySerializer(serializers.Serializer):
    project_count= serializers.IntegerField()
    total_budget = serializers.FloatField()
    sector = serializers.ListField(
        child=serializers.DictField(
        allow_empty=True
        ), allow_empty=True
    )


























# class CommitmentSerializer(serializers.ModelSerializer):
#     # project = ProjectSerializer()
#     class Meta:
#         model = Commitment
#         # fields = '__all__'
#         fields = ('id', 'value', 'agreement_date')

#     def to_internal_value(self, data):
#         data.pop('project', None)  # Remove 'project' field from validated data
#         return super().to_internal_value(data)

#     def create(self, validated_data):
#         print('*'*50)
#         print(validated_data)
#         return Commitment.objects.create(**validated_data)


# class DisbursementSerializer(serializers.ModelSerializer):
#     # project = ProjectSerializer()

#     class Meta:
#         model = Disbursement
#         # fields = '__all__'
#         fields = ('id', 'value', 'disbursement_date')

#     def to_internal_value(self, data):
#         data.pop('project', None)
#         return super().to_internal_value(data)
    
#     def create(self, validated_data):
#         print(validated_data)
#         print('----------------inside of disbursement')
#         return super().create(validated_data)


# class CustomSerializer(serializers.Serializer):
#     project = ProjectSerializer()
#     commitment = CommitmentSerializer(required=False)
#     disbursement = DisbursementSerializer(required=False)

#     def create(self, validated_data):
#         print('@'*59)
#         print(validated_data)
#         project_data = validated_data.pop('project')
#         commitment_data = validated_data.pop('commitment')
#         disbursement_data = validated_data.pop('disbursement')

#         # Create Project object
#         project_serializer = ProjectSerializer(data=project_data)
#         project_serializer.is_valid(raise_exception=True)
#         project_obj = project_serializer.save()
        

#          #Create the commitments objects
#         commitment_data['project'] = project_obj.id
#         commitment_serializer = CommitmentSerializer(data=commitment_data)
#         commitment_serializer.is_valid(raise_exception=True)
#         commitment_obj = commitment_serializer.save()


#         # print(commitment_obj)
#         disbursement_data['project'] = project_obj.id
#         disbursement_serializer = DisbursementSerializer(data=disbursement_data)
#         disbursement_serializer.is_valid(raise_exception=True)
#         disbursement_obj = disbursement_serializer.save()


   

