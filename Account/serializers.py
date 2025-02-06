from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from datetime import date
import re 
from tld import get_tld , exceptions







User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    email = serializers.CharField()
    username = serializers.CharField(min_length=3,max_length=20)
    password = serializers.CharField(write_only = True, min_length=8)
    birthday = serializers.DateField()
    phone_number = serializers.CharField(max_length =15, required=False , allow_blank=True)


    def validate_username(self, value):

        if User.objects.filter(username=value).exists():

            raise serializers.ValidationError('this username already exist.')
        
        if 'admin' in value.lower():
            raise serializers.ValidationError("username must not include 'admin'.")
        return value


    def validate_email(self,value):
        
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.fullmatch(regex , value):
            raise serializers.ValidationError("invalid email")
        
        domain = value.split('@')[-1]

        try :
            get_tld(domain , fix_protocol=True)
        except exceptions.TldDomainNotFound:
            raise serializers.ValidationError(" invalid domain")

        return value




    def validate_password(self, value):

        if not any(i.isdigit() for i in value):
            
            raise serializers.ValidationError('password must have at least one number.')

        if not any(i.isupper() for i in value):
    
            raise serializers.ValidationError('password must have at least one capital letter.')
        
        return value



    def validate_birthday(self,value):
        today = date.today()
        age = today.year - value.year - ((today.month , today.day) < (value.month , value.day)) 
        if age < 16:
            raise serializers.ValidationError('users must be at least 16 years old')
        return value
    

    def validate_phone_number(self,value):
        if value and  not re.fullmatch(r'^\+?[0-9]{10,15}$' , value) :
                raise serializers.ValidationError('phone number can only have numbers and must be between 10 and 15 digits.')
        return value


    class Meta:
        model = User
        fields = ("id","username","password","phone_number","birthday","bio","email","profile_image","create_at")
        extra_kwargs = {'password': {'write_only': True},'create_at': {'read_only': True}}

    def create(self,validated_data):
        try:
            validated_data['password'] = make_password(validated_data['password'] , salt=None, hasher="default")
            return super().create(validated_data)
        except:
            return f'somthing went wrong'
    
    
    def update(self, instance, validated_data):

        password = validated_data.get('password',None)

        if password:
            validated_data['password']= make_password(password)

        return super().update(instance, validated_data)