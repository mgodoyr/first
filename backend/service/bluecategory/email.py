# -*- encoding: utf-8 -*-
from __future__ import absolute_import
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'service.settings'
os.environ['C_FORCE_ROOT'] = "true"

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from email.mime.text import MIMEText
import smtplib 
from bluecategory.celery import app
from django.core.exceptions import ImproperlyConfigured
from django.contrib.sites.models import Site
from bluecategory.models import *
import locale
# locale.setlocale( locale.LC_ALL, '' )

@app.task
def mail(base):
    try:
        subject = 'Nuevo cliente'    	
    	try:
            for cl in client.objects.filter(base=base):
                if cl.year == '+1':
                    fn = 'más de 1 año'
                elif cl.year == '-1':
                    fn = 'menos de 1 año'
                else:
                    fn = cl.year
                sex, age, inversion,current,year = cl.gender , cl.age, cl.investment, cl.current, fn
            chage,preferences,clinic = '','',''
            for c in childrens.objects.filter(register=base):
                if c.sex == ' no tiene' and c.age == ' no tiene':
                    chage += 'No tiene cargas  '
                else:
                    chage += c.sex+'/'+c.age+', '
            for p in preference.objects.filter(base=base):
                preferences += p.preference+', '
            for c in clinics.objects.filter(base=base):
                clinic += c.clinic+', '
            htmly = get_template('newclient.html')
            from_email = '"primerocotiza.cl" <contacto@primerocotiza.cl>'
            for x in vendor.objects.values('email','isapre','mail_send'):
                for vn in vendor.objects.filter(email=x['email']):
                    name = vn.name
                text_content = 'Estimado: '+name
                d = Context({ 'username': name, 
                              'sex':sex.upper(), 
                              'age':age,
                              'chage':chage [:-2], 
                              'preference':preferences [:-2],
                              'clinic':clinic [:-2],
                              'inversion': locale.currency( int(inversion), grouping=True ) [:-3],
                              'current':current,
                              'year':year})
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
		
			


 
