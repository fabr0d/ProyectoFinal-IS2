from django.http import HttpResponse
from django.shortcuts import render,redirect
from save.models import Usuario,Ingreso,Egreso,Categoria,ControlEgreso
import datetime


def index(request):
    return HttpResponse("index")


#CU_001
class Vista_IniciarSesion:  


    def iniciar_sesion(request):

        try:
            email=request.POST['email']
            contra=request.POST['password']
        except:
            if 'user' in request.session:
                del request.session['user']
            return render(request, 'save/Plantilla_IniciarSesion.html')
        if Usuario.existeEmail(email):
            if Usuario.existeUsuario(email,contra):
                #guardar el id del usuario en la sesion
                request.session['user'] = Usuario.conseguirUsuario(email)
                return Vista_inicio.inicio(request)#ir a pagina inicio
            else:
                #mostrarErrorContrasenaInvalida()
                return render(request, 'save/Plantilla_IniciarSesion.html',
                              {'error':"Contraseña inválida"})
        else:
            #mostrarErrorEmaiInvalido()
            return render(request, 'save/Plantilla_IniciarSesion.html',
                          {'error':"Email Inválido"})


class Vista_inicio:


	def inicio(request):
		user=request.session['user']
		correoUsuario=Usuario.objects.get(pk=user).correoElectronico
		montoAhorrado=Usuario.objects.get(pk=user).ahorro
		return render(request, 'save/inicioVista.html',
                          {'correo':correoUsuario,
                           'ahorro':montoAhorrado})


#CU_002
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
                return render(request, 'save/Plantilla_Registrar.html',
                              {'error':"El correo esta en uso"})
            else:
                Usuario.registrar(email,contra1)
                #irAPagIniciarSesion()
                return render(request, 'save/Plantilla_IniciarSesion.html')
        else:
            #MostrarErrorContrasenasNoIguales()
            return render(request, 'save/Plantilla_Registrar.html',
                          {'error':"Contraseñas no iguales"})

def inicio(request):    
    return render(request,'save/inicioVista.html')


#CU_003
class Vista_RegistrarIngreso:
    

    def verificar_nombre(nombre):
        
        if len(nombre)<=50:
            return True
        else:
            return False
   
    def verificar_monto(monto):
        
        if float(monto)>=0:
            return True
        else:
            return False
   
    def verificar_ahorro(ahorro,monto):
        
        if float(ahorro)>=0 and float(ahorro)<=float(monto):
            return True
        else:
            return False
   
    def anadir_ingreso(request):
        
        try:
            fecha=request.POST['fecha']
            nombre=request.POST['nombre']
            monto=request.POST['monto']
            ahorro=request.POST['ahorro']
            user=request.session['user']
        except:
            return render(request, 'save/Plantilla_RegistrarIngreso.html')
        if Vista_RegistrarIngreso.verificar_nombre(nombre):
            if Vista_RegistrarIngreso.verificar_monto(monto):
                if Vista_RegistrarIngreso.verificar_ahorro(ahorro,monto):
                    Ingreso.anadirIngreso(fecha,nombre,monto,ahorro,user)
                    Usuario.aumentarAhorro(ahorro,user)
                    #mostrarMensajeIngresoAnadido()
                    return render(request,
                                  'save/Plantilla_RegistrarIngreso.html',
                                  {'error':"Ingreso añadido"})
                else:
                    #mostrarErrorAhorrroInvalido()
                    return render(request,
                                  'save/Plantilla_RegistrarIngreso.html',
                                  {'error':"Ahorro inválido"})
            else:
                #mostrarErrorMontoInvalido()
                return render(request, 'save/Plantilla_RegistrarIngreso.html',
                              {'error':"Monto inválido"})
        else:
            #mostrarErrorNombreInvalido()
            return render(request, 'save/Plantilla_RegistrarIngreso.html',
                          {'error':"Nombre inválido"})


