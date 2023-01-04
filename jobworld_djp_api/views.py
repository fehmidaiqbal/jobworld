from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from jobworld_djp_api.models import User_personal_info,state_info,city_info,area_info,qualif_info,coursetypes,courses,branches,skills,user_skill
from jobworld_djp_api.Serializer import User_personal_info_Serializer,state_info_Serializer,city_info_Serializer,area_info_Serializer,qualif_info_Serializer,coursetypes_Serializer,courses_Serializer,branches_Serializer,skills_Serializer,user_skill_Serializer

from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view



@api_view(['POST'])
def register_user(request):
        input = request.data
        serializer = User_personal_info_Serializer(data=input)
        valid = serializer.is_valid()
        if valid == False:
            return JsonResponse({"error":"invalid data"})

        userName = input.get('email_id')
        Password = input.get('password')

        # check user name in users table
        userExist = User_personal_info.objects.filter(email_id__exact=userName).exists()
        if(userExist == True):
            response = {"error":"user found, please login"}
            return JsonResponse(response,safe=False) 
        #if no user    
        serializer.save()
        return JsonResponse(serializer.data,status = 201)    

@api_view(['POST'])
def login_user(request):
    requestData = request.data
    userName = requestData.get("email_id")
    password = requestData.get("password")
    
    # validate request format
    if len(userName) == 0 or len(password) == 0 :
        return JsonResponse({"error":"invalid input"})

    if len(password) != 8:
        return JsonResponse({"error":"password is  invalid"})

    #check user_id existance in the table   

    isExist = User_personal_info.objects.filter(email_id__exact = userName).exists()
    
    if isExist == False:
        return JsonResponse({"error":"user not found"})

    dbRow = User_personal_info.objects.filter(email_id__exact = userName).values()
    dbData = dbRow.first()
    dbPassword = dbData["password"]
    
     # validate user name and password with DB data 
    if dbPassword == password :
        response = {}
        response["status"] = 1 
        response["user_id"] = dbData["user_id"]
        return JsonResponse(data = response,status = 200)    
   
    # if not throw "error:invalid user//re-enter correct password"
    return JsonResponse({"error":"password not matched"})

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


@api_view(['GET'])  
def get_personal_info(request):
    input = request.queryparams
    req_user_id = input['user_id']
    
    queryList = User_personal_info.objects.filter(user_id__exact = req_user_id).values()
    responseList = []
    for item in queryList:
        responseList.append(item)
    
    return JsonResponse(responseList,status=200,safe=False)

@api_view(['GET'])  
def get_state_info(request):
   # input = request.queryparams
   #req_ = input['']
   # queryList = state_info.objects.all
   #return JsonResponse(responseStateList,status=200)
   pass

@api_view(['GET'])  
def get_city_info(request):
    input = request.queryparams
    req_state_id = input['state_id']
   
    queryList = city_info.objects.filter(state_id__exact = req_state_id).values()
    responseCityList = []
    for item in queryList:
        responseCityList.append(item)
   
    return JsonResponse(responseCityList,status=200)
    
@api_view(['GET'])  
def get_area_info(request):
    input = request.queryparams
    req_city_id = input['city_id']
    
    queryList = area_info.objects.filter(city_id__exact = req_city_id).values()
    responseAreaList = []
    for item in queryList:
        responseAreaList.append(item)
    
    return JsonResponse(responseAreaList,status=200)


