from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import json, base64, time, sys, re
from .models import *
from django.db.models import Sum
from django.core.mail import EmailMultiAlternatives
from django.core import serializers
from django.core.exceptions import MultipleObjectsReturned
from redcategory.email import mail
from redcategory.groups import group, oldgroup
from django.template.loader import get_template
from django.template import Context
import datetime, time, pytz
from django.utils import timezone



class charge():
	@staticmethod
	@csrf_exempt
	def rbt(request):
		if request.method == 'POST':
			for x in request:
				value = json.loads(x)
			print value
			vendor.objects.filter(email = value['email']).update(robot="view")
			return HttpResponse('Revisado')
		else:
			return redirect('http://primerocotiza.cl/')



class bag():
	@staticmethod
	@csrf_exempt
	def data(request):
		if request.method == 'POST':
			for x in request:
				value = json.loads(x)
			base_old = ''
			arr , oldch, sexch= [],'',''
			for vr in vendor.objects.filter(user = value['user'], psw= value['psw']):
				bs = vr.base
			for ven in clients_vendor.objects.filter(id_vendor=bs).order_by('id').reverse():
				for cl in client.objects.filter(base=ven.id_client):
					js = {
						'id': cl.base,
						'date': ven.date.strftime("%d de %b,%Y"),
						'name': cl.name.capitalize(),
						'phone': cl.phone,
						'email': cl.email,
						'gender': cl.gender.upper(),
						'age': cl.age,
						'type': cl.typemath
						
					}
					arr.append(js)
			if len(arr) == 0:
				return HttpResponse('Sin clientes')
			return HttpResponse(json.dumps(arr), content_type = "application/json") 
		else:
			return redirect('http://primerocotiza.cl/')

class login():
	@staticmethod
	@csrf_exempt
	def validator(request):
		if request.method == 'POST':
			for x in request:
				vl = json.loads(x)
			user = vl['user']
			psw = vl['psw']
			value = vendor.objects.filter(user=user, psw = psw)
			response = []
			if value:
				vendor_id = vendor.objects.get(user=user, psw = psw)
				if vendor_id.validate != "1":
					return HttpResponse ('Usuario no validado')
				response.append(vendor_id.name)
				response.append(vendor_id.coins_avaiable)
				response.append(vendor_id.base)
				response.append(vendor_id.gr)
				response.append(vendor_id.link)
				return HttpResponse(json.dumps(response), content_type = "application/json")
			else:
				return HttpResponse("Usuario no registrado")
		else:
			return redirect('http://primerocotiza.cl/')


class table():

	@staticmethod
	@csrf_exempt
	def data(request):
		if request.method=='POST':
			try:
				for x in request:
					vl = json.loads(x)
				usr, ps, base_old = vl['user'], vl['psw'], ''
				for vnd in vendor.objects.filter(user=usr, psw = ps):
					indi = vnd.gr
				if indi == '2':
					arr = group(usr,ps)
				if indi == '1':
					arr = oldgroup(usr,ps)
				if arr == 'Sin clientes':
					return HttpResponse(arr)
				return HttpResponse(json.dumps(arr), content_type = "application/json")
			except IndexError:
				print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
				if arr == 'Sin clientes':
					return HttpResponse(arr)
				return HttpResponse(json.dumps(arr), content_type = "application/json")
		else:
			return redirect('http://primerocotiza.cl/')

	

		
		
class confirmation():
	@staticmethod
	@csrf_exempt
	def user(request):
		if request.method == 'POST':
			return redirect('http://primerocotiza.cl/')
		if request.method == 'GET':
			try:
				value = request.GET['value']
				if vendor.objects.filter(base_login=value):
					vendor.objects.filter(base_login=value).update(validate="1")
					return redirect("http://primerocotiza.cl/bienvenido")
				else:
					return redirect("http://primerocotiza.cl/opps")
			except ValueError:
				return redirect("http://primerocotiza.cl/opps")

class register():
	@staticmethod
	@csrf_exempt
	def user(request):
		if request.method == 'POST':
			try:
				for x in request:
					value = json.loads(x)
				if vendor.objects.filter(user= value['form']['user'], email=value['form']['email']):
					return HttpResponse('ya existe')
				vendor.objects.create (
				base = value['id'],
				base_login = value['param'],
				name = value['form']['name'],
				phone = value['form']['phone'],
				email = value['form']['email'],
				user = value['form']['user'],
				psw = value['form']['psw']
				)
				subject = 'Registro Primero Cotiza'
				text_content = 'Estimado: '+value['form']['name']
				htmly = get_template('emailregistro.html')
				d = Context({'port':'8600', 'username': value['form']['name'], 'user':value['form']['user'], 'psw':value['form']['psw'] ,'email':value['form']['email'], 'base':value['param']})
				html_content = htmly.render(d)
				from_email = '"primerocotiza.cl" <contacto@primerocotiza.cl>'
				to = value['form']['email']
				msg = EmailMultiAlternatives(subject,text_content,from_email,[to])
				msg.attach_alternative(html_content, "text/html")
				msg.send()
				return HttpResponse('registrado')
			except ValueError:
				return ("error del servidor")
		else:
			return redirect('http://primerocotiza.cl/')
		
