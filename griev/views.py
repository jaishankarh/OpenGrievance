# Create your views here.

from django.contrib.auth.models import User
from django.contrib import auth
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
from django.http import HttpResponseRedirect
from griev import formmodels
from griev import models
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.template.loader import get_template
from django.template import Context
from string import split
from django.db.models.query import QuerySet
from django.contrib.auth import logout


#*********************************************************************************************************************

def login(request):
#                if form.is_valid():
            if request.method == 'POST':
                    if 'next' in request.GET:
                        action_url = '/login/?next=%s' % request.GET['next'];
                    form = formmodels.LoginForm(request.POST)
                    if form.is_valid():
                        username = request.POST['username'];
                        password = request.POST['password'];
                        #email = request.POST['email'];
                        user = auth.authenticate(username=username, password=password);
                        #request.session.set_expiry(150);
                        if user is not None and user.is_active:
                            # Correct password, and the user is marked "active"
                            auth.login(request, user);
                            # Redirect to a success page.
                            try:
                                check_reg = models.UserType.objects.get(userid__username=request.user.username);
                                request.session['usertype']=check_reg.usertype;
                            except:
                                return render(request, 'user_home.html',{'title':"Sorry Unknown database error occured",'username':request.user.username});
                            if 'next' in request.REQUEST:
                                return HttpResponseRedirect(request.REQUEST['next']);
                            #next_url = request.GET['next']## rewrite this so that the view will forward the reqeust to the correct view..
                            return HttpResponseRedirect('/home');
                                #request.session.set_expiry(0);
                        else:
                            return HttpResponseRedirect('/login_failure');
                            
                              # Show an error page
                                #return HttpResponseRedirect('/login_failure/');
            else :
                form = formmodels.LoginForm()
                if 'next' in request.GET:
                    action_url = '/login/?next=%s' % request.GET['next'];
                else:
                    action_url = '/login/'
            return render(request, 'login_home.html',{'form':form, 'title':"User Login",'action_url':action_url});
                    #return HttpResponse("Not post!!");

#*********************************************************************************************************************
   
def logout_view(request):
    auth.logout(request);
    return HttpResponseRedirect('/login');
#def register(request):
#	
#	if(request.method == 'POST'):
#			if(request.session['usertype']=='C'):User Login
#				form = formmodels.UserReg(request.POST);
#			elif(request.session['usertype']=='Off'):
#				form = formmodels.OfficerReg(request.POST); ###have to change this UserReg constructor once the formmodel is made
#			elif(request.session['usertype']=='Org'):
#				form = formmodels.OrgReg(request.POST);###have to change this UserReg constructor once the formmodel is made
#			else: 
#				form = formmodels.UserReg(request.POST);
#			if form.is_valid():
#				#return success...
#				return HttpResponseRedirect('/login_success');
#			else:
#				second_part = render_to_string('second_part_reg.txt', {'form':form, 'title':"Register to Begin",'action_url':'/register/'});
#				first_part = render_to_string('first_part_reg.txt');username
#				render(request, 'register_generic.html',{'first_part_of_form':first_part, 'rest_of_form':second_part, 'action_url':'/register/'}); 
#			
#	else:			
#		rendered = render_to_string('first_part_reg.txt');
#		return render(request, 'register_generic.html',{'first_part_of_form':rendered, 'title':"Register to Begin",'action_url':'/register/'}); 
#
##*********************************************************************************************************************

def cal(request):
    form = formmodels.LoginForm()
    return render(request,'generic_home.html',{'form':form,'title':"Hello Please Login"})
#********************************************************************************************************************

def register(request):
    if(request.method == 'POST'):
        if 'which_page' in request.POST and request.POST['which_page'] == 'usertype_page':
            form = formmodels.UserSelect(request.POST);
            if form.is_valid():
                request.session['usertype'] = request.POST['usertype'];
                form = formmodels.FirstRegForm();
            return render(request, 'generic_reg.html',{'form':form, 'title':"Tell Us Who You Are?",'action_url':'/register/'});
        else:
            form = formmodels.FirstRegForm(request.POST);
            if form.is_valid():
                username = form.cleaned_data['username'];
                password = form.cleaned_data['password'];
                email = form.cleaned_data['email'];
                user = User.objects.create_user(username=username,password=password,email=email);
                user = auth.authenticate(username=username, password=password);
                auth.login(request,user);
                usertype = models.UserType(userid=user,usertype=request.session['usertype'],registered=False);	#this will fail if the session has timed out...		
                usertype.save();
                return redirect('/home');
            else:    
                return render(request, 'generic_reg.html',{'form':form, 'title':"Tell Us Who You Are?",'action_url':'/register/'});
    else:
        form = formmodels.UserSelect();
        text = "<input type=\"hidden\" name=\"which_page\" value=\"usertype_page\"/>";
        return render(request, 'generic_reg.html',{'form':form, 'title':"Tell Us Who You Are?",'action_url':'/register/','which_page':text});
