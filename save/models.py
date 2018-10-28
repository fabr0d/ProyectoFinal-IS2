from django.db import models

# Create your models here.
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
	tema = models.IntegerField(default=0)
	moneda = models.CharField(max_length=5)
	tipoDeCuenta = models.IntegerField(default=0)
	def autenticar(email,contra):
		user=Usuario.objects.filter(correoElectronico=email)
		if len(user)==0:
			return False
		if contra==user[0].contrasena :
			return True
		else:
			return False
	def verificarExistencia(email):
		user=Usuario.objects.filter(correoElectronico=email)
		if len(user)==0:
			return True
		else:
			return False
	def registrar(email,contra):
		user=Usuario(correoElectronico=email, contrasena=contra,tema=0,moneda="$",tipoDeCuenta=0)
		user.save()
	def conseguirUsuario(email_):
		return (Usuario.objects.get(correoElectronico=email_)).pk
class Ingreso(models.Model):
	fecha = models.DateTimeField()
	nombre = models.CharField(max_length=50)
	monto = models.DecimalField(decimal_places=2,max_digits=20)
	id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
	def anadirIngreso(fecha_,nombre_,monto_,user_):
		user=Usuario.objects.get(pk=user_)
		ingreso=Ingreso(fecha=fecha_,nombre=nombre_,monto=monto_,id_usuario=user)
		ingreso.save()
	def editarIngreso(fecha_,nombre_,monto_,user_,ingreso_id):
		ingreso=Ingreso.objects.get(pk=ingreso_id)
		ingreso.fecha=fecha_
		ingreso.nombre=nombre_
		ingreso.monto=monto_
		ingreso.save()
	def obtenerIngresos(user):#conseguir todos los ingresos de user
		transacciones=Ingreso.objects.filter(id_usuario=user)
		return transacciones
	def conseguirIngreso(ingreso_id):#conseguir el ingreso con id= ingreso_id
		return Ingreso.objects.get(pk=ingreso_id)

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