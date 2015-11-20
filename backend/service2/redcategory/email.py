# -*- encoding: utf-8 -*-
from __future__ import absolute_import
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'service2.settings'
os.environ['C_FORCE_ROOT'] = "true"

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from email.mime.text import MIMEText
import smtplib 
from redcategory.celery import app
from django.core.exceptions import ImproperlyConfigured
from django.contrib.sites.models import Site
from redcategory.models import *
import locale
locale.setlocale( locale.LC_ALL, '' )

@app.task
def mail(base):
    try:
        subject = 'Nuevo cliente'    	
    	try:
            for cl in client.objects.filter(base=base):
                sex, age, typemath,math = cl.gender , cl.age, cl.typemath, cl.math
            chage,preferences,clinic = '','',''
            htmly = get_template('newclientL.html')
            from_email = '"primerocotiza.cl" <contacto@primerocotiza.cl>'
            for x in vendor.objects.values('email','isapre','mail_send'):
                for vn in vendor.objects.filter(email=x['email']):
                    name = vn.name
                text_content = 'Estimado: '+name
                d = Context({ 'username': name, 
                              'sex':sex.upper(), 
                              'age':age,
                              'math':math})
                html_content = htmly.render(d)
                to = x['email']
                msg = EmailMultiAlternatives(subject,text_content,from_email,[to])
                msg.attach_alternative(html_content, "text/html")
                if preferences.find(x['isapre']) >= 0 and current != x['isapre'] and x['mail_send']=='1':
                    msg.send()
                    print "Correo enviado"
    	except ValueError: 
            print ValueError
    except ValueError:
    	print ValueError
		
			


 
