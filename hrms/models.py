from django.db import models
from django.contrib.auth.models import AbstractUser

import os
from django.utils.crypto import get_random_string

class LeaveType(models.Model):
    leave_id = models.AutoField(primary_key=True)
    leave_typename = models.CharField(max_length=100)

    def __str__(self):
        return self.leave_typename

class Leave_Entitlement(models.Model):
    ent_id = models.AutoField(primary_key=True)
    leave_typename = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    no_of_days = models.IntegerField()
    leave_period = models.CharField(max_length=200,blank=True, null=True)

    # def __str__(self):
    #     return self.ent_id

# =========================================
# Define a mapping of field names to upload paths
FIELD_UPLOAD_PATHS = {
    'educational_certificates': 'educational_certificates/',
    'appointment_letter': 'appointment_letter/',
    'passport_size_photo': 'passport_size_photo/',
    'pancard': 'pancards/',
    'aadharcard': 'aadharcards/',
}

def generate_filename(instance, filename):
    # Generate a random string to ensure unique file names
    random_string = get_random_string(length=10)

    # Get the field name based on the current file field
    for field_name, upload_path in FIELD_UPLOAD_PATHS.items():
        if hasattr(instance, field_name) and getattr(instance, field_name).name == filename:
            ext = filename.split('.')[-1]

             # Remove the file extension from the original filename
            filename_without_ext = os.path.splitext(filename)[0]
            
            new_filename = f"{instance.emp_id.id}_{filename_without_ext}{random_string}.{ext}"

            return os.path.join(upload_path, new_filename)


class CustomUser(AbstractUser):
    # prefix = models.CharField(max_length=10,blank=True)
    username = models.CharField(max_length=20, unique=True)
    # first_name = None
    # last_name = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    leave_balance1 = models.PositiveIntegerField(default=10)
    leave_balance2 = models.PositiveIntegerField(default=15)
    biits_id = models.CharField(max_length=20,blank=True, null=True)
    job_title = models.CharField(max_length=50,blank=True, null=True)
    department = models.CharField(max_length=50,blank=True, null=True)
    reporting_manager = models.CharField(max_length=50,blank=True, null=True)
    work_location = models.CharField(max_length=50,blank=True, null=True)
    # marital_status = models.CharField(max_length=50,blank=True, null=True)
    joining_date = models.DateField(null=True, blank=True)
    # aadhar_number = models.CharField(max_length=20,null=True, blank=True)
    # pancard_number = models.CharField(max_length=20,null=True, blank=True)
    gender = models.CharField(max_length=20,null=True, blank=True)
    form_id = models.IntegerField(default=0)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"] 

# ===================================================


# Define a mapping of field names to upload paths
FIELD_UPLOAD_PATHS = {
    'educational_certificates': 'educational_certificates/',
    'appointment_letter': 'appointment_letter/',
    'passport_size_photo': 'passport_size_photo/',
    'pancard': 'pancards/',
    'aadharcard': 'aadharcards/',
}

def generate_filename1(instance, filename):
    # Generate a random string to ensure unique file names
    random_string = get_random_string(length=10)

    # Get the field name based on the current file field
    for field_name, upload_path in FIELD_UPLOAD_PATHS.items():
        if hasattr(instance, field_name) and getattr(instance, field_name).name == filename:
            ext = filename.split('.')[-1]

             # Remove the file extension from the original filename
            filename_without_ext = os.path.splitext(filename)[0]
            
            new_filename = f"{instance.emp_id.id}_{filename_without_ext}{random_string}.{ext}"

            return os.path.join(upload_path, new_filename)

class Employee_documents(models.Model):
    emp_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    educational_certificates = models.FileField(upload_to=generate_filename1)
    appointment_letter = models.FileField(upload_to=generate_filename1)
    passport_size_photo = models.FileField(upload_to=generate_filename1)
    pancard = models.FileField(upload_to=generate_filename1)
    aadharcard = models.FileField(upload_to=generate_filename1)

# ===============================================
   

class Emp_leaves(models.Model):
    emp_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='emp_leaves')
    application_date = models.DateField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    leave_typename = models.ForeignKey(LeaveType, on_delete=models.PROTECT)
    # leave_balance = models.IntegerField(null=True, blank=True)
    no_of_days = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=50,default='3')
    mg_conformation = models.CharField(max_length=50,default='3')
    mg_comments = models.CharField(max_length=500,default='Waiting for manager confirmation')
    hr_comments = models.CharField(max_length=500,null=True, blank=True)
    approved_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.emp_id.username
    
    
class Leave_Application(models.Model):
    emp_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    application_date = models.DateField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    comments = models.CharField(max_length=200)
    leave_typename = models.ForeignKey(LeaveType, on_delete=models.PROTECT)

    def __str__(self):
        return self.emp_id.username
    
# ================ (20-09-2023) =================
class Emp_Onboardingform(models.Model):
    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50,blank=True,null=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=50)
    age = models.IntegerField()
    phone = models.CharField(max_length=10,unique=True)
    email = models.EmailField(unique=True)
    aadhar_number = models.CharField(max_length=50,unique=True)
    pan_number = models.CharField(max_length=50,unique=True)
    passport_number = models.CharField(max_length=50,null=True, blank=True)
    blood_group = models.CharField(max_length=10)
    marital_status = models.CharField(max_length=10)
    permenent_address = models.CharField(max_length=200)
    emergency_contact = models.CharField(max_length=10)
    father_name = models.CharField(max_length=50)
    mother_name = models.CharField(max_length=50)
    spouse_name = models.CharField(max_length=50)
    qualification = models.CharField(max_length=50)
    # educational_documents = models.FileField()
    name_of_the_bank = models.CharField(max_length=50)
    account_holder_name = models.CharField(max_length=50)
    account_number = models.CharField(max_length=50)
    ifsc_code = models.CharField(max_length=30)
    branch = models.CharField(max_length=30)
    year_of_experience = models.CharField(max_length=30)
    reason_for_resignation = models.CharField(max_length=200,null=True, blank=True)
    uan_number = models.CharField(max_length=20)
    # photo = models.FileField()
    hr_verification = models.CharField(max_length=50,default ='Pending')

    

    

    