##******************************************************************************************************************************88
def update_profile(request): #still the many to many saving is remaning... and the organisation update profile..have to learn how to access the multiple choice field select...
    if not request.user.is_authenticated():
	return redirect('/login/?next=%s' % request.path);
    try:
        check_reg = models.UserType.objects.get(userid__username=request.user.username);
    except:
        return render(request, 'user_home.html',{'title':"Sorry Unknown database error occured",'username':request.user.username});
    if(not(check_reg.registered == False)): #this line checks and is to shoo away people who are already registered..
        return redirect('//home');
    else:
        if(request.method == 'POST'):#1
            if(request.session['usertype']=='C'):
                form = formmodels.UserRegForm(request.POST);
                success = updateUser(request,form);
            elif(request.session['usertype']=='Off'):
                form = formmodels.OfficerRegForm(request.POST); 
                success = updateOfficer(request,form);
            else:
                form = formmodels.OrgRegForm(request.POST);
                success = updateOrg(request,form);
                
            if(success == True):
#                return render(request, 'user_home.html',{'title':"Welcome %s" %(request.user.username),'username':request.user.username});
                return render(request, 'user_home.html',{'title':'Welcome %s'%request.user.username,'username':request.user.username});
            return render(request, 'generic_reg.html',{'form':form, 'title':"Please take a moment to fill this information.",'action_url':'update_profile/'});

        else:#2
                request.session['usertype'] = check_reg.usertype;
                if(request.session['usertype']=='C'):
                   form = formmodels.UserRegForm();
                elif(request.session['usertype']=='Off'):
                   form = formmodels.OfficerRegForm(); ###have to change this UserReg constructor once the formmodel is made
                else:
                   form = formmodels.OrgRegForm();###have to change this UserReg constructor once the formmodel is made
                
                return render(request, 'generic_reg.html',{'form':form, 'title':"Please take a moment to fill this information.",'action_url':'update_profile/'});

#********************************************************************************************************************************
def updateUser(request, form):
    if form.is_valid():
        usertype = models.UserType.objects.get(userid=request.user);
        usertype.registered = True;
        newform = formmodels.UserRegForm(form.cleaned_data);
	newform = form.save(commit=False);
	newform.userid = request.user;
        newform.username = request.user.username;
        newform.email = request.user.email;
        newform.save();
        usertype.save();
        return True;
    else:
        return False;
    
#******************************************************************************************************************************
def updateOfficer(request, form):
    if form.is_valid():
        usertype = models.UserType.objects.get(userid=request.user);
        usertype.registered = True;
        newform = formmodels.OfficerRegForm(form.cleaned_data);
	newform = form.save(commit=False);
	newform.userid = request.user;
        newform.username = request.user.username;
        newform.email = request.user.email;
        newform.save();
        for org in form.cleaned_data['organisation']:
            newform.organisation.add(org);            
        
        usertype.save();
        #newform.save_m2m();
        return True;
    else:
        return False;
 
 #********************************************************************************************************************************
def updateOrg(request, form):
    if form.is_valid():
        usertype = models.UserType.objects.get(userid=request.user);
        usertype.registered = True;
        newform = formmodels.OfficerRegForm(form.cleaned_data);
	newform = form.save(commit=False);
	newform.userid = request.user;
        newform.username = request.user.username;
        newform.email = request.user.email;
        newform.save();
        for org in form.cleaned_data['organisation']:
            newform.organisation.add(org);            
        
        usertype.save();
        #newform.save_m2m();
        return True;
    else:
        return False;
 
 #********************************************************************************************************************************
				

