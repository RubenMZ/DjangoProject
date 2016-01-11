from django.forms.extras.widgets import SelectDateWidget
from django.forms import ModelForm
from django import forms
from Web.models import Comment, New, User

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        
        exclude = ['author', 'date', 'time', 'new']
        fields = ['description']
        
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['description'].label = ""

class NewForm(ModelForm):
    class Meta:
        model = New
        
        # exclude = ['user', 'bottle', ]
        # fields = ['pub_date', 'headline', 'content', 'reporter']
        fields = ['title', 'description', 'section', 'image']
        exclude = ['author', 'date', 'time', 'votes', 'punctuation']
    def __init__(self, *args, **kwargs):
        super(NewForm, self).__init__(*args, **kwargs)
        self.fields['section'].label = "Secciones (mantener ctrl y seleccionar)"
        self.fields['title'].label = "Titulo"
        self.fields['description'].label = "Descripcion"
        self.fields['image'].label = "Imagen"


class UserForm(ModelForm):
    class Meta:
        model = User
        
        widgets = {
            'password': forms.PasswordInput(),
        }
        fields = ['nick', 'email', 'password', 'name', 'surname', 'age', 'gender', 'imagen']
        exclude = ['vip']
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['nick'].label = "Usuario"
        self.fields['email'].label = "Email"
        self.fields['password'].label = "Contrasena"
        self.fields['name'].label = "Nombre"
        self.fields['surname'].label = "Apellidos"
        self.fields['age'].label = "Edad"
        self.fields['gender'].label = "Genero (Masculino/Femenino)"
