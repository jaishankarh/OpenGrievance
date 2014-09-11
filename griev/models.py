from django.db import models
from django.contrib.auth.models import User

USER_TYPES = (('C','Client'),('Off','Officer'),('Org','Organisation'));
GENDER_CHOICES = (('M','Male'),('F','Female'));
DOMAIN_CHOICES = (('Public','Public'),('Private','Private'));
U_TYPES = {'C':'Client','Off':'Officer','Org':'Organisation'}

class UserType(models.Model):
	userid = models.ForeignKey(User)
	usertype = models.CharField(max_length=3,choices=USER_TYPES)
        registered = models.BooleanField();
	def __unicode__(self):
		return u'%s' %(self.userid.username + " " + U_TYPES[self.usertype])

class ClientDetails(models.Model):##rename this to client details
                userid = models.ForeignKey(User)
                username = models.CharField(max_length=30)
                first_name = models.CharField(max_length=30)
                last_name = models.CharField(max_length=30)
                dob = models.DateField(verbose_name="Date of Birth")
                gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
                email = models.EmailField();
                address = models.TextField()
                city = models.CharField(max_length=60)
                state = models.CharField(max_length=30)
                country = models.CharField(max_length=50)
                pincode = models.IntegerField(max_length=10)
                phone = models.CharField(max_length=12)
                image = models.ImageField(upload_to='photos',blank=True)
                
                def __unicode__(self):
                            return u'%s'%(self.username)


#********************************************************************************



#***************************************************************************************#
  
class Organisation(models.Model):
  userid = models.ForeignKey(User)
  Organisation_reg_no = models.IntegerField()
  name = models.CharField(max_length=30)
  address = models.CharField(max_length=60)
  city = models.CharField(max_length=60)
  state = models.CharField(max_length=30)
  country = models.CharField(max_length=50)
  email = models.EmailField();
  pincode = models.IntegerField(max_length=10)
  phone = models.CharField(verbose_name='Telepone',max_length=12)
  altphone = models.CharField(verbose_name='Alternate Contact No',max_length=12)
  
  def __unicode__(self):
    return u'%s' %(self.name)

#********************************************************************************  
  
class GrievanceOfficer(models.Model):
  userid = models.ForeignKey(User)
  organisation = models.ManyToManyField(Organisation)
  designation = models.CharField(max_length=30)
  first_name = models.CharField(max_length=30)
  last_name = models.CharField(max_length=30)
  dob = models.DateField(verbose_name="Date of Birth")
  gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
  domain = models.CharField(max_length=30, choices=DOMAIN_CHOICES)
  department = models.CharField(max_length=30)
  off_address = models.CharField(max_length=60, verbose_name="Official Address") #official address
  city = models.CharField(max_length=60)
  state = models.CharField(max_length=30)
  country = models.CharField(max_length=50)
  pincode = models.IntegerField(max_length=10)
  email = models.EmailField()#official email
  phone = models.CharField(max_length=12)
  keywords = models.TextField(verbose_name='Keywords (seperate using  commas)')
  
  def __unicode__(self):
    return u'%s %s' %(self.first_name,self.last_name)
  
#********************************************************************************
  
class GrievanceRegistration(models.Model):
  orgid = models.ManyToManyField(Organisation); #This is there so that we can refer to which organisation it went
  officerid = models.ForeignKey(User, related_name="officers") #which user is trying to resolve this issue..
  client_no = models.ForeignKey(User, related_name="clients") ##### to check how to add this..can we have two foreign keys of User table into this table??
  sector = models.CharField(max_length=40,choices=DOMAIN_CHOICES)
  description = models.TextField(verbose_name='A Short Description')
  state = models.CharField(max_length=30)
  city = models.CharField(max_length=30)
  location = models.CharField(max_length=50,verbose_name='Landmark/Street/Locality')
  pincode = models.IntegerField(max_length=10)
  time = models.TimeField()
  date = models.DateField()
  image = models.ImageField(blank=True,upload_to='Images_%d-%m-%Y')
  solved = models.BooleanField();
  keywords = models.TextField(verbose_name="Keywords");
  
  def __unicode__(self):
    return u'%s %s' %(self.officerid.username,self.date)  
  
#********************************************************************************

class GrievanceRedressed(models.Model):
  orgid = models.ManyToManyField(Organisation); #though this can be fetched from the grievance table.. the organistaion who resolves the issue may be a different one
  officerid = models.ForeignKey(User) #though this can be fetched from the grievance table.. the person who resolves the issue may be a different fellow
  grievance_id = models.ForeignKey(GrievanceRegistration)
  date = models.DateField()
  time_taken = models.TimeField()
  message = models.CharField(max_length=40)

  def __unicode__(self):
    return u'%s %s' %(self.grievance_id, self.date)
  
#********************************************************************************

# Create your models here.