#CU_004
class Vista_RegistrarEgreso:


    def verificar_nombre(nombre):
        if len(nombre)<=50:
            return True
        else:
            return False    

    def verificar_monto(monto):
        if float(monto)>=0:
            return True
        else:
            return False

    def anadir_egreso(request):
        categorias=Categoria.objects.all()#conseguirCategorias
        try:
            fecha=request.POST['fecha']
            nombre=request.POST['nombre']
            monto=request.POST['monto']
            categoria=request.POST['categoria']
            user=request.session['user']
        except:
            return render(request, 'save/Plantilla_RegistrarEgreso.html',
                          {'categorias':categorias})

        if Vista_RegistrarEgreso.verificar_nombre(nombre):
            if Vista_RegistrarEgreso.verificar_monto(monto):
                #si categoria es ahorro
                if Categoria.objects.get(pk=categoria).nombre=="Ahorro":
                    if Usuario.disminuirAhorro(monto,user):
                        Egreso.anadirEgreso(fecha,nombre,monto,categoria,user)
                        #mostrarMensajeEgresoAnadido()
                        return render(request, 
                                      'save/Plantilla_RegistrarEgreso.html',
                                      {'error':"Egreso añadido",
                                       'categorias':categorias})
                    else:
                        #mostrarErrorNoExisteAhorroParaQuitar()
                        return render(request, 
                                      'save/Plantilla_RegistrarEgreso.html',
                                      {'error':"No existe ahorro para quitar",
                                       'categorias':categorias})
                else:
                    Egreso.anadirEgreso(fecha,nombre,monto,categoria,user)
                    #mostrarMensajeEgresoAnadido()
                    return render(request, 
                                  'save/Plantilla_RegistrarEgreso.html',
                                  {'error':"Egreso añadido",
                                   'categorias':categorias})
            else:
                #mostrarErrorMontoInvalido()    
                return render(request, 
                              'save/Plantilla_RegistrarEgreso.html',
                              {'error':"Monto inválido",
                               'categorias':categorias})
        else:
            #mostrarErrorNombreInvalido()
            return render(request, 
                          'save/Plantilla_RegistrarEgreso.html',
                          {'error':"Nombre inválido",
                           'categorias':categorias})


class Vista_VerListado:


    def verificar_nombre(nombre):
        if len(nombre)<=50:
            return True
        else:
            return False

    def verificar_monto(monto):
        if float(monto)>=0:
            return True
        else:
            return False

    def verificar_ahorro(ahorro,monto):
        if float(ahorro)>=0 and float(ahorro)<=float(monto):
            return True
        else:
            return False

    def ver_listado_ingresos(request):

        user=request.session['user']
        #obtener todos los ingresos de user
        transacciones=Ingreso.obtenerIngresos(user)
        try:
            ingreso_id=request.POST['transaccion'] 
        except:
            #mostrar los ingresos
            return render(request, 'save/Plantilla_VerListadoIngreso.html',
                          {'transacciones':transacciones})        
        ingreso=Ingreso.conseguirIngreso(ingreso_id)
        request.session['tmp'] = ingreso_id
        #mostrar la plantilla de editar ingreso con todos 
        #los valores de el ingreso seleccionado
        return render(request, 'save/Plantilla_EditarIngreso.html',
                      {'ingreso':ingreso})

