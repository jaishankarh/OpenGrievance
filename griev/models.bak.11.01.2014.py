from django.db import models
from django.contrib.auth.models import User

USER_TYPES = (('C','Client'),('Off','Officer'),('Org','Organisation'));
GENDER_CHOICES = (('M','Male'),('F','Female'));

class UserType(models.Model):
	userid = models.OneToOneField(User)
	usertype = models.CharField(max_length=1,choices=USER_TYPES)

class User_details(models.Model):##rename this to client details
                userid = models.OneToOneField(User)
                username = models.CharField(max_length=30)
                usertype = models.CharField(max_length=1,choices=USER_TYPES)##to remove this when new syncdb is done...
                first_name = models.CharField(max_length=30)
                last_name = models.CharField(max_length=30)
                dob = models.DateField(verbose_name="Date of Birth")
                gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
                email = models.EmailField();
                address = models.TextField()
                city = models.CharField(max_length=60)
                state = models.CharField(max_length=30)
                country = models.CharField(max_length=50)
                phone = models.CharField(max_length=10)
                Image = models.ImageField(upload_to='photos',blank=True)
                
                def __unicode__(self):
                            return u'%s'%(self.username)


#********************************************************************************



#***************************************************************************************#
  
class Organisation(models.Model):
  userid = models.OneToOneField(User)
  Organisation_reg_no = models.IntegerField()
  name = models.CharField(max_length=30)
  address = models.CharField(max_length=60)
  tel_no = models.IntegerField(verbose_name='Telepone')
  alt_tel_no = models.IntegerField(verbose_name='Alternate Contact No')
  
  def __unicode__(self):
    return u'%s' %(self.name)

#********************************************************************************  
  
class GrievanceOfficer(models.Model):
  userid = models.OneToOneField(User)
  organisation = models.ManyToManyField(Organisation)
  designation = models.CharField(max_length=30)
  domain = models.CharField(max_length=30)
  department = models.CharField(max_length=30)
  off_address = models.CharField(max_length=60) #official address
  email = models.EmailField()#official email
  phone = models.IntegerField()
  keywords = models.TextField(verbose_name='Keywords (seperate using  commas)')
  
  def __unicode__(self):
    return u'%s %s' %(self.first_name,self.last_name)
  
#********************************************************************************
  
class GrievanceRegistration(models.Model):
  orgid = models.ManyToManyField(Organisation); #This is there so that we can refer to which organisation it went
  officerid = models.OneToOneField(User) #which user is trying to resolve this issue..
  #client_no = models.OneToOneField(User) ##### to check how to add this..can we have two foreign keys of User table into this table??
  sector = models.CharField(max_length=40)
  description = models.TextField(verbose_name='A Short Description')
  state = models.CharField(max_length=30)
  city = models.CharField(max_length=30)
  location = models.CharField(max_length=50,verbose_name='Landmark/Street/Locality')
  time = models.TimeField()
  date = models.DateField()
  image = models.ImageField(blank=True,upload_to='Images_%d-%m-%Y')
  
  def __unicode__(self):
    return u'%s %s' %(self.client_no, self.date)  
  
#********************************************************************************
  
class GrievanceRedressed(models.Model):
  orgid = models.ManyToManyField(Organisation); #though this can be fetched from the grievance table.. the organistaion who resolves the issue may be a different one
  officerid = models.OneToOneField(User) #though this can be fetched from the grievance table.. the person who resolves the issue may be a different fellow
  grievance_id = models.OneToOneField(GrievanceRegistration)
  date = models.DateField()
  time_taken = models.TimeField()
  message = models.CharField(max_length=40)

  def __unicode__(self):
    return u'%s %s' %(self.grievance_id, self.date)
  
#********************************************************************************

# Create your models here.

