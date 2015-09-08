from django.contrib.auth.models import User
from donorsdetail.models import *
from tastypie.resources import Resource,ModelResource
from tastypie import fields
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import *
import json
from django.core.serializers.json import DjangoJSONEncoder
from itertools import groupby
from operator import itemgetter
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from requests import Request, Session
from requests.auth import AuthBase
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
import time
import datetime
import itertools
from django.contrib.auth import authenticate, login

# from tastypie import allowed_methods



class dict2obj(object):
  def __init__(self, initial=None):
    self.__dict__['_data'] = {}

    if hasattr(initial, 'items'):
      self.__dict__['_data'] = initial

  def __getattr__(self, name):
    return self._data.get(name, None)

  def __setattr__(self, name, value):
    self.__dict__['_data'][name] = value

  def to_dict(self):
    return self._data


class UserRegisterResource(ModelResource):
    class Meta:
        queryset = UserRegister.objects.all()
        resource_name = 'user_register'
        include_resource_uri = False
        allowed_methods = ['post']
    
    def obj_create(self, bundle, request=None, **kwargs):
        username = bundle.data['dusername']
        if User.objects.filter(username=username):
            status = "not"
        else:
            auth = User.objects.create(username=username)
            auth.set_password(bundle.data['dpswd'])
            auth.save()
            new_user = UserRegister.objects.create(
                                                    name=username,
                                                    gender=bundle.data['dgender'],
                                                    age='5',
                                                    mail_id=bundle.data['dmail'],
                                                    phone_no=bundle.data['dnumber'],
                                                    address=bundle.data['daddress'],
                                                    password=bundle.data['dpswd'],
                )
            status = "saved"
        raise ImmediateHttpResponse(response=HttpResponse(content=json.dumps({'status':status}), content_type='application/json'))


class Donorlogin(ModelResource,AuthBase):
    class Meta:
        resource_name = 'donorlogin'
        queryset = UserRegister.objects.all()
        include_resource_uri = False
        allowed_methods = ['post']


    def obj_create(self, bundle, request=None, **kwargs):
        login_name = bundle.data['uname']
        login_pswd = bundle.data['pswd']
        user = authenticate(username=login_name, password=login_pswd)
        if user is not None:
            if user.is_superuser:
                login(bundle.request, user)
                status = 'admin'
            elif user.is_active:
                login(bundle.request, user)
                status =  'success'
        else:
            status = 'failure'
        raise ImmediateHttpResponse(response=HttpResponse(content=json.dumps({'status':status}), content_type='application/json'))


class Changepswd(Resource):
    class Meta:
        resource_name = 'change_pswd'
        queryset= UserRegister.objects.all()
        include_resource_uri = False
        allowed_methods = ['patch']

    def patch_list(self, request, **kwargs):
        data = eval(request.body)        
        cuser = data['cusername']
        cpswd = data['cpswd']
        changepswd = User.objects.filter(username=cuser)
        if changepswd:
            changepswd[0].set_password(cpswd)
            changepswd[0].save()
            status='saved'
        else:
            status='failed'
        raise ImmediateHttpResponse(response=HttpResponse(content=json.dumps({'status':status}),content_type='application/json'))
    


class Donatedetail(ModelResource):
    class Meta:
        resource_name = 'donate_detail'
        include_resource_uri = False
        queryset = DonorsContriDetails.objects.all()
        authentication = Authentication()
        authorization = Authentication()

    def obj_create(self,bundle,request=None,**kwargs):
        donor_project = bundle.data['dproject'] 
        donor_scheme = bundle.data['dscheme']
        donate_amount = bundle.data['damount']
        cur_date = time.strftime("%d/%m/%y")
        if bundle.data['cur_usr'] =='web':
            current_user=bundle.request.user
        else:
            current_user=bundle.data['cur_usr']

        donate_detail = DonorsContriDetails.objects.create(
                                                                    username = current_user,
                                                                    project = donor_project,
                                                                    scheme = donor_scheme,
                                                                    amount = donate_amount,
                                                                    status ='Paid',
                                                                    paid_date = cur_date,
                                                                    hscheme=''
                                                                )
        status = "saved"
        raise ImmediateHttpResponse(response = HttpResponse(content=json.dumps({'status':status}),content_type = 'application/json'))



