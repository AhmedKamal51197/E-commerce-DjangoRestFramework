from rest_framework import  serializers
from django.contrib.auth.models import User
class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ('first_name','last_name','email','password')
        #validation data for signup
        extra_kwargs = {
            'username':{'required':True,'allow_blank':False},
            'first_name':{'required':True,'allow_blank':False},
            'last_name':{'required':True,'allow_blank':False},
            'email':{'required':True,'allow_blank':False},
            'password':{'required':True,'allow_blank':False,'min_length':8}
        }

#user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ('username','first_name','last_name','email','password')
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def update(self,instance,validated_data):
        password = validated_data.pop('password',None)
        instance = super().update(instance,validated_data)
        if password:
            instance.set_password(password)
            instance.save()
            print(instance.password)
        return instance

