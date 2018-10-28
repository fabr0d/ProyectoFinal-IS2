from django.http import HttpResponse
from django.shortcuts import render,redirect

from save.models import Usuario,Ingreso,Egreso,Categoria

def index(request):
	return HttpResponse("index")

class iniciarSesionControlador:	
	def iniciarSesion(request):
		try:
		    email=request.POST['email']
		    contra=request.POST['password']
		except:
			return render(request, 'save/iniciarSesionVista.html')
		if Usuario.autenticar(email,contra):
			request.session['user'] = Usuario.conseguirUsuario(email)
			return redirect('inicio')
		else:
			#MostrarMensaje("Error de inicio de sesion")
			return render(request, 'save/iniciarSesionVista.html',{'error':"Error de inicio de sesion"})


#funcion validar
class registrarControlador:
	def registrar(request):
		try:
		    email=request.POST['email']
		    contra1=request.POST['password1']
		    contra2=request.POST['password2']
		except:
			return render(request, 'save/registrarVista.html')

		if contra1==contra2:#validar(contra1,contra2) 
			if Usuario.verificarExistencia(email):
				Usuario.registrar(email,contra1)
				#redireccionar iniciarSesion
				return render(request, 'save/iniciarSesionVista.html')
			else:
				#MostrarMensaje("El correo esta en uso")
				return render(request, 'save/registrarVista.html',{'error':"El correo esta en uso"})
		else:
			#MostrarMensaje("reingrese las contraseñas")
			return render(request, 'save/registrarVista.html',{'error':"Reingrese las contraseñas"})

def inicio(request):	
	return render(request,'save/inicioVista.html')

class registrarIngresoControlador:
	def anadirIngreso(request):
		try:
		    fecha=request.POST['fecha']
		    nombre=request.POST['nombre']
		    monto=request.POST['monto']
		    user=request.session['user']
		except:

			return render(request, 'save/registrarIngresoVista.html')
		#verificarDatos(fecha,nombre,monto)
		if len(nombre) <= 50 and float(monto) > 0:
			Ingreso.anadirIngreso(fecha,nombre,monto,user)
			return render(request, 'save/registrarIngresoVista.html',{'error':"Ingreso exitoso"})
		else:
			return render(request, 'save/registrarIngresoVista.html',{'error':"Reingrese datos ingreso"})
		
class registrarEgresoControlador:
	def anadirEgreso(request):
		categorias=Categoria.objects.all()#conseguirCategorias
		try:
		    fecha=request.POST['fecha']
		    nombre=request.POST['nombre']
		    monto=request.POST['monto']
		    categoria=request.POST['categoria']
		    user=request.session['user']
		except:
			return render(request, 'save/registrarEgresoVista.html',{'categorias':categorias})
		#verificarDatos(fecha,nombre,monto,categoria)
		if len(nombre) <= 50 and float(monto) > 0:
			Egreso.anadirEgreso(fecha,nombre,monto,categoria,user)
			return render(request, 'save/registrarEgresoVista.html',{'error':"Egreso exitoso",'categorias':categorias})
		else:
			return render(request, 'save/registrarEgresoVista.html',{'error':"Reingrese datos Egreso",'categorias':categorias})

class verListadoControlador:
	def verListadoIngresos(request):
		user=request.session['user']
		transacciones=Ingreso.obtenerIngresos(user) #obtener todos los ingresos de user
		try:
		    ingreso_id=request.POST['transaccion'] 
		except:
			return render(request, 'save/verListadoIngresoVista.html',{'transacciones':transacciones}) #mostrar los ingresos
		
		ingreso=Ingreso.conseguirIngreso(ingreso_id)
		request.session['tmp'] = ingreso_id
		return render(request, 'save/editarIngresoVista.html',{'ingreso':ingreso})#editarIngreso(ingreso)

	def editarIngreso(request):
		#conseguir todos los parametros del form de la vista
		fecha=request.POST['fecha']
		nombre=request.POST['nombre']
		monto=request.POST['monto']
		ingreso_id=request.session['tmp']
		user=request.session['user']
		if len(nombre) <= 50 and float(monto) > 0: 
			Ingreso.editarIngreso(fecha,nombre,monto,user,ingreso_id)#editar el ingreso en la base de datos
			transacciones=Ingreso.obtenerIngresos(user) #se cambiaron datos, obtener todos los ingresos de user
			return render(request, 'save/verListadoIngresoVista.html',{'error':"Ingreso editado",'transacciones':transacciones})#mostrarMensaje("Ingreso editado")
		else:
			ingreso=Ingreso.objects.get(pk=ingreso_id)#deberia hacerse en bd
			return render(request, 'save/editarIngresoVista.html',{'ingreso':ingreso, 'error':"Corrija datos ingreso"})

	def verListadoEgresos(request):
		user=request.session['user']
		transacciones=Egreso.obtenerEgresos(user) #obtener todos los egresos de user
		try:
		    egreso_id=request.POST['transaccion']
		except:
			return render(request, 'save/verListadoEgresoVista.html',{'transacciones':transacciones}) #mostrar los egresos
		egreso=Egreso.conseguirEgreso(egreso_id)
		request.session['tmp'] = egreso_id
		categorias=Categoria.obtenerTodo()#conseguir todas las categorias
		return render(request, 'save/editarEgresoVista.html',{'egreso':egreso,'categorias':categorias})#editarEgreso(egreso,categorias)
		
	def editarEgreso(request):
		#conseguir todos los parametros del form de la vista
		fecha=request.POST['fecha']
		nombre=request.POST['nombre']
		monto=request.POST['monto']
		categoria=request.POST['categoria']
		egreso_id=request.session['tmp']
		user=request.session['user']
		Egreso.editarEgreso(fecha,nombre,monto,categoria,user,egreso_id)#editar el egreso en la base de datos
		transacciones=Egreso.obtenerEgresos(user) #se cambiaron datos, obtener todos los egresos de user

		return render(request, 'save/verListadoEgresoVista.html',{'error':"Egreso editado",'transacciones':transacciones})#mostrarMensaje("Egreso editado")