@api_view(['POST','PUT'])  
def CUqualif_info(request):
    input = request.data 
    userId = input['user_id']
    if len(userId) == 0:
        return JsonResponse(getError("userId missing in request"))
    
    userExist = User_personal_info.objects.filter(user_id__exact = userId).exists()
    if userExist == False:
        return JsonResponse(getError("user not found"))

    CourseTypeId = input['coursetype_id']
    if len(CourseTypeId) == 0:
        return JsonResponse(getError("CourseTypeId missing in request"))

    CourseId = input['course_id']
    if len(CourseId) == 0:
        return JsonResponse(getError("CourseId missing in request"))

    BranchId = input['branch_id']
    if len(BranchId) == 0:
        return JsonResponse(getError("BranchId missing in request"))
    
    Year = input['passout_year']
    if len(Year) == 0:
        return JsonResponse(getError("Year missing in request"))

    Qualif = input['highest_qualif']
    

    Aggre = input['aggregate']
    if Aggre != 2:
        return JsonResponse(getError("invalid Aggregate"))
    if Aggre < 100:
        return JsonResponse(getError("invalid Aggregate"))

    if request.method == 'POST':
        Obj2 = qualif_info(user_id = userId, coursetype_id = CourseTypeId ,course_id = CourseId,branch_id = BranchId,passout_year = Year,highest_qualif = Qualif,aggregate = Aggre)
        Obj2.save()
        response = {"qualification_id":Obj2.qualif_id}
        return JsonResponse(status = 201,data = response)
        
    elif request.method == 'PUT':
        qualificationId = input.get('quailfication_id')
        if len(qualificationId) == 0 :
            return  JsonResponse(getError("qualificationId is missing"))
        Obj3 = qualif_info(qualif_id = qualificationId,user_id = userId, coursetype_id = CourseTypeId ,course_id = CourseId,branch_id = BranchId,passout_year = Year,highest_qualif = Qualif,aggregate = Aggre)
        Obj3.save()
        response = {"qualification_id":Obj3.qualif_id}
        return JsonResponse(status = 201,data = response)
    

@api_view(['GET'])  
def get_qualif_info(request):
    input = request.queryparams
    req_user_id = input['user_id']
    
    queryList = qualif_info.objects.filter(user_id__exact = req_user_id).values()
    responseQualifDetail = []
    for item in queryList:
        responseQualifDetail.append(item)
    
    return JsonResponse(responseQualifDetail,status=200)


@api_view(['GET'])  
def get_coursetypes(request):
    input = request.queryparams
    req_= input['']
    
    queryList = qualif_info.objects.filter(__exact = req_).values()
    responseCourseTypeList = []
    for item in queryList:
        responseCourseTypeList.append(item)
    
    return JsonResponse(data=responseCourseTypeList,status =200)


@api_view(['GET'])  
def get_courses(request):
    input = request.queryparams
    req_coursetype_id = input['coursetype_id']
    
    queryList = courses.objects.filter(coursetype_id__exact = req_coursetype_id).values()
    responseCoursesList = []
    for item in queryList:
        responseCoursesList.append(item)
     
    return JsonResponse(data = responseCoursesList,status =200)
    

@api_view(['GET'])  
def get_branches(request):
    input = request.queryparams
    req_course_id = input['course_id']
    
    queryList = branches.objects.filter(course_id__exact = req_course_id).values()
    responseBranchesList = []
    for item in queryList:
        responseBranchesList.append(item)
     
    return JsonResponse(data = responseBranchesList,status =200)



@api_view(['POST','PUT'])  
def CUskill_info(request):
    input =  request.data
    skillName = input['skill_name']
    if len(skillName) == 0:
        return JsonResponse(getError("Skill missing in request"))
   
    if request.method == 'POST':
        Obj4 = skills(skill_name = skillName)
        Obj4.save()
        response = {"Skill_id":Obj4.skill_id}
        return JsonResponse(status = 201,data = response)

    elif request.method == 'PUT':
        Skill_id = input['skill_id']

        if len(Skill_id) == 0:
            return JsonResponse(getError("Skill_id is missing"))
        
        Obj4 = skills(skill_name = skillName,skill_id = Skill_id)
        Obj4.save()
        response = {"Skill_id":Obj4.skill_id}

        return JsonResponse(status = 201,data = response)

                        

@api_view(['GET'])  
def get_userskill(request):
    input = request.queryparams
    req_user_id = input['user_id']
    
    queryList = user_skill.objects.filter(user_id__exact = req_user_id).values()
    responseUserSkillsList = []
    for item in queryList:
        responseUserSkillsList.append(item)
     
    return JsonResponse(data = responseUserSkillsList,status =200)
    



