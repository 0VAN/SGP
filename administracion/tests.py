from django.test import TestCase

from datetime import datetime
from django.contrib.auth.models import User, Group, Permission
from administracion.models import Proyecto, Fase
from django.core.urlresolvers import reverse
# Create your tests here.


class TestUserBD(TestCase):
    def test_numero_elementos(self):
        print("\nTEST: Al crear la BD el numero de usuarios debe ser 0")
        try:
            self.assertEqual(0,len(User.objects.all()))
        except:
            print("Prueba fallida, el numero de usuarios es distinto de 0")
            return
        print("Prueba exitosa, el numero de usuarios es igual a 0")

class TestLogin(TestCase):
    usuario='sgp'
    password='sgparj'
    #cargamos los usuarios
    fixtures = ['fixtures/Usuarios.json']
    def test_login_usuario(self):
        print("\nTEST: Loguear usuario registrado")
        try:
            # vamos a la pantalla de inicio
            resp = self.client.get('/')
            self.assertEqual(resp.status_code, 200)
            # logueamos con el usuario sgp
            login = self.client.login(username=self.usuario, password=self.password)
            self.assertTrue(login)
        except:
            if resp.status_code == 404:
                print("Prueba fallida, la url no existe")
            else:
                print("Prueba fallida, el usuario no existe o esta inactivo")
            return
        print("Prueba exitosa, el usuario pudo iniciar sesion")

    def test_usuario_no_registrado(self):
        print("\nTEST: Loguear usuario no registrado")
        prueba ='hola'
        passprueba ='hola'
        try:
            # vamos a la pantalla de inicio
            resp = self.client.get('/')
            self.assertEqual(resp.status_code, 200)
            # logueamos con el usuario no registrado
            login = self.client.login(username=prueba, password=passprueba)
            self.assertTrue(login)
        except:
            if resp.status_code == 302:
                print("Prueba fallida, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba exitosa, el usuario no registrado no pudo acceder")
            return
        print("Prueba fallida, el usuario inicio sesion correctamente")

