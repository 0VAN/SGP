from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
# Create your tests here.

class TestUser(TestCase):
    #Test: el numero de usuarios debe ser 0
    def test_numero_elementos(self):
        self.assertEqual(0,len(User.objects.all()))

class TestUser2(TestCase):
    #Test: al insertar un usuario a la bd debe incrementar el numero de elementos
    fixtures = ['fixtures/Usuarios.json']
    def test_numero_elementos(self):
        self.assertEqual(1,len(User.objects.all()))

class TestLogin(TestCase):
    usuario='sgp'
    password='sgparj'
    #cargamos los usuarios
    fixtures = ['fixtures/Usuarios.json']
    def test_login_usuario(self):
        # vamos a la pantalla de inicio
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        # logueamos con el usuario sgp
        login = self.client.login(username=self.usuario, password=self.password)
        self.assertTrue(login)
        # sitodo sale bien pasamos a la interfaz de administracion
        resp = self.client.get('/administracion/')
        self.assertEqual(resp.status_code, 200)

    def test_usuario_no_registrado(self):
        prueba ='hola'
        passprueba ='hola'
        # vamos a la pantalla de inicio
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        # logueamos con el usuario hola
        login = self.client.login(username=prueba, password=passprueba)
        self.assertFalse(login)
        # si el usuario no esta registrado, fallara a la hora de obtener la pagina administracion
        resp = self.client.get('/administracion/')
        self.assertEqual(resp.status_code, 302)

class TestCrearUsuario(TestCase):
    def crear_correctamente(self):
        # Logueamos
        login = self.client.login(username=self.usuario, password=self.password)
        self.assertTrue(login)
        resp = self.client.get('/nuevousuario/')
        self.assertEqual(resp.status_code, 200)
        nombre_usuario ='prueba'
        password_usuario ='prueba'
        user1 = User.objects.create(username=nombre_usuario, password=password_usuario)

