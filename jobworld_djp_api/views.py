from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from jobworld_djp_api.models import User_personal_info,state_info,city_info,area_info,qualif_info,coursetypes,courses,branches,skills,user_skill
from jobworld_djp_api.Serializer import User_personal_info_Serializer,state_info_Serializer,city_info_Serializer,area_info_Serializer,qualif_info_Serializer,coursetypes_Serializer,courses_Serializer,branches_Serializer,skills_Serializer,user_skill_Serializer

from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
import datetime

# temp

@api_view(['POST'])
def register_user():pass

@api_view(['POST'])
def login_user(request):
    requestData = request.data
    userName = requestData.get("email_id")
    password = requestData.get("password")
    ## add your validations if all are met return userId in response 
    return JsonResponse(status = 200,data = {"status":1,"userID":4343})


def getError(errorMsg):
  return {"error":errorMsg}

@api_view(['POST'])
def create__personal_info(request):
    data = request.data 

    FirstName = data['first_name']
    if len(FirstName) == 0:
        return JsonResponse(getError("First Name is missing"))

    SecondName = data['second_name']
    if len(SecondName) == 0:
        return JsonResponse(getError("Second Name is missing"))

    MobileNo = data['mobile_num']
    if len(MobileNo) != 10:
        return JsonResponse(getError("Mobile No is invalid"))

    UserIdenttity = data['email_id']
    if len(UserIdenttity) == 0:
        return JsonResponse(getError("email is missing"))

    Password = data['password']
    if len(Password) == 0:
        return JsonResponse(getError("Password is missing"))

    State = data['state_id']
    if len(State) == 0:
        return JsonResponse(getError("State Name is missing"))
    
    City = data['city_id']
    if len(City) == 0:
        return JsonResponse(getError("City Name is missing"))
    
    Area = data['area_id']
    if len(Area) == 0:
        return JsonResponse(getError("Area Name is missing"))
    
    Obj1 = User_personal_info(first_name = FirstName,second_name = SecondName,mobile_num = MobileNo, email_id = UserIdenttity, password = Password,state_id = State,city_id = City,area_id = Area)
    Obj1.save()
    return JsonResponse(status = 201,data={"status":1,"user_id":Obj1.user_id})

    