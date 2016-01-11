from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from Web.models import New, Comment, Section, User, Vote
from django.template import loader, Context, RequestContext
from PIL import Image
from Web.forms import NewForm, CommentForm, UserForm
import time

# Create your views here.

def index(request):
	sections = Section.objects.all().order_by('name')
	news = New.objects.all().order_by('time').reverse()
	for x in news:
		x.description = x.description[:500]
		if x.image:
			x.image = x.image.url[11:]
	plantilla = loader.get_template('index.html')
	if 'Logueado' in request.session:
		userName = request.session['Logueado']
		contexto = RequestContext(request, {'news': news, 'sections': sections, 'userName':userName } )
	else:
		contexto = RequestContext(request, {'news': news, 'sections': sections } )
	return HttpResponse(plantilla.render(contexto))


def new(request, noticia_id, year, month, day):
	try:
		#DATOS AUXILIARES
		sections = Section.objects.all().order_by('name')
		newAux = New.objects.get(id=noticia_id)
		if int(year) != int(newAux.date.year) or int(month) != int(newAux.date.month) or int(day) != int(newAux.date.day):
			raise Http404
		comments = Comment.objects.filter(new=noticia_id).order_by('time').reverse()
		if int(newAux.punctuation) !=0:
			newAux.punctuation = float(newAux.punctuation)/float(newAux.votes)
		if  newAux.image:
			newAux.image = newAux.image.url[11:]
		plantilla = loader.get_template('new.html')

			# FORM PARA COMENTARIOS
		if 'Logueado' in request.session:
			userName = request.session['Logueado']
			autor=User.objects.get(nick=userName)
			if request.method == 'POST':
				
				tiempo = time.time()
				comment = Comment(author=autor,new=newAux, time=tiempo )
				form = CommentForm(request.POST, request.FILES, instance=comment)
				
				if form.is_valid():
					form.save()
			try:
				voto=Vote.objects.get(author=autor.id, new=newAux.id)
			except Vote.DoesNotExist:
				voto=None
			form = CommentForm()
			contexto = RequestContext(request, {'new': newAux, 'sections': sections, 'comments':comments, 'userName':userName, 'form':form, 'voto':voto } )
		else:
			contexto = RequestContext(request, {'new': newAux, 'sections': sections, 'comments':comments } )

		
		return HttpResponse(plantilla.render(contexto))

	except New.DoesNotExist or Comment.DoesNotExist or User.DoesNotExist or Vote.DoesNotExist:
		raise Http404
	

def filter(request, section_name):
	try:
		sectionAux = Section.objects.get(name=section_name)
		sections = Section.objects.all().order_by('name')
		news = New.objects.filter(section=sectionAux.id).order_by('time').reverse()
		for x in news:
			x.description = x.description[:500]
			if x.image:
				x.image = x.image.url[11:]
		plantilla = loader.get_template('index.html')
		if 'Logueado' in request.session:
			userName = request.session['Logueado']
			contexto = RequestContext(request, {'news': news, 'sections': sections, 'userName':userName, "filtrado":section_name } )
		else:
			contexto = RequestContext(request, {'news': news, 'sections': sections, "filtrado":section_name } )
	except Section.DoesNotExist or New.DoesNotExist:
		raise Http404
	return HttpResponse(plantilla.render(contexto))

def profile(request):
	try:
		sections = Section.objects.all().order_by('name')
		plantilla = loader.get_template('profile.html')
		if 'Logueado' in request.session:
			userName = request.session['Logueado']
			usuario = User.objects.get(nick=userName)
			if  usuario.imagen:
				image = usuario.imagen.url[11:]
			else:
				image = 'photos/users/default.png'
			contexto = RequestContext(request, {'sections': sections, 'usuario':usuario, 'userName':userName, 'image':image } )
		else:
			contexto = RequestContext(request, {'sections': sections } )
	except Section.DoesNotExist or User.DoesNotExist:
		raise Http404
	return HttpResponse(plantilla.render(contexto))

def login(request):
	username = request.POST['nick']
	password = request.POST['pass']
	redirigir = request.META.get('HTTP_REFERER')
	try:
		aux = User.objects.get(nick=username, password=password)
	except User.DoesNotExist:
		aux = None
	if aux is not None:
		request.session['Logueado']=username
		return render(request, 'accepted.html', {'redirigir':redirigir})
	else:
		return render(request, 'denied.html', {'redirigir':redirigir})