#CU_005
    def editar_ingreso(request):

        fecha=request.POST['fecha']
        nombre=request.POST['nombre']
        monto=request.POST['monto']
        ahorro=request.POST['ahorro']
        ingreso_id=request.session['tmp']
        user=request.session['user']
        ingreso=Ingreso.objects.get(pk=ingreso_id)#deberia hacerse en bd
        if Vista_RegistrarIngreso.verificar_nombre(nombre):
            if Vista_RegistrarIngreso.verificar_monto(monto):
                if Vista_RegistrarIngreso.verificar_ahorro(ahorro,monto):
                    antiguoAhorro=Ingreso.obtenerAhorro(ingreso_id)
                    #editar el ingreso en la base de datos
                    Ingreso.editarIngreso(fecha,nombre,monto,
                                          ahorro,user,ingreso_id)
                    Usuario.reemplazarAhorro(user,antiguoAhorro,ahorro)
                    #se cambiaron datos, obtener todos los ingresos de user     
                    transacciones=Ingreso.obtenerIngresos(user)
                    #mostrarMensaje("Ingreso editado")
                    return render(request, 
                                  'save/Plantilla_VerListadoIngreso.html',
                                  {'error':"Ingreso editado",
                                   'transacciones':transacciones})
                else:
                    #mostrarErrorAhfnoorrroInvalidoIngreso()
                    return render(request, 
                                  'save/Plantilla_EditarIngreso.html',
                                  {'ingreso':ingreso, 
                                   'error':"Ahorro inválido"})
            else:
                #mostrarErrorMontoInvalidoIngreso()
                return render(request, 
                              'save/Plantilla_EditarIngreso.html',
                              {'ingreso':ingreso, 
                               'error':"Monto inválido"})
        else:
            #mostrarErrorNombreInvalidoIngreso()
            return render(request, 
                          'save/Plantilla_EditarIngreso.html',
                          {'ingreso':ingreso, 
                           'error':"Nombre inválido"})

    def ver_listado_egresos(request):

        user=request.session['user']
        #obtener todos los egresos de user
        transacciones=Egreso.obtenerEgresos(user) 
        try:
            egreso_id=request.POST['transaccion']
        except:
            #mostrar los egresos
            return render(request, 
                          'save/Plantilla_VerListadoEgreso.html',
                          {'transacciones':transacciones}) 
        egreso=Egreso.conseguirEgreso(egreso_id)
        request.session['tmp'] = egreso_id
        categorias=Categoria.obtenerTodo()#conseguir todas las categorias
        #mostrar la plantilla de editar egreso con todos
        #los valores de el egreso seleccionado
        #editarEgreso(egreso,categorias)
        return render(request, 
                      'save/Plantilla_EditarEgreso.html',
                      {'egreso':egreso,'categorias':categorias})

#CU_006 
    def editar_egreso(request):

        #conseguir todos los parametros del form de la vista
        fecha=request.POST['fecha']
        nombre=request.POST['nombre']
        monto=request.POST['monto']
        categoria=request.POST['categoria']
        egreso_id=request.session['tmp']
        user=request.session['user']
        egreso=Egreso.conseguirEgreso(egreso_id)
        categorias=Categoria.objects.all()#conseguirCategorias
        if Vista_RegistrarEgreso.verificar_nombre(nombre):
            if Vista_RegistrarEgreso.verificar_monto(monto):
                #editar el egreso en la base de datos
                Egreso.editarEgreso(fecha,nombre,monto,
                                    categoria,user,egreso_id)
                #se cambiaron datos, obtener todos los egresos de user
                transacciones=Egreso.obtenerEgresos(user)
                #mostrarMensaje("Egreso editado")
                return render(request, 'save/Plantilla_VerListadoEgreso.html',
                              {'error':"Egreso editado",
                               'transacciones':transacciones})
            else:
                #mostrarErrorMontoInvalido()    
                return render(request, 'save/Plantilla_EditarEgreso.html',
                              {'egreso':egreso,'error':"Monto inválido",
                               'categorias':categorias})
        else:
            #mostrarErrorNombreInvalido()
            return render(request, 'save/Plantilla_EditarEgreso.html',
                          {'egreso':egreso,'error':"Nombre inválido",
                           'categorias':categorias})