class Showdonatedetails(Resource):
    class Meta:
        resource_name = 'show_dd_admin'
        object_class = dict2obj
        include_resource_uri = False
        # queryset = DonorsContriDetails.objects.all()


    def obj_get_list(self, bundle, **kwargs):
        if bundle.data['key']=='admin':
            data = []
            donate_detail = DonorsContriDetails.objects.all()
            for i in donate_detail:
                data.append({'user':i.username,'project':i.__dict__['project'],'scheme':i.scheme,'amount':i.amount,'status':i.status,'paid_date':i.paid_date})
            raise ImmediateHttpResponse(response = HttpResponse(content = json.dumps({'cont_all':data}),content_type = 'application/json'))

        if bundle.data['key']== 'all_users':
            a_user=[]
            all_user=UserRegister.objects.all()
            a_user =[i.name for i in all_user]
            raise ImmediateHttpResponse(response = HttpResponse(content = json.dumps({'all_users':a_user}),content_type = 'application/json'))




class Showmycontribution(ModelResource):
    class Meta:
        resource_name = 'my_contribution'
        queryset = DonorsContriDetails.objects.all()
        fields = ['project','scheme','amount','status','paid_date']
        include_resource_uri = False


    def get_object_list(self,request):
        user = request.user 
        return super(Showmycontribution, self).get_object_list(request).filter(username=user.username)

    def obj_create(self,bundle,request=None,**kwargs):
        """" this post method for android app"""
        data=[]
        my_contribution = DonorsContriDetails.objects.filter(username=bundle.data['current_user'])
        for i in my_contribution:
            data.append({'user':i.username,'project':i.project,'scheme':i.scheme,'amount':i.amount+'.Rs','status':i.status,'paid_date':i.paid_date})
        raise ImmediateHttpResponse(response = HttpResponse(content = json.dumps({'my_contribution':data}),content_type = 'application/json'))

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict) and 'meta' in data_dict:
            del(data_dict['meta'])
            data_dict['my_contribution'] = data_dict['objects']
            del data_dict['objects']
        return data_dict



class Accountsetting(ModelResource):
    class Meta:
        resource_name = 'account_setting'
        queryset = ProjectsAndSchemes.objects.all()
        include_resource_uri = False

    def get_object_list(self,request):  
        account_setting = DonorsContriDetails.objects.all().values()
        data =[]
        data1 = []
        for pr,sch in groupby(sorted(account_setting,key=itemgetter('project')),key=itemgetter('project')):
            res = {}
            res['project'], amount = pr, [ v['amount'] for v in sch]
            for i in amount:
                data1.append(int(i))
            b=sum(data1)
            res['amount']=b
            data.append(res)
        raise ImmediateHttpResponse(response = HttpResponse(content = json.dumps({'projects':data}),content_type='application/json'))

class Donorsstatus(ModelResource):
    class Meta:
        resource_name = 'donors_status'
        include_resource_uri = False
        

    def obj_create(self,bundle,request=None,**kwargs):
        data=[]
        ary=[]
        i =datetime.datetime.now()
        st=DonorProject.objects.filter(project=bundle.data['pro_model'],scheme=bundle.data['sch_model'])
        for i in st:
            dcd=DonorsContriDetails.objects.filter(project=bundle.data['pro_model'],scheme=bundle.data['sub_sch_model'],username=i.user)
            for j in dcd:
                if j.username in i.user:
                    ary.append(j.username)
            if i.user in ary:
                print i.user
            else:
                data.append({'user':i.user,'status':'Pending'}) 
        raise ImmediateHttpResponse(response=HttpResponse(content=json.dumps({'pendinguser':data}),content_type='application/json'))



class Showdonorproject(ModelResource):
    class Meta:
        resource_name = 'show_donor_project'
        queryset = DonorProject.objects.all()
        include_resource_uri = False
        fields = ['project', 'scheme']

    def get_object_list(self,request):
        data = []
        user = request.user
        # return super(Showdonorproject, self).get_object_list(request).filter(user=user)
        donor_pro = DonorProject.objects.filter(user = user)
        for i in donor_pro:
            data.append({'project':i.project,'schemes':i.scheme})
        raise ImmediateHttpResponse(response = HttpResponse(content = json.dumps({'projects':data}),content_type='application/json'))

    def obj_create(self,bundle,request=None,**kwargs):
        data=[]
        user = bundle.data['current_user']
        donor_pro = DonorProject.objects.filter(user=user)
        for  i in donor_pro:
            data.append({'project':i.project,'schemes':i.scheme})
        raise ImmediateHttpResponse(response=HttpResponse(content=json.dumps({'projects':data}),content_type='application/json'))
    
    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict) and 'meta' in data_dict:
            del data_dict['meta']
            data_dict['projects'] = data_dict['objects']
            del data_dict['objects']
        return data_dict




