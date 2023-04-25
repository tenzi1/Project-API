import django_filters

from django.db.models import Count, Sum
from rest_framework.views import APIView
from rest_framework import generics,status
from rest_framework.response import Response

from .models import  Project
from .serializers import ProjectSerializer


# Project Filter 
class ProjectFilter(django_filters.FilterSet):
    district = django_filters.CharFilter(field_name='municipality__district__name', lookup_expr='icontains')
    province = django_filters.CharFilter(field_name='municipality__district__province__name', lookup_expr='icontains')

    class Meta:
        model = Project
        fields = ('sector', 'counterpart_ministry', 'status', 'disbursement_date', 'agreement_date', 'district', 'province')


class CountProjectBudget(APIView):
    filterset_class = ProjectFilter

    def get(self, request):
        project_filter = self.filterset_class(request.GET, queryset=Project.objects.all())
        queryset = project_filter.qs

        summary_data = queryset.values('municipality__id', 'municipality__name').annotate(
            count=Count('id',),
            budget=Sum('commitments')
        )
        data = [{'id':row['municipality__id'],'name': row['municipality__name'], 'count': row['count'], 'budget':row['budget'] } for row in summary_data]
       
        return Response(data)
    

# a view for returning project summary
class ProjectSummary(APIView):
    filterset_class = ProjectFilter
    serializer_class = ProjectSerializer

    def get(self, request):
        project_filter = self.filterset_class(request.GET, queryset=Project.objects.all())
        queryset = project_filter.qs
        

        summary_data = {
                'project_count': queryset.count(),
                'total_budget' : queryset.aggregate(Sum('commitments'))['commitments__sum'] or 0,
                'sector': queryset.values('sector').annotate(
                    project_count=Count('id',),
                    budget=Sum('commitments')
                ).values('id', 'sector', 'project_count', 'budget')
        }
        return Response(summary_data)
    
        

#A View for Listing all Projects
class ProjectView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filterset_class = ProjectFilter


#view for uploading projects
class UploadProjectView(APIView):

    def post(self, request):
        serializer = ProjectSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

    

    # test  
        
#         data = [
#     {
#         'title': 'Project 1',
#         'status': 'On-Going',
#         'donor': 'Donor 1',
#         'executing_agency': 'Agency 1',
#         'implementing_partner': 'Partner 1',
#         'counterpart_ministry': 'Ministry 1',
#         'type_of_assistance': 'TA',
#         'budget_type': 'Off Budget',
#         'is_humanitarian': True,
#         'sector': 'Sector 1',
#         'commitments': 900000,
#         'agreement_date': '2/24/2023',
#         'disbursement': '985000',
#         'disbursement_date': None,
#         'municipality': {
#             'name': 'Municipality 1',
#             'district': {
#                 'name': 'District 1',
#                 'province': {
#                     'name': 'Province 1'
#                 }
#             }
#         }
#     },
#     {
#         'title': 'Project 2',
#         'status': 'Completed',
#         'donor': 'Donor 2',
#         'executing_agency': 'Agency 2',
#         'implementing_partner': 'Partner 2',
#         'counterpart_ministry': 'Ministry 1',
#         'type_of_assistance': 'TA',
#         'budget_type': 'Off Budget',
#         'is_humanitarian': True,
#         'sector': 'Sector 1',
#         'commitments': 900000,
#         'agreement_date': '2/24/2023',
#         'disbursement': '985000',
#         'disbursement_date': None,
#         'municipality': {
#             'name': 'Municipality 1',
#             'district': {
#                 'name': 'District 1',
#                 'province': {
#                     'name': 'Province 1'
#                 }
#             }
#         }
#     }
# ] 
    










# def upload_projects(request):
#     if request.method == 'POST':
#         #Authenticating GS API with bot account
#         gc = gspread.service_account()

#         # Opening worksheet
#         worksheet = gc.open('sample sheet').worksheet('Sheet1')

#         #Retrieve data
#         rows = worksheet.get_all_records()
#         headers = worksheet.row_values(1)

        # Iterate through rows and create project objects
    #     for row in rows:
    #        province, created =  Province.objects.get_or_create(name=row['Province'])
    #        district, created = District.objects.get_or_create(name=row['District'], province=province)
    #        municipality, created = Municipality.objects.get_or_create(name=row['Municipality'], district=district)

    #        project, created = Project.objects.get_or_create(
    #            title=row['Project Title'],
    #            defaults={
    #                 'status': row['Project Status'],
    #                 'donor': row['Donor'],
    #                 'executing_agency':row['Executing Agency'],
    #                 'implementing_partner': row['Implementing Partner'],
    #                 'counterpart_ministry': row['Counterpart Ministry'],
    #                 'type_of_assistance':row['Type of Assistance'],
    #                 'budget_type': row['Budget Type'],
    #                 'is_humanitarian': row['Humanitarian'],
    #                 'sector': row['Sector'],
    #                 'municipality': municipality
    #            })
    #        commitment = Commitments.objects.create(
    #             value=row['Commitments'],
    #             agreement_date=row['Agreement Date'],
    #             project=project
    #        )
        
    #        disbursement = Disbursement.objects.create(
    #            value=row['Disbursement'],
    #            disbursement_date=row['Disbursement Date'],
    #            project=project
    #        )
    #     return JsonResponse({'success':True})
    # else:
    #     return JsonResponse({'error': 'Invalid request method'})
    


# def access_gs(request):
#     gc = gspread.service_account()
#     sh = gc.open("sample sheet").worksheet('Sheet1')
#     # A1 = sh.sheet1.get('A1')
#     # print(A1)
#     rows = sh.get_all_records()
#     header_row = sh.row_values(1)
#     return HttpResponse(f'{header_row}')


# def worksheet(request):
#     gc = gspread.service_account()
#     sh = gc.open('sample sheet')
#     worksheet_list = sh.worksheets()
#     return HttpResponse(f'{worksheet_list}')

# def create_worksheet(request):
#     gc = gspread.service_account()
#     sh = gc.open('sample sheet')
#     sh.add_worksheet(title='A worksheet',rows=100, cols=3)
#     return HttpResponse('Created successfully')

# def delete_worksheet(request):
#     gc = gspread.service_account()
#     sh = gc.open('sample sheet')
#     worksheet = sh.worksheet("A worksheet")
#     sh.del_worksheet(worksheet)
#     return HttpResponse('Deleted Successfully')