#CU_007
class Vista_ControlEgresos:


    def ver_control_egreso(request):

        user=request.session['user']
        if Usuario.objects.get(pk=user).tipoDeCuenta == 0:
        	return render(request,'save/Plantilla_ControlEgresosNoP.html')
        aGastarPorCategorias=list()
        try:            
        	#conseguir todos los campos del template dentro de la lista aGastarPorCategorias
            aGastarPorCategorias.append(request.POST['Servicios'])
            aGastarPorCategorias.append(request.POST['Compras'])
            aGastarPorCategorias.append(request.POST['Ahorro'])
            aGastarPorCategorias.append(request.POST['Alimentacion'])
            aGastarPorCategorias.append(request.POST['Transporte'])
            aGastarPorCategorias.append(request.POST['Otros'])
            return Vista_ControlEgresos.actualizar_montos_usar(request,aGastarPorCategorias)
        except:
            montos_usar=ControlEgreso.obtenerMontosUsar(user)
            montos_usados=Egreso.obtenerMontosUsadosPorCategoria(user)
            return render(request, 'save/Plantilla_ControlEgresos.html',
                          {'montoAUsar':montos_usar,
                           'montosUsados':montos_usados})
    
    def actualizar_montos_usar(request, listaDeMontos):

        user=request.session['user']
        montos_usar=ControlEgreso.obtenerMontosUsar(user)
        montos_usados=Egreso.obtenerMontosUsadosPorCategoria(user)
        #si algun monto no est en el rango error Monto invalido
        for mon in listaDeMontos:
            if float(mon)<0 or float(mon)>999999999:
                return render(request, 'save/Plantilla_ControlEgresos.html',
                              {'error':"monto invalido",
                              'montoAUsar':montos_usar,
                              'montosUsados':montos_usados})
        #actualizar todos los montos
        ControlEgreso.actualizarMontoUsar(user,'Servicios',listaDeMontos[0])
        ControlEgreso.actualizarMontoUsar(user,'Compras',listaDeMontos[1])
        ControlEgreso.actualizarMontoUsar(user,'Ahorro',listaDeMontos[2])
        ControlEgreso.actualizarMontoUsar(user,'Alimentacion',listaDeMontos[3])
        ControlEgreso.actualizarMontoUsar(user,'Transporte',listaDeMontos[4])
        ControlEgreso.actualizarMontoUsar(user,'Otros',listaDeMontos[5])
        return render(request, 'save/Plantilla_ControlEgresos.html',
                      {'error':"montos actualizados",
                       'montoAUsar':montos_usar,
                       'montosUsados':montos_usados})


#CU_008
class Vista_CompararPeriodos:


    def comparar_periodos(request):

        user=request.session['user']
        try:
            fecha1=datetime.datetime.strptime(request.POST['fecha1'],
                                              '%Y-%m-%d')
            fecha2=datetime.datetime.strptime(request.POST['fecha2'],
                                              '%Y-%m-%d')
            tipo=request.POST['periodo']
        except:
            fecha1=datetime.datetime.now()
            fecha2=datetime.datetime.now()
            tipo="mes"          
        #verificarFechas(fecha1, fecha2)
        if fecha1<datetime.datetime.strptime("1000-01-01",'%Y-%m-%d') or \
        	fecha1>datetime.datetime.strptime("9000-12-31",'%Y-%m-%d') or \
        	fecha2<datetime.datetime.strptime("1000-01-01",'%Y-%m-%d') or \
        	fecha2>datetime.datetime.strptime("9000-12-31",'%Y-%m-%d'):
        	# mostrarErrorFechasInvalidas()
        	return render(request,'save/Plantilla_CompararPeriodos.html',
                    	  {'fecha1':fecha1.strftime("%Y-%m-%d"),
                    	   'fecha2':fecha2.strftime("%Y-%m-%d"),
                    	   'tipo':tipo,
                    	   'error':"Fechas invalidas"})
        #obtener la lista de egresos de ambas fechas en el periodo "tipo"
        egresos1=Egreso.obtenerEgresosCategoria(user,fecha1,tipo)
        egresos2=Egreso.obtenerEgresosCategoria(user,fecha2,tipo)
        return render(request,'save/Plantilla_CompararPeriodos.html',
                      {'egresos1':egresos1,
                       'egresos2':egresos2,
                       'fecha1':fecha1.strftime("%Y-%m-%d"),
                       'fecha2':fecha2.strftime("%Y-%m-%d"),
                       'tipo':tipo})
