from django.db import models

class User_personal_info(models.Model):
   first_name = models.CharField(max_length=20)
   second_name = models.CharField(max_length=20)
   mobile_num= models.CharField(max_length=10,db_index=True,unique=True)
   email_id = models.CharField(max_length=50,blank=False,db_index=True,unique=True)
   password= models.CharField(max_length=8,blank = False)
   state_id= models.IntegerField(max_length=2)
   city_id= models.IntegerField(max_length=2)
   area_id= models.IntegerField(max_length=2)
   user_id= models.AutoField(primary_key=True,db_index=True)

class state_info(models.Model):
    state_name = models.CharField(max_length=50)
    state_id = models.AutoField(primary_key=True)

class city_info(models.Model):
    state_id = models.IntegerField(max_length=2)
    city_name = models.CharField(max_length=50)
    city_id = models.AutoField(primary_key=True)

class area_info(models.Model):
    city_id = models.IntegerField(max_length=2)
    area_name = models.CharField(max_length=50)
    area_id = models.AutoField(primary_key=True)

class qualif_info(models.Model):
    user_id = models.IntegerField(max_length=100)
    qualif_id = models.AutoField(primary_key=True)
    coursetype_id = models.IntegerField(max_length=2)
    course_id = models.IntegerField(max_length=2)
    branch_id = models.IntegerField(max_length=2)
    passout_year = models.IntegerField(max_length=4)
    highest_qualif = models.BooleanField()
    aggregate = models.IntegerField(max_length=2)

class coursetypes(models.Model):
    coursetype_name = models.CharField(max_length=100)
    coursetype_id = models.AutoField(primary_key=True)
    coursetype_duration = models.SmallIntegerField(max_length=2)

class courses(models.Model):
    coursetype_id = models.IntegerField(max_length=2)
    course_name = models.CharField(max_length=100)
    course_id = models.AutoField(primary_key=True)
    
class branches(models.Model):
   course_id = models.IntegerField(max_length=2)
   branch_name = models.CharField(max_length=100)
   branch_id = models.AutoField(primary_key=True)

class skills(models.Model):
    skill_name = models.CharField(max_length=100)
    skill_id = models.AutoField(primary_key=True)

class user_skill(models.Model):
    user_id = models.IntegerField(max_length=10)
    skill_id = models.IntegerField(max_length=10)
    experience = models.SmallIntegerField(max_length=2) 
