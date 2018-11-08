from django.http import HttpResponse
from django.shortcuts import render,redirect

from save.models import Usuario,Ingreso,Egreso,Categoria

def index(request):
	return HttpResponse("index")

class Vista_IniciarSesion:	
	def iniciarSesion(request):
		try:
		    email=request.POST['email']
		    contra=request.POST['password']
		except:
			if 'user' in request.session:
				del request.session['user']
			return render(request, 'save/Plantilla_IniciarSesion.html')
		if Usuario.existeEmail(email):
			if Usuario.existeUsuario(email,contra):
				request.session['user'] = Usuario.conseguirUsuario(email)#guardar el id del usuario en la sesion
				return redirect('inicio')#ir a pagina inicio
			else:
				#mostrarErrorContrasenaInvalida()
				return render(request, 'save/Plantilla_IniciarSesion.html',{'error':"Contraseña inválida"})
		else:
			#mostrarErrorEmaiInvalido()
			return render(request, 'save/Plantilla_IniciarSesion.html',{'error':"Email Inválido"})

class Vista_Registrar:
	def registrar(request):
		try:
		    email=request.POST['email']
		    contra1=request.POST['password1']
		    contra2=request.POST['password2']
		except:
			return render(request, 'save/Plantilla_Registrar.html')

		if contra1==contra2:#validar(contra1,contra2) 
			if Usuario.existeEmail(email):
				#MostrarErrorCorreoEnUso()
				return render(request, 'save/Plantilla_Registrar.html',{'error':"El correo esta en uso"})
			else:
				Usuario.registrar(email,contra1)
				#irAPagIniciarSesion()
				return render(request, 'save/Plantilla_IniciarSesion.html')
		else:
			#MostrarErrorContrasenasNoIguales()
			return render(request, 'save/Plantilla_Registrar.html',{'error':"Contraseñas no iguales"})

def inicio(request):	
	return render(request,'save/inicioVista.html')

class Vista_RegistrarIngreso:
	def verificarNombre(nombre):
		if len(nombre)<=50:
			return True
		else:
			return False
	def verificarMonto(monto):
		if float(monto)>0:
			return True
		else:
			return False
	def verificarAhorro(ahorro,monto):
		if float(ahorro)>0 and float(ahorro)<=float(monto):
			return True
		else:
			return False
	def anadirIngreso(request):
		try:
		    fecha=request.POST['fecha']
		    nombre=request.POST['nombre']
		    monto=request.POST['monto']
		    ahorro=request.POST['ahorro']
		    user=request.session['user']
		except:
			return render(request, 'save/Plantilla_RegistrarIngreso.html')
		if Vista_RegistrarIngreso.verificarNombre(nombre):
			if Vista_RegistrarIngreso.verificarMonto(monto):
				if Vista_RegistrarIngreso.verificarAhorro(ahorro,monto):
					Ingreso.anadirIngreso(fecha,nombre,monto,ahorro,user)
					Usuario.aumentarAhorro(ahorro,user)
					#mostrarMensajeIngresoAnadido()
					return render(request, 'save/Plantilla_RegistrarIngreso.html',{'error':"Ingreso añadido"})
				else:
					#mostrarErrorAhorrroInvalido()
					return render(request, 'save/Plantilla_RegistrarIngreso.html',{'error':"Ahorro inválido"})
			else:
				#mostrarErrorMontoInvalido()
				return render(request, 'save/Plantilla_RegistrarIngreso.html',{'error':"Monto inválido"})
		else:
			#mostrarErrorNombreInvalido()
			return render(request, 'save/Plantilla_RegistrarIngreso.html',{'error':"Nombre inválido"})

class Vista_RegistrarEgreso:
	def verificarNombre(nombre):
		if len(nombre)<=50:
			return True
		else:
			return False
	def verificarMonto(monto):
		if float(monto)>0:
			return True
		else:
			return False
	def anadirEgreso(request):
		categorias=Categoria.objects.all()#conseguirCategorias
		try:
		    fecha=request.POST['fecha']
		    nombre=request.POST['nombre']
		    monto=request.POST['monto']
		    categoria=request.POST['categoria']
		    user=request.session['user']
		except:
			return render(request, 'save/Plantilla_RegistrarEgreso.html',{'categorias':categorias})

		if Vista_RegistrarEgreso.verificarNombre(nombre):
			if Vista_RegistrarEgreso.verificarMonto(monto):
				if Categoria.objects.get(pk=categoria).nombre=="Ahorro":#si categoria es ahorro
					if Usuario.disminuirAhorro(monto,user):
						Egreso.anadirEgreso(fecha,nombre,monto,categoria,user)
						#mostrarMensajeEgresoAnadido()
						return render(request, 'save/Plantilla_RegistrarEgreso.html',{'error':"Egreso añadido",'categorias':categorias})
					else:
						#mostrarErrorNoExisteAhorroParaQuitar()
						return render(request, 'save/Plantilla_RegistrarEgreso.html',{'error':"No existe ahorro para quitar",'categorias':categorias})
				else:
					Egreso.anadirEgreso(fecha,nombre,monto,categoria,user)
					#mostrarMensajeEgresoAnadido()
					return render(request, 'save/Plantilla_RegistrarEgreso.html',{'error':"Egreso añadido",'categorias':categorias})
			else:
				#mostrarErrorMontoInvalido()	
				return render(request, 'save/Plantilla_RegistrarEgreso.html',{'error':"Monto inválido",'categorias':categorias})
		else:
			#mostrarErrorNombreInvalido()
			return render(request, 'save/Plantilla_RegistrarEgreso.html',{'error':"Nombre inválido",'categorias':categorias})

