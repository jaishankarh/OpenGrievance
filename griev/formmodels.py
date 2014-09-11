from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from griev import models
from django.core.exceptions import ObjectDoesNotExist
import re

USER_TYPES = (('C','Client'),('Off','Officer'),('Org','Organisation'));
GENDER_CHOICES = (('M','Male'),('F','Female'));
KEYWORD_CHOICES = (('','-------'));

#****************************************************************************************************************

class CalendarWidget(forms.TextInput):
    class Media:
        css = {'all':('custom_widgets/calendar-widget/css/jquery-ui.css',)};
        js = ('custom_widgets/calendar-widget/js/jquery-1.9.1.js','custom_widgets/calendar-widget/js/jquery-ui.js','custom_widgets/calendar-widget/js/script.js');
        
#****************************************************************************************************************   
        
class DateTimeWidget(forms.TextInput):
    class Media:
        css = {'all':('custom_widgets/datetime-widget/css/jquery.datetimepicker.css',)};
        js = ('custom_widgets/datetime-widget/js/jquerydatetimepicker.js','custom_widgets/datetime-widget/js/script.js');
                  
#****************************************************************************************************************

class CustomSectorWidget(forms.Select): #this widget is exculsively for the ajax feature of the post grievance form..to get the key words via ajax..
    class Media:
        js = ('custom_widgets/custom-domain-widget/js/sectorscript.js',);
                  
#****************************************************************************************************************

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

#****************************************************************************************************************    
    
class UserSelect(forms.Form):
	usertype = forms.ChoiceField(widget=forms.RadioSelect, choices=USER_TYPES);
	
#****************************************************************************************************************    
    
class OfficerReg(ModelForm):
    class Meta:
        model = models.GrievanceOfficer;
        exclude = ['userid'];
    def clean_phone(self):
        phone = self.cleaned_data['phone'];
        if(re.match(r'\d{6,10}',phone) is not None):
                return phone
        raise forms.ValidationError("Incorrect Phone number!!");
        return phone;	
			
#****************************************************************************************************************                                
                                
class OfficerRegForm(OfficerReg):
					
	class Meta(OfficerReg.Meta):
		fields= ['first_name','last_name','dob','gender','organisation','designation','keywords','domain','department','phone','off_address','country','state','city','pincode']
		widgets = {
                        'first_name': forms.TextInput(attrs={'placeholder':'Enter First Name', 'max_length':30,'size':35}),
                        'last_name' : forms.TextInput(attrs={'placeholder':'Enter Last Name', 'max_length':30,'size':35}),
                        'designation' : forms.TextInput(attrs={'placeholder':'What is your Designation', 'max_length':30,'size':35}),
                        'department' : forms.TextInput(attrs={'placeholder':'Your Department at Work', 'max_length':30,'size':35}),
                        'domain' : forms.TextInput(attrs={'placeholder':'Your Work Domain', 'max_length':30,'size':35}),
                        'phone' : forms.TextInput(attrs={'placeholder':'Contact No', 'max_length':10,'size':35}),
                        'off_address' : forms.Textarea(attrs={'placeholder':'Official Address'}),
                        'city': forms.TextInput(attrs={'placeholder':'Enter Your City', 'max_length':60,'size':35}),
                        'state': forms.TextInput(attrs={'placeholder':'Enter State', 'max_length':30,'size':35}),
                        'country': forms.TextInput(attrs={'placeholder':'Enter Country', 'max_length':30,'size':35}),
                        'dob': CalendarWidget(attrs={'placeholder':'When were you Born?', 'max_length':10,'size':35,'id':'date'}),
                        'pincode': forms.TextInput(attrs={'placeholder':'Area Pincode', 'max_length':30,'size':35}),
                        'gender' : forms.RadioSelect,								
        }
	
#****************************************************************************************************************
        
class OrgReg(ModelForm):
        class Meta:
            model = models.Organisation;
            exclude = ['userid'];

        def clean_phone(self):
            phone = self.cleaned_data['phone'];
            if(re.match(r'\d{6,10}',phone) is not None):
                    return phone;
            else:
                    raise forms.ValidationError("Incorrect Phone number!!");
            return phone;	

        def clean_altphone(self):
            phone = self.cleaned_data['altphone'];
            if(re.match(r'\d{6,10}',phone) is not None):
                    return phone;
            else:
                    raise forms.ValidationError("Incorrect Phone number!!");
            return phone;	
				
#****************************************************************************************************************
class OrgRegForm(OrgReg):
		
	class Meta(OrgReg.Meta):
            fields= ['Organisation_reg_no','name','phone','address','country','state','city','pincode']
            widgets = {
                'Organisation_reg_no': forms.TextInput(attrs={'placeholder':'Enter Organisation Registration No', 'max_length':30,'size':35}),
                'name' : forms.TextInput(attrs={'placeholder':'Enter Name', 'max_length':30,'size':35}),
                'address' : forms.Textarea(attrs={'placeholder':'Address'}),
                'city': forms.TextInput(attrs={'placeholder':'Enter Your City', 'max_length':60,'size':35}),
                'state': forms.TextInput(attrs={'placeholder':'Enter State', 'max_length':30,'size':35}),
                'country': forms.TextInput(attrs={'placeholder':'Enter Country', 'max_length':30,'size':35}),
                'pincode': forms.TextInput(attrs={'placeholder':'Area Pincode', 'max_length':30,'size':35}),
								
        }