def home_view(request):
    if not request.user.is_authenticated():
	return redirect('/login/?next=%s' % request.path);
    elif 'menus' in request.session:
        menus = request.session['menus'];
    else:
        try:
            user = models.UserType.objects.get(userid = request.user);
        
        except ObjectDoesNotExist:
            return render(request, 'user_home.html',{'title':"Sorry An unexpected error occured!!"});
        
        type = user.usertype;
        if(type == 'C'):
            links = {'my_grievances': 'My Grievances','post_grievance':'Post Your Grievance','statistics':'Statistics'}
            
        elif(type == 'Off'):
            links = {'pending_grievances':'Pending Unresolved Grievances','resolved_grievances':'Resolved Grievances','statistics':'My Stats'}
        elif(type == 'Org'):
            links = {'pending_grievances':'Pending Unresolved Grievances','resolved_grievances':'Resolved Grievances','statistics':'My Stats','view_officers':'Officers'}
            
        t = get_template("home_menus.html");
        menus = t.render(Context({"links":links}));
        request.session['menus'] = menus;
    return render(request, 'user_home.html',{'title':"Welcome %s" %(request.user.username),'username':request.user.username,'menus':menus});

#*********************************************************************************************************************

def login_failure(request):
            return render(request, 'home.html',{'username':"Invalid User!! Please Login Again"})
            
def post_grievance(request): ##need to implement a check that allows only clients to post a grievance..and also implement the updation of the registered field
	if not request.user.is_authenticated():
		return redirect('/login/?next=%s' % request.path);
        try:
            check_reg = models.UserType.objects.get(userid__username=request.user.username);
        except:
            return render(request, 'user_home.html',{'title':"Sorry Unknown database error occured",'username':request.user.username});
        if(check_reg.registered == False or check_reg.registered is None):
            return redirect('update_profile/');
	if(request.method=='POST'):
		form = formmodels.GrievanceReg(request.POST);
		if form.is_valid():
			 ##need to change this line.....
			newform = formmodels.GrievanceReg(form.cleaned_data);
			newform = form.save(commit=False);
                        newform.client_no = request.user;	
                        
			officer = allocate_best_officer(form.cleaned_data);
                        if officer is not False:
                            newform.officerid = officer.userid;
                            newform.solved = False;
                            newform.save();
                            associated_org = officer.organisation.all()
                            for org in associated_org:
                                newform.orgid.add(org);#need to change this line tooooooo.,......
                            return render(request, 'user_home.html',{'title':'Grievance was Succesfully Posted...We will get back to you shortly!','username':request.user.username});
			return render(request, 'user_home.html',{'title':'Sorry there was an internal server error! Please try again!','username':request.user.username});					
			
			#newform.save_m2m();
			
		else:
			return render(request,'user_home.html',{'form':form, 'title':'Post your grievance','action_url':'post_grievance/'});
	else:
		form = formmodels.GrievanceReg();
		return render(request,'user_home.html',{'form':form, 'title':'Post your grievance','action_url':'post_grievance/'});
#**************************************************************************************************************************************
def allocate_best_officer(data):
    keyword = data['keywords'];
    #found_officers=QuerySet(model=models.GrievanceOfficer);
    #for word in chosen_words:
    found_officers = models.GrievanceOfficer.objects.filter(keywords__icontains=keyword);
        
    officers = found_officers;    
    if len(officers) is not 0:
        min_work_officer=officers[0];
        min_count = len(models.GrievanceRegistration.objects.filter(officerid=min_work_officer.userid).filter(solved=False));#to check the work load of an officer by counting how many grievance he already has against his name
        for officer in officers:
            if len(models.GrievanceRegistration.objects.filter(officerid=officer.userid).filter(solved=False)) < min_count:
                min_work_officer = officer;
        return min_work_officer;
    return False;
    
    
    ###this workload functionality is not working....have to check again....
    
        




#*****************************************************************************************************************************
#**************************************************************************************************************************************
def provide_keywords(request):
    if 'sector' in request.GET:
        officers = models.GrievanceOfficer.objects.filter(domain__iexact=request.GET['sector']);
        keywords = "";
        for officer in officers:
            keywords = keywords + officer.keywords;
        keywords = split(keywords,sep=",");
        t = get_template("sector_keywords.html");
        keyword_options = t.render(Context({'options':keywords}));
        
    return HttpResponse(keyword_options);    




#*****************************************************************************************************************************
                