class Vista_VerListado:
	def verificarNombre(nombre):
		if len(nombre)<=50:
			return True
		else:
			return False
	def verificarMonto(monto):
		if float(monto)>0:
			return True
		else:
			return False
	def verificarAhorro(ahorro,monto):
		if float(ahorro)>0 and float(ahorro)<=float(monto):
			return True
		else:
			return False
	def verListadoIngresos(request):
		user=request.session['user']
		transacciones=Ingreso.obtenerIngresos(user) #obtener todos los ingresos de user
		try:
		    ingreso_id=request.POST['transaccion'] 
		except:
			return render(request, 'save/Plantilla_VerListadoIngreso.html',{'transacciones':transacciones}) #mostrar los ingresos
		
		ingreso=Ingreso.conseguirIngreso(ingreso_id)
		request.session['tmp'] = ingreso_id
		#mostrar la plantilla de editar ingreso con todos los valores de el ingreso seleccionado
		return render(request, 'save/Plantilla_EditarIngreso.html',{'ingreso':ingreso})

	def editarIngreso(request):
		fecha=request.POST['fecha']
		nombre=request.POST['nombre']
		monto=request.POST['monto']
		ahorro=request.POST['ahorro']
		ingreso_id=request.session['tmp']
		user=request.session['user']
		ingreso=Ingreso.objects.get(pk=ingreso_id)#deberia hacerse en bd
		if Vista_RegistrarIngreso.verificarNombre(nombre):
			if Vista_RegistrarIngreso.verificarMonto(monto):
				if Vista_RegistrarIngreso.verificarAhorro(ahorro,monto):
					antiguoAhorro=Ingreso.obtenerAhorro(ingreso_id)
					Ingreso.editarIngreso(fecha,nombre,monto,ahorro,user,ingreso_id)#editar el ingreso en la base de datos
					Usuario.reemplazarAhorro(user,antiguoAhorro,ahorro)
					transacciones=Ingreso.obtenerIngresos(user) #se cambiaron datos, obtener todos los ingresos de user		
					return render(request, 'save/Plantilla_VerListadoIngreso.html',{'error':"Ingreso editado",'transacciones':transacciones})#mostrarMensaje("Ingreso editado")
				else:
					#mostrarErrorAhfnoorrroInvalidoIngreso()
					return render(request, 'save/Plantilla_EditarIngreso.html',{'ingreso':ingreso, 'error':"Ahorro inválido"})
			else:
				#mostrarErrorMontoInvalidoIngreso()
				return render(request, 'save/Plantilla_EditarIngreso.html',{'ingreso':ingreso, 'error':"Monto inválido"})
		else:
			#mostrarErrorNombreInvalidoIngreso()
			return render(request, 'save/Plantilla_EditarIngreso.html',{'ingreso':ingreso, 'error':"Nombre inválido"})

	def verListadoEgresos(request):
		user=request.session['user']
		transacciones=Egreso.obtenerEgresos(user) #obtener todos los egresos de user
		try:
		    egreso_id=request.POST['transaccion']
		except:
			return render(request, 'save/Plantilla_VerListadoEgreso.html',{'transacciones':transacciones}) #mostrar los egresos
		egreso=Egreso.conseguirEgreso(egreso_id)
		request.session['tmp'] = egreso_id
		categorias=Categoria.obtenerTodo()#conseguir todas las categorias
		#mostrar la plantilla de editar egreso con todos los valores de el egreso seleccionado
		return render(request, 'save/Plantilla_EditarEgreso.html',{'egreso':egreso,'categorias':categorias})#editarEgreso(egreso,categorias)
		
	def editarEgreso(request):
		#conseguir todos los parametros del form de la vista
		fecha=request.POST['fecha']
		nombre=request.POST['nombre']
		monto=request.POST['monto']
		categoria=request.POST['categoria']
		egreso_id=request.session['tmp']
		user=request.session['user']
		egreso=Egreso.conseguirEgreso(egreso_id)
		categorias=Categoria.objects.all()#conseguirCategorias
		if Vista_RegistrarEgreso.verificarNombre(nombre):
			if Vista_RegistrarEgreso.verificarMonto(monto):
				Egreso.editarEgreso(fecha,nombre,monto,categoria,user,egreso_id)#editar el egreso en la base de datos
				transacciones=Egreso.obtenerEgresos(user) #se cambiaron datos, obtener todos los egresos de user
				return render(request, 'save/Plantilla_VerListadoEgreso.html',{'error':"Egreso editado",'transacciones':transacciones})#mostrarMensaje("Egreso editado")
			else:
				#mostrarErrorMontoInvalido()	
				return render(request, 'save/Plantilla_EditarEgreso.html',{'egreso':egreso,'error':"Monto inválido",'categorias':categorias})
		else:
			#mostrarErrorNombreInvalido()
			return render(request, 'save/Plantilla_EditarEgreso.html',{'egreso':egreso,'error':"Nombre inválido",'categorias':categorias})
