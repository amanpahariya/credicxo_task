from rest_framework import serializers
from .models import User




class CustomTeacherSerializer(serializers.ModelSerializer):
    '''
    this serializers is for teacher
    below fields are required when user is registering
    '''
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name','last_name','password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data,is_teacher=True)
        if password is not None:
            instance.set_password(password)
            instance
        instance.save()
        return instance

class CustomStudentSerializer(serializers.ModelSerializer):
    
    '''
    this serializers is for student
    below fields are required when user is registering
    '''
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name','last_name','password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data,is_student=True)
        if password is not None:
            instance.set_password(password)
            instance
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    '''
    user details
    '''
    class Meta:
        model=User
        fields = ('email', 'first_name','last_name')