class formularios():
	@staticmethod
	@csrf_exempt
	def list(request):
		if request.method == 'POST':
			try:
				for x in request:
					value = json.loads(x)
				if value['step'] == "1":
					if client.objects.filter(base=value['id']):
						return HttpResponse('ya existe')
					client.objects.create(
						base = value['id'],
						name = value['form']['name'],
						phone = value['form']['phone'],
						email = value['form']['email']
						)
					return HttpResponse('Form1 cargado')
				elif value['step'] == "2":
					client.objects.filter(base=value['id']).update(
						region = value['region'],
						commune = value['commune'],
						gender = value['form']['gender'],
						age = value['form']['age']
						)
					return HttpResponse('Form2 cargado')
				else:
					client.objects.filter(base=value['id']).update(
						typemath = value['forms']['typemath'],
						math = value['forms']['math']
						)
					mail.delay(value['id'])
					return HttpResponse('Form3 cargado')
			except ValueError:
				arr = ValueError.__doc__
				return HttpResponse(arr)
		else:
			return redirect('http://primerocotiza.cl/')

	


class real_time():
	@staticmethod
	@csrf_exempt
	def form_client(request):
		if request.method == 'POST':
			return HttpResponse('new')
		else:
			return redirect('http://primerocotiza.cl/')

class first():
	@staticmethod
	@csrf_exempt
	def region(rgn):
		with open('/backend/json/data.json') as data_file:
			data = json.loads(data_file.read())
			if rgn.find('Metropolitana') != -1:
				rgn = 'Metropolitana'
			return data[rgn]


	@staticmethod
	@csrf_exempt
	def data(request):
		if request.method == 'POST':
			for x in request:
				value = json.loads(x)
			cargas, pre = [],[]
			for c in client.objects.filter(base = value['id_client']):
				if c.gender == 'm':
					gr = 'Hombre'
				else:
					gr = 'Mujer'
				arr = [
					c.date.strftime('%d de %b, %Y'),
					gr,
					c.age,
					c.commune,
					first.region(c.region),
					c.typemath
				]
			return HttpResponse(json.dumps(arr), content_type = "application/json")
		else:
			return redirect('http://primerocotiza.cl/')



class details():
	@staticmethod
	@csrf_exempt
	def region(rgn):
		with open('/backend/json/data.json') as data_file:
			data = json.loads(data_file.read())
			if rgn.find('Metropolitana') != -1:
				rgn = 'Metropolitana'
			return data[rgn]


	@staticmethod
	@csrf_exempt
	def data(request):
		if request.method == 'POST':
			for x in request:
				value = json.loads(x)
			cargas, preferencias = [],[]
			for c in client.objects.filter(base = value['id_client']):
				if c.gender == 'm':
					gr = 'Hombre'
				else:
					gr = 'Mujer'
				arr = [
					c.date.strftime('%d de %b, %Y'),
					gr,
					c.age,
					c.commune,
					details.region(c.region),
					c.typemath,
					c.math,
					c.name,
					c.phone,
					c.email

				]
			return HttpResponse(json.dumps(arr), content_type = "application/json")
		else:
			return redirect('http://primerocotiza.cl/')

class coins():
	@staticmethod
	@csrf_exempt
	def data(request):
		if request.method == 'POST':
			for x in request:
				value = json.loads(x)
			for d in vendor.objects.filter(user=value['user'], psw = value['psw']):
				coins = d.coins_avaiable
			return HttpResponse(coins)
		else:
			return redirect('http://primerocotiza.cl/')
		



class buy():
	@staticmethod
	@csrf_exempt
	def new(request):
		if request.method == 'POST':
			for x in request:
				value = json.loads(x)
			if clients_vendor.objects.filter(id_vendor=value['id_vendor'], id_client = value['id_client']):
				return HttpResponse('revisa')
			for dt in vendor.objects.filter(base= value['id_vendor']):
				curr = dt.isapre
				if dt.coins_avaiable == '0':
					return HttpResponse('Sin coins')
			for bl in block.objects.filter(base = value['id_client'],isapre = curr):
				return HttpResponse('Full')
			arr = []
			for v in vendor.objects.filter(base = value['id_vendor']):
				co = v.coins_avaiable
				cu = v.coins_used
				gru = v.gr
			if gru == '1':
				itt = '7'
			elif gru == '2':
				for cle in client.objects.filter(base=value['id_client']):
					itt = cle.it
				if int(itt) < 7:
					itt = int(itt)+1
					itt = str(itt)
				elif int(itt) == 7:
					return HttpResponse('Full')
				else: 
					blue = 'kfsd'
			else:
				hfh= 'sdkfn'
			clients_vendor.objects.create(
				id_vendor = value['id_vendor'],
				id_client = value['id_client']
				)
			block.objects.create(
				base = value['id_client'],
				isapre = curr
				)
			client.objects.filter(base=value['id_client']).update(buy='1', gr= gru, it= itt)
			newco, newcou= int(co) -1, int(cu) +1
			vendor.objects.filter(base= value['id_vendor']).update(coins_avaiable= str(newco), coins_used=str(newcou))
			for c in  client.objects.filter(base=value['id_client']):
				js = {
				'name': c.name,
				'phone': c.phone,
				'email': c.email
				}
			arr.append(js)
			return HttpResponse(json.dumps(arr), content_type = "application/json")
		else:
			return redirect('http://primerocotiza.cl/')


class avaiable():
	@staticmethod
	@csrf_exempt
	def data(request):
		if request.method == 'POST':
			for x in request:
				value = json.loads(x)
			for v in vendor.objects.filter(base = value['id_vendor']):
				co = v.coins_avaiable
			if co == '0':
				return HttpResponse('Sin coins')
			for c in client.objects.filter(base = value['id_client']):
				cl = c.it
			if cl == '7':
				return HttpResponse('Cliente no disponible')
			elif cl != '7':
				return HttpResponse('Cliente disponible')
			else:
				return HttpResponse('Salir')
		else:
			return redirect('http://primerocotiza.cl/')


		

# Create your views here.
