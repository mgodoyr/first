# coding=utf-8
from __future__ import absolute_import
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'service.settings'
from bluecategory.models import *
import json, base64, time, sys, re, datetime, time, pytz
from django.db.models import Sum
from django.utils import timezone


def prefvalid(pre,year):
	if pre == "Fonasa":
		return True
	elif year =="+1" or year == "No lo sabe":
		return True
	return False

def region(rgn):
	with open('/backend/json/data.json') as data_file:
		data = json.loads(data_file.read())
		if rgn.find('Metropolitana') != -1:
			rgn = 'Metropolitana'
		return data[rgn]

def nowt():
	utc = pytz.utc
	santiago = pytz.timezone('America/Santiago')
	dt = datetime.datetime.now()
	local_dt = santiago.localize(dt)
	utc_dt = utc.normalize(local_dt.astimezone(utc))
	santiago_dt =  santiago.normalize(utc_dt)
	return santiago_dt

def group(us,ps):
	now = nowt()
	arr,lt, js, oldch, sexch, isap, clinic, base_old, vali, pri = [], 0, {} ,'','','','','','',''
	for isa in vendor.objects.filter(user = us, psw = ps):
		isap = isa.isapre
		idv = isa.base
	for x in client.objects.filter(status="complete").order_by('date').reverse():
		for d in preference.objects.filter(base = x.base):
			if d.preference == isap:
				pri = 'pass'
		if pri == '':
			continue
		pri = ''
		if x.gr == '1':
			continue
		for cv in clients_vendor.objects.filter(id_vendor = idv, id_client = x.base):
			vali = 'notvalid'
		if vali == 'notvalid':
			vali = ''
			continue
		for bl in block.objects.filter(base = x.base, isapre = isap):
			vali = 'notvalid'
		if vali == 'notvalid':
			vali = ''
			continue
		if prefvalid(x.current, x.year) and int(x.it) < 7:
			for data in childrens.objects.filter(register=x.base):
				oldch += str(data.age)+' |'
				sexch += str(data.sex)+' |'
			if int(x.date.strftime("%Y")) > int(now.strftime("%Y")):
				oldch, sexch, clinic= '','',''
				base_old = x.base
				continue
			elif int(x.date.strftime("%m")) > int(now.strftime("%m")):
				oldch, sexch, clinic= '','',''
				base_old = x.base
				continue
			elif int(x.date.strftime("%m")) == int(now.strftime("%m")) and int(x.date.strftime("%d")) > int(now.strftime("%d")):
				oldch, sexch, clinic= '','',''
				base_old = x.base
				continue
			elif int(x.date.strftime("%m")) == int(now.strftime("%m")) and int(x.date.strftime("%H%M%S")) > int(now.strftime("%H%M%S")):
				oldch, sexch, clinic= '','',''
				base_old = x.base
				continue
			elif x.date.strftime("%d%m%Y") == now.strftime("%d%m%Y"):
				ddtt = 'Hoy, '+x.date.strftime("%H:%M")
			elif int(now.strftime("%d"))-int(x.date.strftime("%d")) == 1 and x.date.strftime("%m") == now.strftime("%m"):
				ddtt = 'Ayer, '+x.date.strftime("%H:%M")
			else:
				ddtt = x.date.strftime("%d de %b, %Y")
			if oldch == '':
				oldch = 'No tiene '
			if sexch == '':
				sexch = 'No tiene '
			base_old = x.base
			js = {'id':x.base,
				  'name':x.name,
				  'age': x.age,
				  'gender': x.gender.upper(),
				  'actual': x.current,
				  'oldchildren': oldch [:-1],
				  'sexchildren': sexch [:-1],
				  'inversion': x.investment,
				  'old': x.year,
				  'date': ddtt,
				  'cant': x.childrens,
				  'region': region(x.region),
				  'commune': x.commune.capitalize()}
			oldch, sexch, clinic= '','',''
			arr.append(js)
	if len(arr) == 0:
		return 'Sin clientes'
	return arr

def oldgroup(us,ps):
	now = nowt()
	arr,lt, js, oldch, sexch, isap, clinic, base_old, vali, pri = [], 0, {} ,'','','','','','',''
	for isa in vendor.objects.filter(user = us, psw = ps):
		isap = isa.isapre
		idv = isa.base
	for x in client.objects.filter(status="complete", gr = "0").order_by('date').reverse():
		for d in preference.objects.filter(base = x.base):
			if d.preference == isap:
				pri = 'pass'
		if pri == '':
			continue
		pri = ''
		if prefvalid(x.current, x.year):
			for data in childrens.objects.filter(register=x.base):
				oldch += str(data.age)+' |'
				sexch += str(data.sex)+' |'
			if int(x.date.strftime("%Y")) > int(now.strftime("%Y")):
				oldch, sexch, clinic= '','',''
				base_old = x.base
				continue
			if int(x.date.strftime("%m")) > int(now.strftime("%m")):
				oldch, sexch, clinic= '','',''
				base_old = x.base
				continue
			if int(x.date.strftime("%m")) == int(now.strftime("%m")) and int(x.date.strftime("%d")) > int(now.strftime("%d")):
				oldch, sexch, clinic= '','',''
				base_old = x.base
				continue
			if x.date.strftime("%d%m%Y") == now.strftime("%d%m%Y") and int(x.date.strftime("%H%M%S")) > int(now.strftime("%H%M%S")):
				oldch, sexch, clinic= '','',''
				base_old = x.base
				continue
			if int(now.strftime("%d"))-int(x.date.strftime("%d")) == 1 and x.date.strftime("%m") == now.strftime("%m"):
				ddtt = 'Ayer, '+x.date.strftime("%H:%M")
			else:
				ddtt = x.date.strftime("%d de %b, %Y")
			if x.date.strftime("%d%m%Y") == now.strftime("%d%m%Y"):
				ddtt = 'Hoy, '+x.date.strftime("%H:%M")
			if oldch == '':
				oldch = 'no tiene '
			if sexch == '':
				sexch = 'no tiene '
			if x.base == base_old:
				print 'repetido'
				oldch, sexch, clinic= '','',''
				continue
			base_old = x.base
			js = {'id':x.base,
				  'name':x.name,
				  'age': x.age,
				  'gender': x.gender.upper(),
				  'actual': x.current,
				  'oldchildren': oldch [:-1],
				  'sexchildren': sexch [:-1],
				  'inversion': x.investment,
				  'old': x.year,
				  'date': ddtt,
				  'cant': x.childrens,
				  'region': region(x.region),
				  'commune': x.commune.capitalize()}
			oldch, sexch, clinic= '','',''
			arr.append(js)
	print len(arr)
	if len(arr) == 0:
		return 'Sin clientes'
	return arr