def logout(request):
	del request.session['Logueado']
	redirigir = request.META.get('HTTP_REFERER')
	if 'Logueado' in request.session:
		return render(request, 'denied.html', {'redirigir':redirigir})
	else:
		return render(request, 'accepted.html', {'redirigir':redirigir})

def register(request):
	try:
		sections = Section.objects.all().order_by('name')
		plantilla = loader.get_template('register.html')

		if request.method == 'POST':
			form = UserForm(request.POST, request.FILES)
			if form.is_valid():
				form.save()
			return HttpResponseRedirect('/news/')
		else:	
			if 'Logueado' in request.session:
				userName = request.session['Logueado']
				contexto = RequestContext(request, {'sections': sections, 'userName':userName } )
			else:
				form = UserForm()
				contexto = RequestContext(request, {'sections': sections, 'form':form } )
	except New.DoesNotExist or Comment.DoesNotExist or Section.DoesNotExist:
		raise Http404
	return HttpResponse(plantilla.render(contexto))


def modify_user(request):
	try: 
		sections = Section.objects.all().order_by('name')
		if 'Logueado' in request.session:
			userName = request.session['Logueado']
			usuario = User.objects.get(nick=userName)
			contexto = RequestContext(request, {'sections': sections, 'userName':userName, 'usuario':usuario } )
		else:
			contexto = RequestContext(request, {'sections': sections } )
		plantilla = loader.get_template('modify.html')
	except Section.DoesNotExist or User.DoesNotExist:
		raise Http404	
	return HttpResponse(plantilla.render(contexto))

def send_modification(request):
	userName = request.session['Logueado']
	password1 = request.POST['password1']
	password2 = request.POST['password2']
	email = request.POST['email']
	sections = Section.objects.all().order_by('name')

	try:
		usuario = User.objects.get(nick=userName)
	except User.DoesNotExist:
		usuario = None
	if usuario is None:
		mensaje="Usuario sin registrar"
		return render(request, 'modify.html', {'mensaje':mensaje, 'userName':userName, 'usuario':usuario, 'sections':sections})
	if password1 != password2:
		mensaje="Las contrasenas no coinciden."
		return render(request, 'modify.html', {'mensaje':mensaje, 'userName':userName, 'usuario':usuario, 'sections':sections})
	if email is '' or password1 == '' or password2 == '':
		mensaje="Campos obligatorios sin rellenar"
		return render(request, 'modify.html', {'mensaje':mensaje, 'userName':userName, 'usuario':usuario, 'sections':sections})

	usuario.password=request.POST['password1']
	usuario.email=request.POST['email']
	usuario.name=request.POST['name']
	usuario.surname=request.POST['surname']
	usuario.age=request.POST['age']

	usuario.save()
	return HttpResponseRedirect('/news/profile/')


def write_new(request):
	try:
		plantilla = loader.get_template('write.html')
		if request.method == 'POST':

			if 'Logueado' in request.session:
				userName = request.session['Logueado']
				usuario = User.objects.get(nick=userName)
				tiempo = time.time()
				new=New(author=usuario, time=tiempo)	
			else:
					raise Http404
			form = NewForm(request.POST, request.FILES, instance=new)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/news/')
		else:
			sections = Section.objects.all().order_by('name')
			form = NewForm()
			if 'Logueado' in request.session:
				userName = request.session['Logueado']
				usuario = User.objects.get(nick=userName)
				contexto = RequestContext(request, {'sections': sections, 'userName':userName, 'usuario':usuario, 'form':form } )
			else:
				contexto = RequestContext(request, {'sections': sections, 'form':form } )
	except Section.DoesNotExist:
		raise Http404
	return HttpResponse(plantilla.render(contexto))

def vote(request, noticia_id):
	new = New.objects.get(pk=noticia_id)
	aux = request.POST['vote']
	if 'Logueado' in request.session:
		userName = request.session['Logueado']
		usuario = User.objects.get(nick=userName)
	voto = Vote(author=usuario, new=new, calification=aux)
	new.punctuation =int(new.punctuation)+int(aux)
	new.votes=int(new.votes)+1
	voto.save()
	new.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))