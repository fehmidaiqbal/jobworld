from rest_framework import serializers

from jobworld_djp_api.models import User_personal_info,state_info,city_info,area_info,qualif_info,coursetypes,courses,branches,skills,user_skill

class User_personal_info_Serializer(serializers.ModelSerializer):
     class Meta:
       model = User_personal_info
       
       fields = ('first_name','second_name','mobile_num','email_id','password','state_id','city_id','area_id')

class state_info_Serializer(serializers.ModelSerializer):
       class Meta:
        model = state_info
        fields = ('state_name','state_id')

class city_info_Serializer(serializers.ModelSerializer):
       class Meta:
        model = city_info
        fields = ('state_id','city_name','city_id')

class area_info_Serializer(serializers.ModelSerializer):
       class Meta:
        model = area_info
        fields = ('city_id','area_name','area_id')

class qualif_Serializer(serializers.ModelSerializer):
       class Meta:
        model = qualif_info
        fields = ('user_id','qualif_id','coursetype_id','course_id','branch_id','passout_year','highest_qualif','aggregate')

class coursetypes_Serializer(serializers.ModelSerializer):
       class Meta:
        model = coursetypes
        fields = ('coursetype_name','coursetype_id','coursetype_duration')

class courses_Serializer(serializers.ModelSerializer):
       class Meta:
        model = courses
        fields = ('coursetype_id','course_name','course_id')


class branches_Serializer(serializers.ModelSerializer):
       class Meta:
        model = branches
        fields = ('course_id','branch_name','branch_id',)

class skills_Serializer(serializers.ModelSerializer):    
        class Meta:
            model = skills
            fields = ('skill_name','skill_id')


class user_skill_Serializer(serializers.ModelSerializer):    
        class Meta:
            model = user_skill
            fields = ('user_id','skill_id','experience')
