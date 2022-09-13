from rest_framework import serializers
from .models import User , AttedanceWorkTime,ListProject,ProjectDescription


class RegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    
    class Meta:
        model = User
        fields = ('username','email', 'password',)
        
        
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)
    

class LoginSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('id','email', 'username', 'password', 'token')

        read_only_fields = ['token']
        
class AttedanceWorkTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttedanceWorkTime
        fields = ('name','date','time', 'type_absen','emp')
        
    
class ListProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListProject
        fields = ('id','name_project')
        
        
class ProjectDescriptionSerializer(serializers.ModelSerializer):
    # choice_project = serializers.ReadOnlyField(source='choice_project.name_project')
    class Meta:
        model = ProjectDescription
        fields = ('name','date','time_in','type_absen','emp','choice_project','lat','lon','detail_project','status')
    
class ProjectDescriptionSerializerView(serializers.ModelSerializer):
    choice_project = serializers.ReadOnlyField(source='choice_project.name_project')
    class Meta:
        model = ProjectDescription
        fields = ('name','date','time_in','type_absen','emp','choice_project','lat','lon','detail_project','status')