from django.http import JsonResponse

from jobworld_djp_api.models import User_personal_info, coursetypes,state_info,city_info,area_info,qualif_info,courses,branches,skills,user_skill
from jobworld_djp_api.Serializer import User_personal_info_Serializer

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

@api_view(['POST','PUT'])
def create__personal_info(request):
    data = request.data 
    FirstName = data.get('first_name','')
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

    if request.method == 'POST':
        Obj1 = User_personal_info(first_name = FirstName,second_name = SecondName,mobile_num = MobileNo, email_id = UserIdenttity, password = Password,state_id = State,city_id = City,area_id = Area)
        Obj1.save()
        return JsonResponse(status = 201,data={"status":1,"UserId":Obj1.user_id})
    
    elif request.method == 'PUT':
        UserId = data.get('user_id',0)
        if UserId == 0 :
            return  JsonResponse(getError("UserId is missing"))

        Obj2 = User_personal_info(user_id= UserId,first_name = FirstName,second_name = SecondName,mobile_num = MobileNo, email_id = UserIdenttity, password = Password,state_id = State,city_id = City,area_id = Area)
        Obj2.save()
        return JsonResponse(status = 201,data={"firstName":Obj2.first_name},safe=False)


@api_view(['GET'])  
def get_personal_info(request):
    input = request.query_params
    UserId = input['user_id']
    queryList = User_personal_info.objects.filter(user_id__exact = UserId).values()
    PList = []
    for item in queryList:
        temp = {"First Name":item.first_name,"Second Name":item.second_name,"Mobile No":item.mobile_num,"User Identtity":item.email_id,"Password":item.password,"State":item.state_id,"City":item.city_id,"Area":item.area_id}
        PList.append(temp)
    return JsonResponse(data = PList,status=201,safe=False)

    
@api_view(['POST','GET'])  
def get_state_info(request):
    if request.method == 'POST':
        State = request.data["state_name"]
        obj = state_info(state_name=State)
        obj.save()
        return JsonResponse(data={"State_Id":obj.state_id},status = 201,safe=False)
    
    queryList = state_info.objects.all()
    aList = []
    for item in queryList:
        temp = {"State_Id":item.state_id,"State":item.state_name}
        aList.append(temp)
    return JsonResponse(data = aList,status=200,safe=False)

   

@api_view(['POST','GET'])  
def get_city_info(request):
    if request.method == 'POST':
        City = request.data["city_name"]
        StateId = request.data["state_id"]
        obj = city_info(state_id = StateId ,city_name = City)
        obj.save()
        return JsonResponse(data={"City_Id":obj.city_id},status = 201,safe=False)

    input = request.query_params
    StateId = input['state_id']
    
    if len(StateId) != 0 :
        queryList = city_info.objects.filter(state_id__exact = StateId).values()
        CList = []
        for item in queryList:
            CList.append(item)
            
        return JsonResponse(data =CList ,status=200,safe=False)

    queryList = city_info.objects.all()
    CList = []
    for item in queryList:
        temp = {"StateId":item.state_id,"CityId":item.city_id,"CityName":item.city_name}
        CList.append(temp)
    return JsonResponse(data=CList,status=200,safe=False)
    
@api_view(['POST','GET'])  
def get_area_info(request):
    data = request.data
    if request.method == 'POST':
        CityId = data.get("city_id",'')
        Area = data["area_name"]
        Obj = area_info(city_id = CityId,area_name = Area)
        Obj.save()
        return JsonResponse(data={"Area_Id":Obj.area_id},status = 201,safe=False)

  
    input = request.query_params
    CityId = input.get('city_id','')
    if len(CityId) != 0 :
        queryList = area_info.objects.filter(city_id__exact = CityId).values()
        AList = []
        for item in queryList:
            AList.append(item)
        return JsonResponse(data =AList ,status=200,safe=False)

    queryList = area_info.objects.all()
    AList = []
    for item in queryList:
        temp= {"City":item.city_id,"Area":item.area_id,"AreaName":item.area_name}
        AList.append(temp)
    return JsonResponse(data = AList ,status=200,safe=False)