def my_grievances(request):
	if not request.user.is_authenticated():
		return redirect('/login/?next=%s' % request.path);
	else:
		my_grievs = models.GrievanceRegistration.objects.filter(client_no_id=request.user.id);
        
        content = [];
        
        for item in my_grievs:
            associated_orgs = item.orgid.all();
            orgs="";
            temp = {};
            for org in associated_orgs:
                orgs = orgs + org.name + ", ";
            temp['orgs'] = orgs;
            temp['id'] = item.id;
            temp['officerid'] = item.officerid;
            temp['client_no'] = item.client_no;
            temp['sector'] = item.sector;
            temp['description'] = item.description;
            temp['state'] = item.state;
            temp['city'] = item.city;
            temp['location'] = item.location;
            temp['pincode'] = item.pincode;
            temp['time'] = item.time;
            temp['date'] = item.date;
            temp['image'] = item.image;
            temp['solved'] = item.solved;
            content.append(temp);
            
      ##all organisations are getting printed should change code for that...      
            
                
        action_url = "view_grievance";
        t = get_template("my_grievances_table.html");
        table_content = t.render(Context({"table_content":content,'action_url':action_url}));
        return render(request,'user_home.html',{'content':table_content,'menus':request.session['menus']});	
    
#**********************	**************************************************************************************************
def view_grievance(request,id):
    if not request.user.is_authenticated():
        return redirect('/login/?next=%s' % request.path);
    else:
        my_grievs = models.GrievanceRegistration.objects.get(pk=id);
        associated_orgs = my_grievs.orgid.all();
        orgs="";
        for value in associated_orgs:
                orgs = orgs + value.name + ", ";
        try:
            user = models.ClientDetails.objects.get(userid=my_grievs.client_no);
            officer = models.GrievanceOfficer.objects.get(userid=my_grievs.officerid);
        except ObjectDoesNotExist:
            return render(request,'user_home.html',{'content':'Sorry Internal Server Error occured!'});
        fields = {};
        fields['name'] = user.first_name + " " + user.last_name;
        fields['officer'] = officer.first_name + " " + officer.last_name;
        fields['orgs'] = orgs;
        fields['sector'] = my_grievs.sector;
        fields['description'] = my_grievs.description;
        fields['state'] = my_grievs.state;
        fields['city'] = my_grievs.city;
        fields['location'] = my_grievs.location;
        fields['pincode'] = my_grievs.pincode;
        fields['time'] = my_grievs.time;
        fields['date'] = my_grievs.date;
        fields['image'] = my_grievs.image;
        if my_grievs.solved == True:
            fields['solved'] = 'Case Resolved';
        else:
            fields['solved'] = "We are sorry...Officers are still working on your problem! "
        fields['keywords'] = my_grievs.keywords;
#        fields = {'date':date, 'time':time, 'name':name, 'officer':officer, 'sector':sector, 'description':description, 
#                    'keywords':keywords, 'location':location, 'city':city, 'state':state, 'pincode':pincode, 'image':image};
        type = request.session['usertype'];
        
        if(type == 'C'):
            links = {'history/'+id:'Review Trace','my_grievances': 'My Grievances','post_grievance':'Post Your Grievance','statistics':'Statistics'}
            
        elif(type == 'Off'):
            links = {'mark_resolved/'+id:'Mark As Resolved','pending_grievances':'Pending Unresolved Grievances','resolved_grievances':'Resolved Grievances','statistics':'My Stats'}
            
        elif(type == 'Org'):
            links = {'mark_resolved/'+id:'Mark As Resolved','pending_grievances':'Pending Unresolved Grievances','resolved_grievances':'Resolved Grievances','statistics':'My Stats','view_officers':'Officers'}
            
        
        t = get_template("home_menus.html");
        menus = t.render(Context({"links":links}));
        
        t = get_template("view_grievance.html");
        table_content = t.render(Context({"fields":fields}));
        return render(request,'user_home.html',{'content':table_content,'menus':menus});	

