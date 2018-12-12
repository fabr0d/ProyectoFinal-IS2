from django.db import models
from django.db.models import Avg, Count, Min, Sum
from decimal import *
from datetime import timedelta
import datetime


class Question(models.Model):
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')

class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)

class Usuario(models.Model):
	correoElectronico = models.CharField(max_length=50)
	contrasena = models.CharField(max_length=50)
	tipoDeCuenta = models.IntegerField(default=0)
	ahorro = models.DecimalField(decimal_places=2,max_digits=20,default=0)
	def existeUsuario(email,contra):
		user=Usuario.objects.filter(correoElectronico=email)
		if len(user)==0:
			return False
		if contra==user[0].contrasena :
			return True
		else:
			return False
	def existeEmail(email):
		user=Usuario.objects.filter(correoElectronico=email)
		if len(user)==0:
			return False
		else:
			return True
	def registrar(email,contra):
		user=Usuario(correoElectronico=email, contrasena=contra,tipoDeCuenta=0,ahorro=0)
		user.save()
		todasCategorias=Categoria.objects.all()
		for cat in todasCategorias:
			tmp=ControlEgreso(monto=0,id_usuario=user,id_categoria=cat)
			tmp.save()
	def conseguirUsuario(email_):
		return (Usuario.objects.get(correoElectronico=email_)).pk
	def aumentarAhorro(monto_,user_):
		user=Usuario.objects.get(pk=user_)
		user.ahorro=user.ahorro+Decimal(monto_)
		user.save()
	def disminuirAhorro(monto_,user_):
		user=Usuario.objects.get(pk=user_)
		if user.ahorro >= float(monto_):
			user.ahorro=user.ahorro-Decimal(monto_)
			user.save()
			return True
		else:
			return False
	def reemplazarAhorro(user_,antiguo_ahorro,nuevo_ahorro):
		user=Usuario.objects.get(pk=user_)
		diferencia=Decimal(nuevo_ahorro) - Decimal(antiguo_ahorro)
		user.ahorro=user.ahorro + Decimal(diferencia)
		user.save()
class Ingreso(models.Model):
	fecha = models.DateTimeField()
	nombre = models.CharField(max_length=50)
	monto = models.DecimalField(decimal_places=2,max_digits=20)
	ahorro = models.DecimalField(decimal_places=2,max_digits=20,default=0)
	id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
	def anadirIngreso(fecha_,nombre_,monto_,ahorro_,user_):
		user=Usuario.objects.get(pk=user_)
		ingreso=Ingreso(fecha=fecha_,nombre=nombre_,monto=monto_,ahorro=ahorro_,id_usuario=user)
		ingreso.save()
	def editarIngreso(fecha_,nombre_,monto_,ahorro_,user_,ingreso_id):
		ingreso=Ingreso.objects.get(pk=ingreso_id)
		ingreso.fecha=fecha_
		ingreso.nombre=nombre_
		ingreso.monto=monto_
		ingreso.ahorro=ahorro_
		ingreso.save()
	def obtenerIngresos(user):#conseguir todos los ingresos de user
		transacciones=Ingreso.objects.filter(id_usuario=user)
		return transacciones
	def conseguirIngreso(ingreso_id):#conseguir el ingreso con id= ingreso_id
		return Ingreso.objects.get(pk=ingreso_id)
	def obtenerAhorro(ingreso_id):#conseguir el ahorro de un ingreso con el ingreso_id
		ingreso=Ingreso.objects.get(pk=ingreso_id)
		return ingreso.ahorro
		
class Categoria(models.Model):
	nombre = models.CharField(max_length=20)
	def obtenerTodo():
		return Categoria.objects.all()

class Egreso(models.Model):
	fecha = models.DateTimeField()
	nombre = models.CharField(max_length=50)
	monto = models.DecimalField(decimal_places=2,max_digits=20)
	id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
	id_categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
	def anadirEgreso(fecha_,nombre_,monto_,categoria_,user_):
		user=Usuario.objects.filter(pk=user_)
		cat=Categoria.objects.filter(pk=categoria_)
		egreso=Egreso(fecha=fecha_,nombre=nombre_,monto=monto_,id_usuario=user[0],id_categoria=cat[0])
		egreso.save()
	def editarEgreso(fecha_,nombre_,monto_,categoria_,user_,egreso_id):
		cat=Categoria.objects.filter(pk=categoria_)
		egreso=Egreso.objects.get(pk=egreso_id)
		egreso.fecha=fecha_
		egreso.nombre=nombre_
		egreso.monto=monto_
		egreso.id_categoria=cat[0]
		egreso.save()
	def obtenerEgresos(user):
		return Egreso.objects.filter(id_usuario=user)
	def conseguirEgreso(egreso_id):
		return Egreso.objects.get(pk=egreso_id)
	def obtenerMontosUsadosPorCategoria(user):
		hoy=datetime.datetime.today()
		mesactual=datetime.datetime(hoy.year,hoy.month,1)
		resultado = Egreso.objects.filter(id_usuario=user,).filter(fecha__gte=mesactual).select_related('id_categoria', 'id_usuario').values('id_categoria__nombre','id_categoria_id').annotate(score = Sum('monto'))
		l=list(resultado)
		l1=list()
		#poblar l1 con ceros
		for i in Categoria.objects.all():
			l1.append({'id_categoria__nombre': i.nombre, 'id_categoria_id': i.pk, 'score': Decimal('0')})
		#copiar no-ceros de l a l1
		for i in l1:
			for j in l:
				if i.get('id_categoria_id')==j.get('id_categoria_id'):
					i['score']=j['score']
		return l1
	def obtenerEgresosCategoria(user,fecha,periodo):
		if periodo=="dia":
			inicio=datetime.datetime(fecha.year,fecha.month,fecha.day)
			fin=inicio+timedelta(days=1)
		if periodo=="mes":
			inicio=datetime.datetime(fecha.year,fecha.month,1)
			if fecha.month % 12==0:
				fin=datetime.datetime(fecha.year+1,(fecha.month % 12 + 1),1)
			else:
				fin=datetime.datetime(fecha.year,(fecha.month % 12 + 1),1)
		if periodo=="anio":
			inicio=datetime.datetime(fecha.year,1,1)
			fin=datetime.datetime(fecha.year+1,1,1)
		resultado = Egreso.objects.filter(id_usuario=user,).filter(fecha__gte=inicio).filter(fecha__lt=fin).select_related('id_categoria', 'id_usuario').values('id_categoria__nombre','id_categoria_id').annotate(score = Sum('monto'))
		l=list(resultado)
		l1=list()
		#poblar l1 con ceros
		for i in Categoria.objects.all():
			l1.append({'id_categoria__nombre': i.nombre, 'id_categoria_id': i.pk, 'score': Decimal('0')})
		#copiar no-ceros de l a l1
		for i in l1:
			for j in l:
				if i.get('id_categoria_id')==j.get('id_categoria_id'):
					i['score']=j['score']
		return l1

class ControlEgreso(models.Model):
	monto = models.DecimalField(decimal_places=2,max_digits=20)
	id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
	id_categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
	def obtenerMontosUsar(user):
		return ControlEgreso.objects.filter(id_usuario=user)
	def actualizarMontoUsar(user,categ,monto_):
		idCateg=Categoria.objects.get(nombre=categ).pk
		aEditar=ControlEgreso.objects.filter(id_usuario=user).get(id_categoria=idCateg)
		aEditar.monto=monto_
		aEditar.save()