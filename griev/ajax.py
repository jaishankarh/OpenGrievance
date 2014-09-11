from django.utils import simplejson
from django.template.loader import render_to_string
from griev import formmodels
from dajaxice.decorators import dajaxice_register


@dajaxice_register
def rest_of_form(request):
	request.session['usertype'] = usertype;
	form = formmodels.UserReg();
	rendered = render_to_string('second_part_reg.txt', {'form':form, 'title':"Register to Begin",'action_url':'/register/'})
	return simplejson.dumps({'form_data':rendered})
 
