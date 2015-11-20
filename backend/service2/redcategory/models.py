#encoding:utf-8
from django.db import models
import datetime, pytz
from django.utils.timezone import get_current_timezone, make_aware, utc

def localize_datetime(dtime):
	tz_aware = make_aware(dtime, utc).astimezone(get_current_timezone())
	return datetime.datetime.strftime(tz_aware, '%Y-%m-%d %H:%M:%S')

class client(models.Model):
	base = models.CharField(max_length=500, default='nobase')
	name = models.CharField(max_length=50)
	phone = models.CharField(max_length=50)
	email = models.EmailField()
	region = models.CharField(max_length=50, default="noregion")
	commune = models.CharField(max_length=50, default="nocommune")
	gender = models.CharField(max_length=50)
	age = models.CharField(max_length=50)
	typemath = models.CharField(max_length=50, default="notypemath")
	math = models.CharField(max_length=1000, default="nomath")
	status = models.CharField(max_length=50, default='incomplete')
	date = models.DateTimeField(auto_now_add=True)
	buy = models.CharField(max_length=50 , default='0')
	description = models.CharField(max_length=1000 , default='nodescription')
	gr = models.CharField(max_length=50, default='0')
	it = models.CharField(max_length=50, default='0')
	@property
	def created_tz(self):
		return localize_datetime(self.date)


class vendor(models.Model):
	base = models.CharField(max_length=500, default='nobase')
	base_login = models.CharField(max_length=500, default='nobase_login')
	name = models.CharField(max_length=50, default='noname')
	phone = models.CharField(max_length=50, default='nophone')
	email = models.EmailField()
	coins_avaiable = models.CharField(max_length=50 , default='0')
	coins_used = models.CharField(max_length=50, default='0')
	user = 	models.CharField(max_length=50, default='nouser')
	psw = models.CharField(max_length=1000 ,default='nopsw')
	delay = models.CharField(max_length=1000 ,default='50000')
	date = models.DateTimeField(auto_now_add=True)
	validate = models.CharField(max_length=1000 ,default='0')
	robot = models.CharField(max_length=1000 ,default='noview')
	mail_send = models.CharField(max_length=50, default='1')
	segment = models.CharField(max_length=50, default='nosegment')
	gr = models.CharField(max_length=50, default='2')
	link = models.CharField(max_length=1000 ,default='potenciales')
	@property
	def created_tz(self):
		return localize_datetime(self.date)
	

class clients_vendor(models.Model):
	id_vendor = models.CharField(max_length=500, default='noid_vendor')
	id_client = models.CharField(max_length=500, default='noid_client')
	date = models.DateTimeField(auto_now_add=True)
	@property
	def created_tz(self):
		return localize_datetime(self.date)


class block(models.Model):
	base = models.CharField(max_length=500, default='nobase')
	isapre = models.CharField(max_length=500, default='noisapre')
	date = models.DateTimeField(auto_now_add=True)
	@property
	def created_tz(self):
		return localize_datetime(self.date)
	
	
		
		