#def edit_grievances(request, id):
#
#   
#    if not request.user.is_authenticated():
#        return redirect('/login/?next=%s' % request.path);
#    elif request.method == 'POST':
#                    form = formmodels.GrievanceReg(request.POST)
#                    if form.is_valid():
#                        #org = models.Organisation.objects.get(name='Yahoo'); ##need to change this line.....
#                        #newform = formmodels.GrievanceReg(form.cleaned_data);
#                        #newform = form.save(commit=False);
#                        #newform.officerid = request.user;
#                        #newform.orgid = org;
#                        #newform.client_no = request.user;                        
#                        #newform.save();
#                        #newform.save_m2m();
#                        clean_form = form.cleaned_data;
#                        old = models.GrievanceRegistration.objects.get(pk=request.session['id']);
#                        old.date = clean_form['date'];
#                        old.time = clean_form['time'];
#                        old.sector = clean_form['sector'];
#                        old.description = clean_form['description'];
#                        old.state = clean_form['state'];
#                        old.city = clean_form['city'];
#                        old.location = clean_form['location'];
#                        old.pincode = clean_form['pincode'];
#                        old.save();
#                        return render(request,'user_home.html',{'content':'Successfully edited your grievance!',});
#                    else:
#                        return render(request,'user_home.html',{'form':form, 'title':'Edit your grievance','action_url':request.path});
#                        
#    else :
#         griev_id = id;
#         my_griev = models.GrievanceRegistration.objects.get(id=griev_id);
#         form = formmodels.GrievanceReg(instance=my_griev);
#         request.session['id']=id;
#         return render(request, 'user_home.html',{'form':form, 'title':"Edit your grievance",'action_url':request.path});
#                    #return HttpResponse("Not post!!");
def pending_grievances(request):
        if not request.user.is_authenticated():
		return redirect('/login/?next=%s' % request.path);
        if 'menus' not in request.session:
            return redirect('/home')
	else:
		my_grievs = models.GrievanceRegistration.objects.filter(officerid=request.user.id).filter(solved=False);
        
        content = [];
        
        for item in my_grievs:
            associated_orgs = item.orgid.all();
            orgs="";
            temp = {};
            for org in associated_orgs:
                orgs = orgs + org.name + ", ";
            temp['orgs'] = orgs;
            temp['id'] = item.id;
            temp['officerid'] = item.officerid;
            temp['client_no'] = item.client_no;
            temp['sector'] = item.sector;
            temp['description'] = item.description;
            temp['state'] = item.state;
            temp['city'] = item.city;
            temp['location'] = item.location;
            temp['pincode'] = item.pincode;
            temp['time'] = item.time;
            temp['date'] = item.date;
            temp['image'] = item.image;
            temp['solved'] = item.solved;
            content.append(temp);
            
      ##all organisations are getting printed should change code for that...      
            
        
        action_url = "view_grievance";
        t = get_template("my_grievances_table.html");
        table_content = t.render(Context({"table_content":content,'action_url':action_url}));
        return render(request,'user_home.html',{'content':table_content,'menus':request.session['menus']});
    
def mark_resolved(request,id):
        if not request.user.is_authenticated():
		return redirect('/login/?next=%s' % request.path);
        if 'menus' not in request.session:
            return redirect('/home')
	else:
            try:
		my_grievs = models.GrievanceRegistration.objects.get(id=id);
            except ObjectDoesNotExist:
                return render(request,'user_home.html',{'content':'Sorry Internal Server Error occured!'});
            my_grievs.solved=True;
            my_grievs.save();
            return render(request,'user_home.html',{'content':'Resolved Successfully!','menus':request.session['menus']});
        
###################################################################################################################################
def resolved_grievances(request):
        if not request.user.is_authenticated():
		return redirect('/login/?next=%s' % request.path);
        if 'menus' not in request.session:
            return redirect('/home')
	else:
		my_grievs = models.GrievanceRegistration.objects.filter(officerid=request.user.id).filter(solved=True);
        
        content = [];
        
        for item in my_grievs:
            associated_orgs = item.orgid.all();
            orgs="";
            temp = {};
            for org in associated_orgs:
                orgs = orgs + org.name + ", ";
            temp['orgs'] = orgs;
            temp['id'] = item.id;
            temp['officerid'] = item.officerid;
            temp['client_no'] = item.client_no;
            temp['sector'] = item.sector;
            temp['description'] = item.description;
            temp['state'] = item.state;
            temp['city'] = item.city;
            temp['location'] = item.location;
            temp['pincode'] = item.pincode;
            temp['time'] = item.time;
            temp['date'] = item.date;
            temp['image'] = item.image;
            temp['solved'] = item.solved;
            content.append(temp);
            
      ##all organisations are getting printed should change code for that...      
            
        
        action_url = "view_grievance";
        t = get_template("my_grievances_table.html");
        table_content = t.render(Context({"table_content":content,'action_url':action_url}));
        return render(request,'user_home.html',{'content':table_content,'menus':request.session['menus']});