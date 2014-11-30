from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from models import Publicacion, Comentario
# django login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
# only registered users in internal User class can login
from django.contrib.auth.models import User
#
from django.template import RequestContext


def login_view(request):
    state = "Ingrese sus credenciales para comenzar"
    login_ok = None

    username = password = ""
    if request.POST:
        # get user and pass and validate them
        username = request.POST.get("username")
        password = request.POST.get("password")
        #authenticate
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                state = "El usuario SI existe y esta activo"
                login_ok = True
                login(request, user)
                return HttpResponseRedirect("/")
        else:
            state = "Credenciales no validas!"
            login_ok = False
    # display login form, no post and get requests detected
    return render_to_response("login.html", {"state": state, "login_ok": login_ok})

#serializar una lista de objeto
from django.core import serializers
import json
@login_required(login_url="/login/")
def index_view(request):
    listpost=Publicacion.objects.all()

    if request.POST:
        # get user and pass and validate them
        publi = request.POST.get("publi")
        if request.user.is_authenticated():
            actualuser = request.user
        usu = Publicacion(idPubli=None, contenidoPubli=publi, numeroLikesPubli=0,
                          fechaPubli='aa', publicadorPubli=actualuser)
        usu.save()
        return HttpResponseRedirect("/")

    return render_to_response('index.html', {'listpost':listpost}, context_instance=RequestContext(request))










def registro_view(request):
    if request.POST:
        # get user and pass and validate them
        name = request.POST.get("name")
        username = request.POST.get("email")
        pass1 = request.POST.get("pass1")
        pass2 = request.POST.get("pass2")
        #system user(username, email, password)
        usu = User.objects.create_user(name, username, pass1)
        usu.is_staff = False
        usu.save()
        return HttpResponseRedirect("/")
    return render_to_response('registro.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")



def getdata_view(request):
    return render_to_response('aaa.html')

#serializar una lista de objeto
from django.core import serializers
import json
def verjson_view(request):
    try:
        if request.method=='GET' or request.is_ajax():
            #atender peticiones GET o AJAX
            lista_posts = Publicacion.objects.all()
            return HttpResponse(serializers.serialize('json', lista_posts), content_type = 'application/json')
        else:
            return HttpResponse(json.dumps({"error": 'Peticion no valida'}))
    except Exception, e:
        #retornar en formato json ese diccionario si se presenta un error
        return HttpResponse(json.dumps({"error": str(e)}))



