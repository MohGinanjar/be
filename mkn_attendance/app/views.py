from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import ProjectDescriptionSerializerView, RegisterSerializer, LoginSerializer,ProjectDescriptionSerializer, ListProjectSerializer
from rest_framework import response,status,generics
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import User , AttedanceWorkTime, AttedanceTimeView, ListProject, ProjectDescription
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.


class RegisterAPIView(GenericAPIView):
    authentication_classes = []
    serializer_class=RegisterSerializer
    
    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class LoginAPIView(GenericAPIView):
    authentication_classes = []

    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        user = authenticate(username=username, password=password)

        if user:
            serializer = self.serializer_class(user)

            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response({'message': "Invalid credentials, try again"}, status=status.HTTP_401_UNAUTHORIZED)




class ProjectListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = ListProject.objects.all()
    serializer_class = ListProjectSerializer
    filter_fields = (
        'id',
    )



class ListProjectUserView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = ProjectDescription.objects.all()
    serializer_class = ProjectDescriptionSerializerView
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['emp']
    


@csrf_exempt
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def clockin(request):
    try:
        name = request.data['name']
        date = request.data['date']
        time = request.data['time']
        type_absen= request.data['type_absen']
        choice_project = request.data['choice_project']
        lat = request.data['lat']
        lon = request.data['lon']
        detail_project = request.data['detail_project']
        status_respon= request.data['status']
        data_from_mobile = {
            'name':name,
            'date':date,
            'time_in':time,
            'type_absen':type_absen,
            'emp':request.user.id,
            'choice_project':choice_project,
            'lat':lat,
            'lon':lon,
            'detail_project':detail_project,
            'status':status_respon    
        }
        serializer = ProjectDescriptionSerializer(data=data_from_mobile)
        user = User.objects.get(id=request.user.id)
        if type_absen == 'CLOCK_IN':
            print('CLOCK_IN')
            if serializer.is_valid():
                serializer.save()
                return response.Response(data_from_mobile, status=status.HTTP_201_CREATED)
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif type_absen == 'CLOCK_OUT':
            print('CLOCK_OUT')
            attedance_view = ProjectDescription.objects.filter(name=name,date=date,type_absen='CLOCK_IN',emp=user,status='0').exists()
            if attedance_view :
                print('ada')
                ProjectDescription.objects.filter(name=name,date=date,type_absen='CLOCK_IN', emp=user, status='0').update(time_out=time, status=status_respon,type_absen=type_absen)
                return response.Response(data_from_mobile, status=status.HTTP_201_CREATED)
            else:
                print('tidak ada')
                return response.Response({"message": "Belum clock in" ,"value":3})
        else:
            return response.Response({'message':'not request on system' ,"value":5})
    except Exception as e:
        return response.Response(e, status=status.HTTP_400_BAD_REQUEST)




# example post
# {
#     "name":"Mohamad Ginanjar",
#     "date":"12-09-2022",
#     "time":"01:05",
#     "type_absen":"CLOCK_IN"
#     "user": 2
# }

# example post
# {
#     "name":"Mohamad Ginanjar",
#     "date":"12-09-2022",
#     "time":"01:05",
#     "type_absen":"CLOCK_OUT"
#     "user": 2
# }