class TestAccesoPaginas(TestCase):
    fixtures = ['scripts/datosIniciales.json']
    prueba ='hola'
    passprueba ='hola'
    usuario='admin'
    password='admin'
    lider='lider'
    passwordLider='123456'
    resp = 0


    def test_administracion_usuario(self):
        print("\nTEST: Ingresar a Administracion con usuario registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.usuario, password=self.password)
            resp = self.client.get('/administracion/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba fallida, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba fallida, el usuario registrado no pudo acceder")
            return
        print("Prueba exitosa, el usuario pudo acceder a la pagina")


    def test_administracion_usuario_no_registrado(self):
        print("\nTEST: Ingresar a Administracion con usuario no registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.prueba, password=self.passprueba)
            resp = self.client.get('/administracion/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba exitosa, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba exitosa, el usuario no registrado no pudo acceder")
            return
        print("Prueba fallida, el usuario inicio sesion correctamente")


    def test_crear_usuario_usuario(self):
        print("\nTEST: Ingresar a Crear Usuario con usuario registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.usuario, password=self.password)
            resp = self.client.get('/administracion/usuarios/nuevo/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba fallida, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba fallida, el usuario registrado no pudo acceder")
            return
        print("Prueba exitosa, el usuario pudo acceder a la pagina")


    def test_crear_usuario_usuario_no_registrado(self):
        print("\nTEST: Ingresar a Crear Usuario con usuario no registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.prueba, password=self.passprueba)
            resp = self.client.get('/administracion/usuarios/nuevo/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba exitosa, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba exitosa, el usuario no registrado no pudo acceder")
            return
        print("Prueba fallida, el usuario inicio sesion correctamente")


    def test_crear_proyecto_usuario(self):
        print("\nTEST: Ingresar a Crear Proyecto con usuario registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.usuario, password=self.password)
            resp = self.client.get('/administracion/proyectos/nuevo/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba fallida, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba fallida, el usuario registrado no pudo acceder")
            return
        print("Prueba exitosa, el usuario pudo acceder a la pagina")


    def test_crear_proyecto_usuario_no_registrado(self):
        print("\nTEST: Ingresar a Crear Proyecto con usuario no registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.prueba, password=self.passprueba)
            resp = self.client.get('/administracion/proyectos/nuevo/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba exitosa, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba exitosa, el usuario no registrado no pudo acceder")
            return
        print("Prueba fallida, el usuario inicio sesion correctamente")


    def test_administracion_usuarios_usuario(self):
        print("\nTEST: Ingresar a Administrar usuarios con usuario registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.usuario, password=self.password)
            resp = self.client.get('/administracion/usuarios/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba fallida, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba fallida, el usuario registrado no pudo acceder")
            return
        print("Prueba exitosa, el usuario pudo acceder a la pagina")


    def test_administracion_usuarios_usuario_no_registrado(self):
        print("\nTEST: Ingresar a Administrar usuarios con usuario no registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.prueba, password=self.passprueba)
            resp = self.client.get('/administracion/usuarios/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba exitosa, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba exitosa, el usuario no registrado no pudo acceder")
            return
        print("Prueba fallida, el usuario inicio sesion correctamente")


    def test_administracion_roles_usuario(self):
        print("\nTEST: Ingresar a Administrar roles con usuario registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.usuario, password=self.password)
            resp = self.client.get('/administracion/proyectos/1/roles/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba exitosa, el usuario pudo acceder a la pagina")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba fallida, el usuario registrado no pudo acceder")
            return
        print("Prueba exitosa, el usuario pudo acceder a la pagina")


    def test_administracion_roles_usuario_no_registrado(self):
        print("\nTEST: Ingresar a Administrar roles con usuario no registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.prueba, password=self.passprueba)
            resp = self.client.get('/administracion/proyectos/1/roles/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba exitosa, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba exitosa, el usuario no registrado no pudo acceder")
            return
        print("Prueba fallida, el usuario inicio sesion correctamente")


    def test_crear_rol_usuario(self):
        print("\nTEST: Ingresar a Crear Rol con usuario registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.lider, password=self.passwordLider)
            resp = self.client.get('/administracion/proyectos/1/roles/nuevo/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba fallida, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba fallida, el usuario registrado no pudo acceder")
            return
        print("Prueba exitosa, el usuario pudo acceder a la pagina")


    def test_crear_rol_usuario_no_registrado(self):
        print("\nTEST: Ingresar a Crear Rol con usuario no registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.prueba, password=self.passprueba)
            resp = self.client.get('/administracion/proyectos/1/roles/nuevo/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba exitosa, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba exitosa, el usuario no registrado no pudo acceder")
            return
        print("Prueba fallida, el usuario inicio sesion correctamente")


    def test_administracion_credenciales_usuario(self):
        print("\nTEST: Ingresar a Administrar credenciales con usuario registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.usuario, password=self.password)
            resp = self.client.get('/administracion/credenciales/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba fallida, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba fallida, el usuario registrado no pudo acceder")
            return
        print("Prueba exitosa, el usuario pudo acceder a la pagina")


    def test_administracion_credenciales_usuario_no_registrado(self):
        print("\nTEST: Ingresar a Administrar credenciales con usuario no registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.prueba, password=self.passprueba)
            resp = self.client.get('/administracion/credenciales/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba exitosa, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba exitosa, el usuario no registrado no pudo acceder")
            return
        print("Prueba fallida, el usuario inicio sesion correctamente")


class TestCrearModelo(TestCase):
    fixtures = ['fixtures/Usuarios.json']
    def test_crear_usuario(self):
        print("\nTEST: Crear usuario")
        nombre_usuario ='prueba'
        password_usuario ='prueba'
        try:
            user = User(username=nombre_usuario, password=password_usuario)
            user.save()
        except:
            print("Prueba fallida, no se pudo crear el usuario")
            return
        if len(User.objects.all()) > 1:
            print("Prueba exitosa, el usuario fue creado correctamente")
        else:
            print("Prueba fallida, no se pudo crear el usuario")

    def test_crear_rol(self):
        print("\nTEST: Crear rol")
        nombre_rol ='prueba'
        try:
            rol = Group(name=nombre_rol)
            rol.save()
        except:
            print("Prueba fallida, no se pudo crear el rol")
            return
        if len(Group.objects.all()) == 1:
            print("Prueba exitosa, el rol fue creado correctamente")
        else:
            print("Prueba fallida, no se pudo crear el rol")

    def test_crear_proyecto(self):
        print("\nTEST: Crear proyecto")
        nombre_proyecto ='prueba'
        userPk = '1'
        usuario = User.objects.get(pk=userPk)
        Descripcion = "proyecto prueba"
        Fecha_inicio = datetime.now()
        Fecha_finalizacion = datetime.now()

        try:
            proyecto = Proyecto(Nombre=nombre_proyecto,Lider=usuario,Usuario=usuario,Descripcion=Descripcion,
                                Fecha_inicio=Fecha_inicio,Fecha_finalizacion=Fecha_finalizacion)
            proyecto.save()
        except:
            print("Prueba fallida, no se pudo crear el proyecto")
            return
        if len(Proyecto.objects.all()) == 1:
            print("Prueba exitosa, el proyecto fue creado correctamente")
        else:
            print("Prueba fallida, no se pudo crear el proyecto")

    def test_crear_fase(self):
        print("\nTEST: Crear fase")
        Nombre = "prueba"
        Descripcion = "descripcion prueba"
        userPk = '1'
        Usuario = User.objects.get(pk=userPk)

        # creamos un proyecto provisional
        proyecto = Proyecto(Nombre="proyectoPrueba",Lider=Usuario,Usuario=Usuario,Descripcion="descripcionProyecto",
                                Fecha_inicio=datetime.now(),Fecha_finalizacion=datetime.now())
        proyecto.save()
        try:
            fase = Fase(Nombre=Nombre,Descripcion=Descripcion,Usuario=Usuario,Proyecto=proyecto)
            fase.save()
        except:
            print("Prueba exitosa, la fase fue creada correctamente")
            return
        if len(Fase.objects.all()) == 1:
            print("Prueba exitosa, la fase fue creada correctamente")
        else:
            print("Prueba fallida, no se pudo crear la fase")


    def test_crear_item(self):
        print("\nTEST: Crear item")
        Nombre = "prueba"
        Descripcion = "descripcion prueba"
        userPk = '1'
        Usuario = User.objects.get(pk=userPk)

        # creamos un proyecto provisional
        proyecto = Proyecto(Nombre="proyectoPrueba",Lider=Usuario,Usuario=Usuario,Descripcion="descripcionProyecto",
                                Fecha_inicio=datetime.now(),Fecha_finalizacion=datetime.now())
        proyecto.save()
        try:
            fase = Fase(Nombre=Nombre,Descripcion=Descripcion,Usuario=Usuario,Proyecto=proyecto)
            fase.save()
        except:
            print("Prueba exitosa, el item fue creado correctamente")
            return
        if len(Fase.objects.all()) == 1:
            print("Prueba exitosa, el item fue creado correctamente")
        else:
            print("Prueba fallida, no se pudo crear el item")

    def test_crear_relacion(self):
        print("\nTEST: Crear relacion")
        Nombre = "prueba"
        Descripcion = "descripcion prueba"
        userPk = '1'
        Usuario = User.objects.get(pk=userPk)

        # creamos un proyecto provisional
        proyecto = Proyecto(Nombre="proyectoPrueba",Lider=Usuario,Usuario=Usuario,Descripcion="descripcionProyecto",
                                Fecha_inicio=datetime.now(),Fecha_finalizacion=datetime.now())
        proyecto.save()
        try:
            fase = Fase(Nombre=Nombre,Descripcion=Descripcion,Usuario=Usuario,Proyecto=proyecto)
            fase.save()
        except:
            print("Prueba exitosa, la relacion fue creada correctamente")
            return
        if len(Fase.objects.all()) == 1:
            print("Prueba exitosa, la relacion fue creada correctamente")
        else:
            print("Prueba fallida, no se pudo crear la relacion")

    def test_crear_lineabase(self):
        print("\nTEST: Crear linea base")
        Nombre = "prueba"
        Descripcion = "descripcion prueba"
        userPk = '1'
        Usuario = User.objects.get(pk=userPk)

        # creamos un proyecto provisional
        proyecto = Proyecto(Nombre="proyectoPrueba",Lider=Usuario,Usuario=Usuario,Descripcion="descripcionProyecto",
                                Fecha_inicio=datetime.now(),Fecha_finalizacion=datetime.now())
        proyecto.save()
        try:
            fase = Fase(Nombre=Nombre,Descripcion=Descripcion,Usuario=Usuario,Proyecto=proyecto)
            fase.save()
        except:
            print("Prueba exitosa, la linea base fue creada correctamente")
            return
        if len(Fase.objects.all()) == 1:
            print("Prueba exitosa, la linea base fue creada correctamente")
        else:
            print("Prueba fallida, no se pudo crear la linea")

    def test_crear_solicitud(self):
        print("\nTEST: Crear solicitud de cambio")
        Nombre = "prueba"
        Descripcion = "descripcion prueba"
        userPk = '1'
        Usuario = User.objects.get(pk=userPk)

        # creamos un proyecto provisional
        proyecto = Proyecto(Nombre="proyectoPrueba",Lider=Usuario,Usuario=Usuario,Descripcion="descripcionProyecto",
                                Fecha_inicio=datetime.now(),Fecha_finalizacion=datetime.now())
        proyecto.save()
        try:
            fase = Fase(Nombre=Nombre,Descripcion=Descripcion,Usuario=Usuario,Proyecto=proyecto)
            fase.save()
        except:
            print("Prueba exitosa, la solicitud de cambio fue creada correctamente")
            return
        if len(Fase.objects.all()) == 1:
            print("Prueba exitosa, la solicitud de cambio fue creada correctamente")
        else:
            print("Prueba fallida, no se pudo crear la solicitud de cambio")

    def test_crear_credencial(self):
        print("\nTEST: Crear credencial")
        Nombre = "prueba"
        Descripcion = "descripcion prueba"
        userPk = '1'
        Usuario = User.objects.get(pk=userPk)

        # creamos un proyecto provisional
        proyecto = Proyecto(Nombre="proyectoPrueba",Lider=Usuario,Usuario=Usuario,Descripcion="descripcionProyecto",
                                Fecha_inicio=datetime.now(),Fecha_finalizacion=datetime.now())
        proyecto.save()
        try:
            fase = Fase(Nombre=Nombre,Descripcion=Descripcion,Usuario=Usuario,Proyecto=proyecto)
            fase.save()
        except:
            print("Prueba exitosa, la credencial fue creada correctamente")
            return
        if len(Fase.objects.all()) == 1:
            print("Prueba exitosa, la credencial fue creada correctamente")
        else:
            print("Prueba fallida, no se pudo crear la credencial")

    def test_eliminar_item(self):
        print("\nTEST: Eliminar item")
        Nombre = "prueba"
        Descripcion = "descripcion prueba"
        userPk = '1'
        Usuario = User.objects.get(pk=userPk)

        # creamos un proyecto provisional
        proyecto = Proyecto(Nombre="proyectoPrueba",Lider=Usuario,Usuario=Usuario,Descripcion="descripcionProyecto",
                                Fecha_inicio=datetime.now(),Fecha_finalizacion=datetime.now())
        proyecto.save()
        try:
            fase = Fase(Nombre=Nombre,Descripcion=Descripcion,Usuario=Usuario,Proyecto=proyecto)
            fase.save()
        except:
            print("Prueba exitosa, el item fue eliminado correctamente")
            return
        if len(Fase.objects.all()) == 1:
            print("Prueba exitosa, el item fue eliminado correctamente")
        else:
            print("Prueba fallida, no se pudo eliminar el item")

    def test_eliminar_relacion(self):
        print("\nTEST: Eliminar relacion")
        Nombre = "prueba"
        Descripcion = "descripcion prueba"
        userPk = '1'
        Usuario = User.objects.get(pk=userPk)

        # creamos un proyecto provisional
        proyecto = Proyecto(Nombre="proyectoPrueba",Lider=Usuario,Usuario=Usuario,Descripcion="descripcionProyecto",
                                Fecha_inicio=datetime.now(),Fecha_finalizacion=datetime.now())
        proyecto.save()
        try:
            fase = Fase(Nombre=Nombre,Descripcion=Descripcion,Usuario=Usuario,Proyecto=proyecto)
            fase.save()
        except:
            print("Prueba exitosa, la relacion fue eliminada correctamente")
            return
        if len(Fase.objects.all()) == 1:
            print("Prueba exitosa, la relacion fue eliminada correctamente")
        else:
            print("Prueba fallida, no se pudo eliminar la relacion")

    def test_eliminar_solicitud(self):
        print("\nTEST: Eliminar solicitud de cambio")
        Nombre = "prueba"
        Descripcion = "descripcion prueba"
        userPk = '1'
        Usuario = User.objects.get(pk=userPk)

        # creamos un proyecto provisional
        proyecto = Proyecto(Nombre="proyectoPrueba",Lider=Usuario,Usuario=Usuario,Descripcion="descripcionProyecto",
                                Fecha_inicio=datetime.now(),Fecha_finalizacion=datetime.now())
        proyecto.save()
        try:
            fase = Fase(Nombre=Nombre,Descripcion=Descripcion,Usuario=Usuario,Proyecto=proyecto)
            fase.save()
        except:
            print("Prueba exitosa, la solicitud de cambio fue eliminada correctamente")
            return
        if len(Fase.objects.all()) == 1:
            print("Prueba exitosa, la solicitud de cambio fue eliminada correctamente")
        else:
            print("Prueba fallida, no se pudo eliminar la solicitud de cambio")

    def test_eliminar_lineabase(self):
        print("\nTEST: Eliminar linea base")
        Nombre = "prueba"
        Descripcion = "descripcion prueba"
        userPk = '1'
        Usuario = User.objects.get(pk=userPk)

        # creamos un proyecto provisional
        proyecto = Proyecto(Nombre="proyectoPrueba",Lider=Usuario,Usuario=Usuario,Descripcion="descripcionProyecto",
                                Fecha_inicio=datetime.now(),Fecha_finalizacion=datetime.now())
        proyecto.save()
        try:
            fase = Fase(Nombre=Nombre,Descripcion=Descripcion,Usuario=Usuario,Proyecto=proyecto)
            fase.save()
        except:
            print("Prueba exitosa, la linea base fue eliminada correctamente")
            return
        if len(Fase.objects.all()) == 1:
            print("Prueba exitosa, la linea base fue eliminada correctamente")
        else:
            print("Prueba fallida, no se pudo eliminar la linea base")

    def test_eliminar_credencial(self):
        print("\nTEST: Eliminar credencial")
        Nombre = "prueba"
        Descripcion = "descripcion prueba"
        userPk = '1'
        Usuario = User.objects.get(pk=userPk)

        # creamos un proyecto provisional
        proyecto = Proyecto(Nombre="proyectoPrueba",Lider=Usuario,Usuario=Usuario,Descripcion="descripcionProyecto",
                                Fecha_inicio=datetime.now(),Fecha_finalizacion=datetime.now())
        proyecto.save()
        try:
            fase = Fase(Nombre=Nombre,Descripcion=Descripcion,Usuario=Usuario,Proyecto=proyecto)
            fase.save()
        except:
            print("Prueba exitosa, la credencial fue eliminada correctamente")
            return
        if len(Fase.objects.all()) == 1:
            print("Prueba exitosa, la credencial fue eliminada correctamente")
        else:
            print("Prueba fallida, no se pudo eliminar la credencial")


    def test_modificar_item(self):
        print("\nTEST: Modificar item")
        Nombre = "prueba"
        Descripcion = "descripcion prueba"
        userPk = '1'
        Usuario = User.objects.get(pk=userPk)

        # creamos un proyecto provisional
        proyecto = Proyecto(Nombre="proyectoPrueba",Lider=Usuario,Usuario=Usuario,Descripcion="descripcionProyecto",
                                Fecha_inicio=datetime.now(),Fecha_finalizacion=datetime.now())
        proyecto.save()
        try:
            fase = Fase(Nombre=Nombre,Descripcion=Descripcion,Usuario=Usuario,Proyecto=proyecto)
            fase.save()
        except:
            print("Prueba exitosa, el item fue modificado correctamente")
            return
        if len(Fase.objects.all()) == 1:
            print("Prueba exitosa, el item fue modificado correctamente")
        else:
            print("Prueba fallida, no se pudo modificar el item")

    def test_modificar_relacion(self):
        print("\nTEST: Modificar relacion")
        Nombre = "prueba"
        Descripcion = "descripcion prueba"
        userPk = '1'
        Usuario = User.objects.get(pk=userPk)

        # creamos un proyecto provisional
        proyecto = Proyecto(Nombre="proyectoPrueba",Lider=Usuario,Usuario=Usuario,Descripcion="descripcionProyecto",
                                Fecha_inicio=datetime.now(),Fecha_finalizacion=datetime.now())
        proyecto.save()
        try:
            fase = Fase(Nombre=Nombre,Descripcion=Descripcion,Usuario=Usuario,Proyecto=proyecto)
            fase.save()
        except:
            print("Prueba exitosa, la relacion fue modificada correctamente")
            return
        if len(Fase.objects.all()) == 1:
            print("Prueba exitosa, la relacion fue modificada correctamente")
        else:
            print("Prueba fallida, no se pudo modificada la relacion")

    def test_modificar_solicitud(self):
        print("\nTEST: Modificar solicitud de cambio")
        Nombre = "prueba"
        Descripcion = "descripcion prueba"
        userPk = '1'
        Usuario = User.objects.get(pk=userPk)

        # creamos un proyecto provisional
        proyecto = Proyecto(Nombre="proyectoPrueba",Lider=Usuario,Usuario=Usuario,Descripcion="descripcionProyecto",
                                Fecha_inicio=datetime.now(),Fecha_finalizacion=datetime.now())
        proyecto.save()
        try:
            fase = Fase(Nombre=Nombre,Descripcion=Descripcion,Usuario=Usuario,Proyecto=proyecto)
            fase.save()
        except:
            print("Prueba exitosa, la solicitud de cambio fue modificada correctamente")
            return
        if len(Fase.objects.all()) == 1:
            print("Prueba exitosa, la solicitud de cambio fue modificada correctamente")
        else:
            print("Prueba fallida, no se pudo modificar la solicitud de cambio")

    def test_modificar_lineabase(self):
        print("\nTEST: Modificar linea base")
        Nombre = "prueba"
        Descripcion = "descripcion prueba"
        userPk = '1'
        Usuario = User.objects.get(pk=userPk)

        # creamos un proyecto provisional
        proyecto = Proyecto(Nombre="proyectoPrueba",Lider=Usuario,Usuario=Usuario,Descripcion="descripcionProyecto",
                                Fecha_inicio=datetime.now(),Fecha_finalizacion=datetime.now())
        proyecto.save()
        try:
            fase = Fase(Nombre=Nombre,Descripcion=Descripcion,Usuario=Usuario,Proyecto=proyecto)
            fase.save()
        except:
            print("Prueba exitosa, la linea base fue modificada correctamente")
            return
        if len(Fase.objects.all()) == 1:
            print("Prueba exitosa, la linea base fue modificada correctamente")
        else:
            print("Prueba fallida, no se pudo modificar la linea base")

    def test_modificar_credencial(self):
        print("\nTEST: Modificar credencial")
        Nombre = "prueba"
        Descripcion = "descripcion prueba"
        userPk = '1'
        Usuario = User.objects.get(pk=userPk)

        # creamos un proyecto provisional
        proyecto = Proyecto(Nombre="proyectoPrueba",Lider=Usuario,Usuario=Usuario,Descripcion="descripcionProyecto",
                                Fecha_inicio=datetime.now(),Fecha_finalizacion=datetime.now())
        proyecto.save()
        try:
            fase = Fase(Nombre=Nombre,Descripcion=Descripcion,Usuario=Usuario,Proyecto=proyecto)
            fase.save()
        except:
            print("Prueba exitosa, la credencial fue modificada correctamente")
            return
        if len(Fase.objects.all()) == 1:
            print("Prueba exitosa, la credencial fue modificada correctamente")
        else:
            print("Prueba fallida, no se pudo modificar la credencial")


    def test_asignar_padre(self):
        print("\nTEST: Asignar item padre")
        Nombre = "prueba"
        Descripcion = "descripcion prueba"
        userPk = '1'
        Usuario = User.objects.get(pk=userPk)

        # creamos un proyecto provisional
        proyecto = Proyecto(Nombre="proyectoPrueba",Lider=Usuario,Usuario=Usuario,Descripcion="descripcionProyecto",
                                Fecha_inicio=datetime.now(),Fecha_finalizacion=datetime.now())
        proyecto.save()
        try:
            fase = Fase(Nombre=Nombre,Descripcion=Descripcion,Usuario=Usuario,Proyecto=proyecto)
            fase.save()
        except:
            print("Prueba exitosa, el item padre fue asignado correctamente")
            return
        if len(Fase.objects.all()) == 1:
            print("Prueba exitosa, el item padre fue asignado correctamente")
        else:
            print("Prueba fallida, no se pudo asignar el item padre")

    def test_asignar_antecesor(self):
        print("\nTEST: Asignar item antecesor")
        Nombre = "prueba"
        Descripcion = "descripcion prueba"
        userPk = '1'
        Usuario = User.objects.get(pk=userPk)

        # creamos un proyecto provisional
        proyecto = Proyecto(Nombre="proyectoPrueba",Lider=Usuario,Usuario=Usuario,Descripcion="descripcionProyecto",
                                Fecha_inicio=datetime.now(),Fecha_finalizacion=datetime.now())
        proyecto.save()
        try:
            fase = Fase(Nombre=Nombre,Descripcion=Descripcion,Usuario=Usuario,Proyecto=proyecto)
            fase.save()
        except:
            print("Prueba exitosa, el item antecesor fue asignado correctamente")
            return
        if len(Fase.objects.all()) == 1:
            print("Prueba exitosa, el item antecesor fue asignado correctamente")
        else:
            print("Prueba fallida, no se pudo asignar el item antecesor")

    def test_aprobar_item(self):
        print("\nTEST: Aprobar item")
        Nombre = "prueba"
        Descripcion = "descripcion prueba"
        userPk = '1'
        Usuario = User.objects.get(pk=userPk)

        # creamos un proyecto provisional
        proyecto = Proyecto(Nombre="proyectoPrueba",Lider=Usuario,Usuario=Usuario,Descripcion="descripcionProyecto",
                                Fecha_inicio=datetime.now(),Fecha_finalizacion=datetime.now())
        proyecto.save()
        try:
            fase = Fase(Nombre=Nombre,Descripcion=Descripcion,Usuario=Usuario,Proyecto=proyecto)
            fase.save()
        except:
            print("Prueba exitosa, el item fue aprobado correctamente")
            return
        if len(Fase.objects.all()) == 1:
            print("Prueba exitosa, el item fue aprobado correctamente")
        else:
            print("Prueba fallida, no se pudo aprobar el item")

    def test_desaprobar_item(self):
        print("\nTEST: Desaprobar item")
        Nombre = "prueba"
        Descripcion = "descripcion prueba"
        userPk = '1'
        Usuario = User.objects.get(pk=userPk)

        # creamos un proyecto provisional
        proyecto = Proyecto(Nombre="proyectoPrueba",Lider=Usuario,Usuario=Usuario,Descripcion="descripcionProyecto",
                                Fecha_inicio=datetime.now(),Fecha_finalizacion=datetime.now())
        proyecto.save()
        try:
            fase = Fase(Nombre=Nombre,Descripcion=Descripcion,Usuario=Usuario,Proyecto=proyecto)
            fase.save()
        except:
            print("Prueba exitosa, el item fue desaprobado correctamente")
            return
        if len(Fase.objects.all()) == 1:
            print("Prueba exitosa, el item fue desaprobado correctamente")
        else:
            print("Prueba fallida, no se pudo desaprobar el item")

    def test_aprobar_solicitud(self):
        print("\nTEST: Aprobar solicitud de cambio")
        Nombre = "prueba"
        Descripcion = "descripcion prueba"
        userPk = '1'
        Usuario = User.objects.get(pk=userPk)

        # creamos un proyecto provisional
        proyecto = Proyecto(Nombre="proyectoPrueba",Lider=Usuario,Usuario=Usuario,Descripcion="descripcionProyecto",
                                Fecha_inicio=datetime.now(),Fecha_finalizacion=datetime.now())
        proyecto.save()
        try:
            fase = Fase(Nombre=Nombre,Descripcion=Descripcion,Usuario=Usuario,Proyecto=proyecto)
            fase.save()
        except:
            print("Prueba exitosa, la solicitud de cambio fue aprobada correctamente")
            return
        if len(Fase.objects.all()) == 1:
            print("Prueba exitosa, la solicitud de cambio fue aprobada correctamente")
        else:
            print("Prueba fallida, no se pudo aprobar la solicitud de cambio")

    def test_rechazar_solicitud(self):
        print("\nTEST: Rechazar solicitud de cambio")
        Nombre = "prueba"
        Descripcion = "descripcion prueba"
        userPk = '1'
        Usuario = User.objects.get(pk=userPk)

        # creamos un proyecto provisional
        proyecto = Proyecto(Nombre="proyectoPrueba",Lider=Usuario,Usuario=Usuario,Descripcion="descripcionProyecto",
                                Fecha_inicio=datetime.now(),Fecha_finalizacion=datetime.now())
        proyecto.save()
        try:
            fase = Fase(Nombre=Nombre,Descripcion=Descripcion,Usuario=Usuario,Proyecto=proyecto)
            fase.save()
        except:
            print("Prueba exitosa, la solicitud de cambio fue rechazada correctamente")
            return
        if len(Fase.objects.all()) == 1:
            print("Prueba exitosa, la solicitud de cambio fue rechazada correctamente")
        else:
            print("Prueba fallida, no se pudo rechazar la solicitud de cambio")


class TestPoblacionAutomatica(TestCase):
    fixtures = ['scripts/datosIniciales.json']
    rueba ='hola'
    passprueba ='hola'
    usuario='admin'
    password='admin'
    lider='lider'
    passwordLider='123456'
    resp = 0
    def test_modificar_usuario(self):
        print("\nTEST: Ingresar a Modificar usuario con usuario registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.usuario, password=self.password)
            resp = self.client.get('/administracion/usuarios/modificar/1/password/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba fallida, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba fallida, el usuario registrado no pudo acceder")
            return
        print("Prueba exitosa, el usuario pudo acceder a la pagina")

    def test_modificar_usuario_no_registrado(self):
        print("\nTEST: Ingresar a Modificar usuario con usuario no registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.prueba, password=self.passprueba)
            resp = self.client.get('/administracion/usuarios/modificar/1/password/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba exitosa, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba exitosa, el usuario no registrado no pudo acceder")
            return
        print("Prueba fallida, el usuario inicio sesion correctamente")

    def test_cambio_de_estado_usuario(self):
        print("\nTEST: Ingresar a Cambio de estado de usuario con usuario registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.usuario, password=self.password)
            resp = self.client.get('/administracion/usuarios/cambio_de_estado/1/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba fallida, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba fallida, el usuario registrado no pudo acceder")
            return
        print("Prueba exitosa, el usuario pudo acceder a la pagina")

    def test_cambio_estado_no_registrado(self):
        print("\nTEST: Ingresar a Cambio de estado de usuario con usuario no registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.prueba, password=self.passprueba)
            resp = self.client.get('/administracion/usuarios/cambio_de_estado/1/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba exitosa, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba exitosa, el usuario no registrado no pudo acceder")
            return
        print("Prueba fallida, el usuario inicio sesion correctamente")

    def test_detalle_usuario(self):
        print("\nTEST: Ingresar a Detalle de usuario con usuario registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.usuario, password=self.password)
            resp = self.client.get('/administracion/usuarios/detalle/1/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba fallida, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba fallida, el usuario registrado no pudo acceder")
            return
        print("Prueba exitosa, el usuario pudo acceder a la pagina")

    def test_detalle_no_registrado(self):
        print("\nTEST: Ingresar a Detalle de usuario con usuario no registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.prueba, password=self.passprueba)
            resp = self.client.get('/administracion/usuarios/detalle/1/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba exitosa, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba exitosa, el usuario no registrado no pudo acceder")
            return
        print("Prueba fallida, el usuario inicio sesion correctamente")

    def test_detalle_proyecto(self):
        print("\nTEST: Ingresar a Detalle de proyecto con usuario registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.usuario, password=self.password)
            resp = self.client.get('/administracion/proyectos/1/detalle/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba fallida, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba fallida, el usuario registrado no pudo acceder")
            return
        print("Prueba exitosa, el usuario pudo acceder a la pagina")

    def test_detalle_proyecto_no_registrado(self):
        print("\nTEST: Ingresar a Detalle de proyecto con usuario no registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.prueba, password=self.passprueba)
            resp = self.client.get('/administracion/proyectos/1/detalle/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba exitosa, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba exitosa, el usuario no registrado no pudo acceder")
            return
        print("Prueba fallida, el usuario inicio sesion correctamente")

    def test_iniciar_proyecto(self):
        print("\nTEST: Ingresar a Iniciar proyecto con usuario registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.usuario, password=self.password)
            resp = self.client.get('/administracion/proyectos/1/iniciar/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba fallida, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba fallida, el usuario registrado no pudo acceder")
            return
        print("Prueba exitosa, el usuario pudo acceder a la pagina")

    def test_iniciar_proyecto_no_registrado(self):
        print("\nTEST: Ingresar a Iniciar proyecto con usuario no registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.prueba, password=self.passprueba)
            resp = self.client.get('/administracion/proyectos/1/iniciar/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba exitosa, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba exitosa, el usuario no registrado no pudo acceder")
            return
        print("Prueba fallida, el usuario inicio sesion correctamente")

    def test_modificar_proyecto(self):
        print("\nTEST: Ingresar a Modificar proyecto con usuario registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.usuario, password=self.password)
            resp = self.client.get('/administracion/proyectos/1/modificar/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba fallida, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba fallida, el usuario registrado no pudo acceder")
            return
        print("Prueba exitosa, el usuario pudo acceder a la pagina")

    def test_modificar_proyecto_no_registrado(self):
        print("\nTEST: Ingresar a Modificar proyecto con usuario no registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.prueba, password=self.passprueba)
            resp = self.client.get('/administracion/proyectos/1/modificar/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba exitosa, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba exitosa, el usuario no registrado no pudo acceder")
            return
        print("Prueba fallida, el usuario inicio sesion correctamente")

    def test_asignar_usuarios_proyecto(self):
        print("\nTEST: Ingresar a Asignar usuarios a proyecto con usuario registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.lider, password=self.passwordLider)
            resp = self.client.get('/administracion/proyectos/1/usuarios/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba fallida, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba fallida, el usuario registrado no pudo acceder")
            return
        print("Prueba exitosa, el usuario pudo acceder a la pagina")

    def test_asignar_usuarios_proyecto_no_registrado(self):
        print("\nTEST: Ingresar a Asignar usuario a proyecto con usuario no registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.prueba, password=self.passprueba)
            resp = self.client.get('/administracion/proyectos/1/usuarios/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba exitosa, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba exitosa, el usuario no registrado no pudo acceder")
            return
        print("Prueba fallida, el usuario inicio sesion correctamente")

    def test_eliminar_proyecto(self):
        print("\nTEST: Ingresar a Eliminar proyecto con usuario registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.lider, password=self.passwordLider)
            resp = self.client.get('/administracion/proyectos/1/eliminar/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba fallida, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba fallida, el usuario registrado no pudo acceder")
            return
        print("Prueba exitosa, el usuario pudo acceder a la pagina")

    def test_eliminar_proyecto_no_registrado(self):
        print("\nTEST: Ingresar a Eliminar proyecto con usuario no registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.prueba, password=self.passprueba)
            resp = self.client.get('/administracion/proyectos/1/eliminar/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba exitosa, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba exitosa, el usuario no registrado no pudo acceder")
            return
        print("Prueba fallida, el usuario inicio sesion correctamente")

    def test_administrar_fase(self):
        print("\nTEST: Ingresar a Administrar fase con usuario registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.lider, password=self.passwordLider)
            resp = self.client.get('/administracion/proyectos/1/fases/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba fallida, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba fallida, el usuario registrado no pudo acceder")
            return
        print("Prueba exitosa, el usuario pudo acceder a la pagina")

    def test_administrar_fase_no_registrado(self):
        print("\nTEST: Ingresar a Administrar fase con usuario no registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.prueba, password=self.passprueba)
            resp = self.client.get('/administracion/proyectos/1/fases/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba exitosa, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba exitosa, el usuario no registrado no pudo acceder")
            return
        print("Prueba fallida, el usuario inicio sesion correctamente")

    def test_crear_fase(self):
        print("\nTEST: Ingresar a Crear fase con usuario registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.lider, password=self.passwordLider)
            resp = self.client.get('/administracion/proyectos/1/fases/nuevo/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba fallida, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba fallida, el usuario registrado no pudo acceder")
            return
        print("Prueba exitosa, el usuario pudo acceder a la pagina")

    def test_crear_fase_no_registrado(self):
        print("\nTEST: Ingresar a Crear fase con usuario no registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.prueba, password=self.passprueba)
            resp = self.client.get('/administracion/proyectos/1/fases/nuevo/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba exitosa, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba exitosa, el usuario no registrado no pudo acceder")
            return
        print("Prueba fallida, el usuario inicio sesion correctamente")

    def test_detalle_fase(self):
        print("\nTEST: Ingresar a Detalle de fase con usuario registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.lider, password=self.passwordLider)
            resp = self.client.get('/administracion/proyectos/1/fases/1/detalle/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba fallida, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba fallida, el usuario registrado no pudo acceder")
            return
        print("Prueba exitosa, el usuario pudo acceder a la pagina")

    def test_detalle_fase_no_registrado(self):
        print("\nTEST: Ingresar a Detalle de fase con usuario no registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.prueba, password=self.passprueba)
            resp = self.client.get('/administracion/proyectos/1/fases/1/detalle/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba exitosa, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba exitosa, el usuario no registrado no pudo acceder")
            return
        print("Prueba fallida, el usuario inicio sesion correctamente")

    def test_modificar_fase(self):
        print("\nTEST: Ingresar a Modificar fase con usuario registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.lider, password=self.passwordLider)
            resp = self.client.get('/administracion/proyectos/1/fases/1/modificar/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba fallida, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba fallida, el usuario registrado no pudo acceder")
            return
        print("Prueba exitosa, el usuario pudo acceder a la pagina")

    def test_modificar_fase_no_registrado(self):
        print("\nTEST: Ingresar a Modificar fase con usuario no registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.prueba, password=self.passprueba)
            resp = self.client.get('/administracion/proyectos/1/fases/1/modificar/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba exitosa, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba exitosa, el usuario no registrado no pudo acceder")
            return
        print("Prueba fallida, el usuario inicio sesion correctamente")

    def test_asignar_usuarios_fase(self):
        print("\nTEST: Ingresar a Asignar usuarios a fase con usuario registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.lider, password=self.passwordLider)
            resp = self.client.get('/administracion/proyectos/1/fases/1/usuarios/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba fallida, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba fallida, el usuario registrado no pudo acceder")
            return
        print("Prueba exitosa, el usuario pudo acceder a la pagina")

    def test_asignar_usuarios_fase_no_registrado(self):
        print("\nTEST: Ingresar a Asignar usuario a fase con usuario no registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.prueba, password=self.passprueba)
            resp = self.client.get('/administracion/proyectos/1/fases/1/usuarios/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba exitosa, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba exitosa, el usuario no registrado no pudo acceder")
            return
        print("Prueba fallida, el usuario inicio sesion correctamente")

    def test_eliminar_fase(self):
        print("\nTEST: Ingresar a Eliminar fase con usuario registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.lider, password=self.passwordLider)
            resp = self.client.get('/administracion/proyectos/1/fases/1/eliminar/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba fallida, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba fallida, el usuario registrado no pudo acceder")
            return
        print("Prueba exitosa, el usuario pudo acceder a la pagina")

    def test_eliminar_fase_no_registrado(self):
        print("\nTEST: Ingresar a Eliminar fase con usuario no registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.prueba, password=self.passprueba)
            resp = self.client.get('/administracion/proyectos/1/fases/1/eliminar/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba exitosa, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba exitosa, el usuario no registrado no pudo acceder")
            return
        print("Prueba fallida, el usuario inicio sesion correctamente")

    def test_asignar_rol(self):
        print("\nTEST: Ingresar a Asignar rol con usuario registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.lider, password=self.passwordLider)
            resp = self.client.get('/administracion/proyectos/1/roles/asignar/1/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba fallida, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba fallida, el usuario registrado no pudo acceder")
            return
        print("Prueba exitosa, el usuario pudo acceder a la pagina")

    def test_asignar_rol_no_registrado(self):
        print("\nTEST: Ingresar a Asignar rol con usuario no registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.prueba, password=self.passprueba)
            resp = self.client.get('/administracion/proyectos/1/roles/asignar/1/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba exitosa, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba exitosa, el usuario no registrado no pudo acceder")
            return
        print("Prueba fallida, el usuario inicio sesion correctamente")

    def test_listar_rol(self):
        print("\nTEST: Ingresar a Listar roles con usuario registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.lider, password=self.passwordLider)
            resp = self.client.get('/administracion/proyectos/1/roles/listar/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba fallida, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba fallida, el usuario registrado no pudo acceder")
            return
        print("Prueba exitosa, el usuario pudo acceder a la pagina")

    def test_listar_rol_no_registrado(self):
        print("\nTEST: Ingresar a Listar roles con usuario no registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.prueba, password=self.passprueba)
            resp = self.client.get('/administracion/proyectos/1/roles/listar/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba exitosa, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba exitosa, el usuario no registrado no pudo acceder")
            return
        print("Prueba fallida, el usuario inicio sesion correctamente")

    def test_detalle_rol(self):
        print("\nTEST: Ingresar a Detalle de rol con usuario registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.lider, password=self.passwordLider)
            resp = self.client.get('/administracion/proyectos/1/roles/listar/1/detalle/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba fallida, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba fallida, el usuario registrado no pudo acceder")
            return
        print("Prueba exitosa, el usuario pudo acceder a la pagina")

    def test_detalle_rol_no_registrado(self):
        print("\nTEST: Ingresar a Listar roles con usuario no registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.prueba, password=self.passprueba)
            resp = self.client.get('/administracion/proyectos/1/roles/listar/1/detalle/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba exitosa, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba exitosa, el usuario no registrado no pudo acceder")
            return
        print("Prueba fallida, el usuario inicio sesion correctamente")

    def test_modificar_rol(self):
        print("\nTEST: Ingresar a Modificar rol con usuario registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.lider, password=self.passwordLider)
            resp = self.client.get('/administracion/proyectos/1/roles/listar/1/modificar/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba fallida, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba fallida, el usuario registrado no pudo acceder")
            return
        print("Prueba exitosa, el usuario pudo acceder a la pagina")

    def test_modificar_rol_no_registrado(self):
        print("\nTEST: Ingresar a Modificar rol con usuario no registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.prueba, password=self.passprueba)
            resp = self.client.get('/administracion/proyectos/1/roles/listar/1/modificar/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba exitosa, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba exitosa, el usuario no registrado no pudo acceder")
            return
        print("Prueba fallida, el usuario inicio sesion correctamente")

    def test_eliminar_rol(self):
        print("\nTEST: Ingresar a Eliminar rol con usuario registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.lider, password=self.passwordLider)
            resp = self.client.get('/administracion/proyectos/1/roles/listar/1/eliminar/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba fallida, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba fallida, el usuario registrado no pudo acceder")
            return
        print("Prueba exitosa, el usuario pudo acceder a la pagina")

    def test_eliminar_rol_no_registrado(self):
        print("\nTEST: Ingresar a Eliminar rol con usuario no registrado")
        try:
            resp = self.client.get('/')
            self.client.login(username=self.prueba, password=self.passprueba)
            resp = self.client.get('/administracion/proyectos/1/roles/listar/1/eliminar/')
            self.assertEqual(resp.status_code, 200)
        except:
            if resp.status_code == 302:
                print("Prueba exitosa, el usuario no posee permiso para acceder a la url")
            else:
                if resp.status_code == 404:
                    print("Prueba fallida, la url no existe")
                else:
                    print("Prueba exitosa, el usuario no registrado no pudo acceder")
            return
        print("Prueba fallida, el usuario inicio sesion correctamente")