#****************************************************************************************************************
    
class UserReg(ModelForm):
        class Meta:
            model = models.ClientDetails;
            exclude = ['userid'];


        def clean_phone(self):
            phone = self.cleaned_data['phone'];
            if(re.match(r'\d{6,10}',phone) is not None):
                    return phone;
            else:
                    raise forms.ValidationError("Incorrect Phone number!!");
            return phone;	

        def clean_username(self):
            username = self.cleaned_data['username'];
            try:
                    user = User.objects.get(username=username);
            except User.DoesNotExist:
                    return username;
            raise forms.ValidationError("Username is already taken...Please choose another one!");
            return username;	

        def clean_email(self):
            email = self.cleaned_data['email'];
            try:
                    user = User.objects.get(email__exact=email);
            except User.DoesNotExist:
                    return email;
            raise forms.ValidationError("This Email is already registered with us!! Please choose another one!");
            return email;	
#****************************************************************************************************************
class UserRegForm(UserReg):
				
	class Meta(UserReg.Meta):
            fields= ['first_name','last_name','gender','dob','phone','address','country','state','city','pincode']
            widgets = {
                'first_name': forms.TextInput(attrs={'placeholder':'Enter First Name', 'max_length':30,'size':35}),
                'last_name' : forms.TextInput(attrs={'placeholder':'Enter Last Name', 'max_length':30,'size':35}),
                'phone' : forms.TextInput(attrs={'placeholder':'Contact No', 'max_length':10,'size':35}),
                'address' : forms.Textarea(attrs={'placeholder':'Address'}),
                'city': forms.TextInput(attrs={'placeholder':'Enter Your City', 'max_length':60,'size':35}),
                'state': forms.TextInput(attrs={'placeholder':'Enter State', 'max_length':30,'size':35}),
                'country': forms.TextInput(attrs={'placeholder':'Enter Your Nationality', 'max_length':30,'size':35}),
                'dob': CalendarWidget(attrs={'placeholder':'When were you Born?', 'max_length':10,'size':35,'id':'date'}),
                'gender' : forms.RadioSelect,
        }
								
#****************************************************************************************************************
class LoginForm(forms.Form):
    username = forms.CharField();
    password = forms.CharField(widget=forms.PasswordInput);
    #email = forms.EmailField(max_length=30);
    
class FirstRegForm(forms.Form):
    username = forms.CharField();
    password = forms.CharField(widget=forms.PasswordInput);
    password_confirm = forms.CharField(widget=forms.PasswordInput);
    email = forms.EmailField(max_length=30);
    widgets = {
            'username': forms.TextInput(attrs={'placeholder':'Choose User Name', 'max_length':30,'size':35}),
            'password': forms.PasswordInput(attrs={'placeholder':'Choose A Password', 'max_length':30,'size':35}),
            'password_confirm': forms.PasswordInput(attrs={'placeholder':'Choose A Password', 'max_length':30,'size':35}),
            'email' : forms.TextInput(attrs={'placeholder':'Email','size':35}),
        }
    def clean_username(self):
        if 'username' in self.cleaned_data:
            username = self.cleaned_data['username'];
            try:
                check_exist = User.objects.get(username=username);
            except ObjectDoesNotExist:
                return username;
            raise forms.ValidationError("Username is already taken. Please Choose a new Username.");
            return username;
        raise forms.ValidationError("Please enter your desired username.");
        return username;
    
    def clean(self):
        if 'password' in self.cleaned_data:
            if 'password_confirm' in self.cleaned_data:
                password = self.cleaned_data['password'];
                password_confirm = self.cleaned_data['password_confirm'];
                if(password != password_confirm):
                    raise forms.ValidationError("Passwords don't match. Please try again!");
                return self.cleaned_data;
        raise forms.ValidationError("Please enter a password.");
        return self.cleaned_data;

#*******************************************************************************************************************

class GrievanceReg(ModelForm):
    
    class Meta:
        model = models.GrievanceRegistration;
        exclude = ['orgid','officerid','client_no'];
        fields= ['date','time','sector','description','keywords','location','state','city','pincode','image'];
        widgets = {
            'date': CalendarWidget(attrs={'id':'date','placeholder':'Date of Event', 'max_length':30,'size':35}),
            'time': DateTimeWidget(attrs={'placeholder':'Time of Event', 'max_length':30,'size':35,'id':'time'}),
            'description' : forms.Textarea(attrs={'placeholder':'Write a few words about your mishap...', 'rows':30,'cols':35}),
            'location' : forms.TextInput(attrs={'placeholder':'Enter Location', 'max_length':30,'size':35}),
            'city': forms.TextInput(attrs={'placeholder':'Enter Your City', 'max_length':60,'size':35}),
            'state': forms.TextInput(attrs={'placeholder':'Enter State', 'max_length':30,'size':35}),
            'sector':CustomSectorWidget(attrs={'id':"id_sector",'size':35}),
            'keywords':forms.Select(attrs={'id':"id_keywords",'size':35,'row':6}),


    }