class ProjectSchemeCreate(ModelResource):
    class Meta:
        resource_name = 'project_and_scheme'
        queryset = ProjectsAndSchemes.objects.all()
        include_resource_uri = False

    
    def obj_create(self,bundle,request=None,**kwargs):
        data = []
        key = bundle.data['key']
        if key == 'key':
            add_pro = bundle.data['anew_pro']
            add_sch = bundle.data['anew_sch']
            ProjectsAndSchemes.objects.create(project = add_pro,
                                                scheme = add_sch,
                                                )
            status="saved"
            raise ImmediateHttpResponse(response = HttpResponse(content = json.dumps({'status':status}),content_type = 'application/json'))
        elif key == 'settings':
            array_sub_schem=[]
            # user = bundle.request.user
            pro = bundle.data['spro_model']
            sch = bundle.data['ssch_model']
            if bundle.data['cur_usr'] == 'web':
                user=bundle.request.user
            else:
                user=bundle.data['cur_usr']
            if bundle.data['ssch_model']=="monthly":
                array_sub_schem=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
            
            elif bundle.data['ssch_model']=="yearly":
                i=datetime.datetime.now()
                year= i.year-20
                i=0
                while i<40:
                    array_sub_schem.append(year+i)
                    i=i+1

            elif bundle.data['ssch_model']=="quarterly":
                array_sub_schem=['q1','q2','q3','q4']

            a = DonorProject.objects.filter(user=bundle.request.user)
            mob = DonorProject.objects.filter(user=bundle.data['cur_usr'])
            if a:
                a.update(project=pro,scheme=sch,subscheme=array_sub_schem)
                status = 'update'
                raise ImmediateHttpResponse(response = HttpResponse(content = json.dumps({'status':status}),content_type = 'application/json'))
            else:
                DonorProject.objects.create(
                                            user = user,
                                            project = pro,
                                            scheme = sch,
                                            subscheme=array_sub_schem,
                                     )
                status = 'saved'
                raise ImmediateHttpResponse(response = HttpResponse(content = json.dumps({'status':status}),content_type = 'application/json'))
        elif key == 'delete':
            del_pro = bundle.data['spro_model']
            del_sch = bundle.data['ssch_model']
            del_field = ProjectsAndSchemes.objects.filter(project=del_pro,scheme=del_sch).delete()
            status='deleted'
            raise ImmediateHttpResponse(response = HttpResponse(content = json.dumps({'status':status}),content_type = 'application/json'))
        elif key == 'change':
            user = bundle.request.user
            pro = bundle.data['spro_model']
            sch = bundle.data['ssch_model']
            usr=bundle.data['usr']
            if bundle.data['usr']=='web':
                check = DonorsContriDetails.objects.filter(project=pro,scheme=sch,username=user)
            else:
                check = DonorsContriDetails.objects.filter(project=pro,scheme=sch,username=usr)
            if check:
                for  i in check:
                    amount=i.amount
                    # status=({'status':"exist","amount":i.amount})
                raise ImmediateHttpResponse(response = HttpResponse(content = json.dumps({'amount':amount}),content_type = 'application/json'))
            else:
                amount="0"
                raise ImmediateHttpResponse(response = HttpResponse(content = json.dumps({'amount':amount}),content_type = 'application/json'))
                
           
    def get_object_list(self,request):
        data = []
        projects = ProjectsAndSchemes.objects.all().values()
        for pr, sch in groupby(sorted(projects, key=itemgetter('project')), key=itemgetter('project')):
            res = {}
            res['project'], res['schemes'] = pr, [ v['scheme'] for v in sch]
            data.append(res)  
        raise ImmediateHttpResponse(response = HttpResponse(content = json.dumps({'project':data}),content_type = 'application/json'))
    

