from django import template

register = template.Library();

@register.filter(name='field_type')
def field_type(value):
	return  value.__class__.__name__;
	
	
@register.filter(name='make_div_id')
def make_div_id(value):
	return  "div_"+value;

@register.filter(name='make_radio_id')
def make_radio_id(value,arg):
	return  value[:len(value)-2] +"_" + str(arg);
