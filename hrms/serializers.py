from rest_framework import serializers
from .models import *

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class LogoutSerializer(serializers.Serializer):
    pass
# -------------------------------------------------

class customuserserializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['id','username', 'email', 'password', 'phone','leave_balance1','leave_balance2','first_name','last_name','biits_id','department','job_title','reporting_manager','work_location','joining_date','gender','form_id']
        # fields="__all__"

class leavetypeserializer(serializers.ModelSerializer):
    class Meta:
        model=LeaveType
        fields="__all__"


class leave_applicationserializer(serializers.ModelSerializer):
    class Meta:
        model=Leave_Application
        fields="__all__"

class applyemp_leaveserializer(serializers.ModelSerializer):
    class Meta:
        model=Emp_leaves
        fields="__all__"

class emp_leaveserializer(serializers.ModelSerializer):
    start_date = serializers.CharField(required=False,allow_blank=True)
    end_date = serializers.CharField(required=False,allow_blank=True)
    leave_typename = serializers.CharField(required=False,allow_blank=True)
    status = serializers.CharField(required=False,allow_blank=True)
    
    class Meta:
        model=Emp_leaves
        fields="__all__"

class emp_leave_entitlementserializer(serializers.ModelSerializer):
    class Meta:
        model=Leave_Entitlement
        fields="__all__"

class Employee_documentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee_documents
        fields = '__all__'

class Employee_OnboardingformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emp_Onboardingform
        fields = '__all__'


class CustomUserWithDocumentsSerializer(serializers.ModelSerializer):
    documents = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields=['id','username', 'email', 'phone','leave_balance1','leave_balance2','documents']

    def get_documents(self, obj):
        documents = Employee_documents.objects.filter(emp_id=obj)
        return Employee_documentSerializer(documents, many=True).data