@api_view(['POST','PUT'])  
def CUqualif_info(request):
    input = request.data 
    userId = input['user_id']
    if len(userId) == 0:
        return JsonResponse(getError("userId is missing in request"))
    
    userExist = User_personal_info.objects.filter(user_id__exact = userId).exists()
    if userExist == False:
        return JsonResponse(getError("user not found"))

    CourseTypeId = input['coursetype_id']
    if len(CourseTypeId) == 0:
        return JsonResponse(getError("CourseTypeId is missing in request"))

    CourseId = input['course_id']
    if len(CourseId) == 0:
        return JsonResponse(getError("CourseId is missing in request"))

    BranchId = input['branch_id']
    if len(BranchId) == 0:
        return JsonResponse(getError("BranchId is missing in request"))
    
    Year = input['passout_year']
    if len(Year) == 0:
        return JsonResponse(getError("Year is missing in request"))

    Qualif = input['highest_qualif']
    if len(Qualif) == 0:
        return JsonResponse(getError("Qualification is  missing in request"))

    Aggre = input['aggregate']
    if (len(Aggre)!=2 and Aggre.isnumeric()== False):
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
        return JsonResponse(status = 200,data = Obj3)
    

@api_view(['GET'])  
def get_qualif_info(request):
    input = request.queryparams
    req_user_id = input['user_id']
    if len(req_user_id) == 0:
        return JsonResponse(getError("UserId is missing in request"))

    
    queryList = qualif_info.objects.filter(user_id__exact = req_user_id).values()
    responseQualifDetail = []
    for item in queryList:
        responseQualifDetail.append(item)
    
    return JsonResponse(responseQualifDetail,status=200,safe=False)


@api_view(['POST','GET'])  
def get_coursetypes(request):
    if request.method == 'POST':
        CourseType = request.data["coursetype_name"]
        CourseDuration = request.data["coursetype_duration"]
       
        Obj = coursetypes(coursetype_name = CourseType,coursetype_duration = CourseDuration)
        Obj.save()
        return JsonResponse(data={"coursetype_id":Obj.coursetype_id},status = 201,safe=False)
    
    queryList = coursetypes.objects.all()
    aList = []
    for item in queryList:
        temp = {"CourseType" : item.coursetype_name,"CourseTypeId": item.coursetype_id,"CourseDuration" : item.coursetype_duration}
        aList.append(temp)
    return JsonResponse(data = aList,status=200,safe=False)


@api_view(['POST','GET'])  
def get_courses(request):
    data = request.data
    if request.method == 'POST':
        CourseTypeId = data['coursetype_id']
        CourseName = data['course_name']
        temp = courses(course_name = CourseName,coursetype_id = CourseTypeId)
        temp.save()
        return JsonResponse(data={"course_id":temp.course_id},status = 201,safe=False)

    input = request.query_params
    req_coursetype_id = input.get('coursetype_id','')
    if len(req_coursetype_id) == 0:
        return JsonResponse(getError("CourseTypeId is missing in request"))

    queryList = courses.objects.filter(coursetype_id__exact = req_coursetype_id).values()
    responseCoursesList = []
    for item in queryList:
        responseCoursesList.append(item)
     
    return JsonResponse(data = responseCoursesList,status =200,safe = False)
    

@api_view(['POST','GET'])  
def get_branches(request):
    data = request.data
    if request.method == 'POST':
        CourseId = data['course_id']
        BranchName = data['branch_name']
        temp = branches(branch_name = BranchName,course_id = CourseId)
        temp.save()
        return JsonResponse(data={"branch_id":temp.branch_id},status = 201,safe=False)

    input = request.query_params
    req_course_id = input.get('course_id','')
    if len(req_course_id) == 0:
        return JsonResponse(getError("CourseId is missing in request"))

    queryList = branches.objects.filter(course_id__exact = req_course_id).values()
    responseBranchesList = []
    for item in queryList:
        responseBranchesList.append(item)
     
    return JsonResponse(data = responseBranchesList,status =200,safe = False)

@api_view(['GET','POST'])  
def skill_info(request):
    if request.method == 'POST':
        skill = request.data["skill"]
        obj = skills(skill_name=skill)
        obj.save()
        return JsonResponse(data={"skill_id":obj.skill_id},status = 201,safe=False)
    queryList = skills.objects.all()
    aList = []
    for item in queryList:
        aSkill = {"skill_id":item.skill_id,"skill_name":item.skill_name}
        aList.append(aSkill)
    return JsonResponse(data = aList,status=200,safe=False)


@api_view(['GET'])  
def get_userskill(request):
    input = request.query_params
    req_userId = input['user_id']
    if len(req_userId) == 0:
        return JsonResponse(getError("UserId is missing in request"))
    
    
    queryList = user_skill.objects.filter(user_id__exact = req_userId).values()
    responseUserSkillsList = []
    for item in queryList:
        responseUserSkillsList.append(item)
     
    return JsonResponse(responseUserSkillsList,status =200)
    



