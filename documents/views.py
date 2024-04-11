from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import DocumentForm
from .models import Document
from django.contrib.auth.decorators import login_required
from .utils import send_otp
from datetime import datetime
from django.utils import timezone
import pyotp

import qrcode
from io import BytesIO
from .utils import to_base64
from django.http import HttpResponseBadRequest
# Create your views here.





def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })

    else:
        username = request.POST.get('username')
        request.session['username'] = username

        password = request.POST.get('password')
        code = request.POST.get('code')
        if not username or not password:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o Contraseña Incorrecta'
            })

        user = authenticate(request, username=username,  email=username, password=password)
        if user is not None:
            key = user.last_name
            totp = pyotp.TOTP(key)
            totp.verify(code)
            
            if totp.verify(request.POST.get('code')):
                login(request, user)
                if user.is_staff:
                    return redirect('documents')
                else:
                    return redirect('mydocuments')
            else:
                # print('En el ELSEEEEE')

                return render(request, 'signin.html', {
                    'form': AuthenticationForm,
                    'error': 'Codigo Invalido'
                })
        else:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Error en las credenciales'
            })
            


def otp(request):
    if request.method == 'GET':
        # Llama a send_otp y guarda el valor en qr_text
        key, uri = send_otp()

        qr_text = uri
        # print(qr_text)
        # Genera el código QR
        qr = qrcode.make(qr_text)
        # Convierte el código QR en bytes
        qr_bytes = BytesIO()
        qr.save(qr_bytes)
        qr_bytes = qr_bytes.getvalue()
        # Convierte los bytes en base64
        qr_base64 = to_base64(qr_bytes)
        return render(request, 'otp.html', {'qr_base64': qr_base64})
    else:
        key, uri = send_otp()
        totp = pyotp.TOTP(key)
        # print(totp.verify(request.POST.get('otp')))
        if totp.verify(request.POST.get('otp')):

            # Recuperar el nombre de usuario
            username = request.session.get('username')
            lastname = request.session.get('code')

            if username:
                user = User.objects.create_user(
                    username=username, email=username, password=request.session.get('password'), last_name=key,)
                # user.otp_uri = uri
                user.save()
                login(request, user)
                return render(request, 'documents.html', {'user': user})
            else:
                return HttpResponse("Error: Nombre de usuario no encontrado en la sesión.")

            # # user = get_object_or_404(User, username=username)
            # # login(request, user)
            # return redirect('home')
        else:
            return render(request, 'signup.html', {
                'form': AuthenticationForm,
                'error': 'Codigo Invalido'
            })
        # Inicia sesión y redirige a la página principal


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                request.session['username'] = request.POST['username']
                request.session['password'] = request.POST['password1']
                # print(request.session['password'])
                # regisrter user
                # user = User.objects.create_user(
                #     username=request.POST['username'], password=request.POST['password1'])

                # user.save()
                # login(request, user)
                # return redirect('documents')
                return redirect('otp')
                # return HttpResponse('Usuario Creado')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': "Usuario ya existe",

                })

        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': "Contrasenas no coinciden",

        })


@login_required
def documents(request):
    documents = Document.objects.all()
    # documents = Document.objects.filter(remitente=request.user) PARA LISTAR DOCUMENTOS DEL USUARIO ACTUAL
    # documents = Document.objects.all()
    return render(request, 'documents.html', {
        'documents': documents
    })


@login_required
def documents_pending(request):
    documents = Document.objects.filter(aprobado=False)
    # documents = Document.objects.filter(remitente=request.user) PARA LISTAR DOCUMENTOS DEL USUARIO ACTUAL
    # documents = Document.objects.all()
    return render(request, 'documents.html', {
        'documents': documents
    })


@login_required
def documents_approved(request):
    documents = Document.objects.filter(aprobado=True)
    # documents = Document.objects.filter(remitente=request.user) PARA LISTAR DOCUMENTOS DEL USUARIO ACTUAL
    # documents = Document.objects.all()
    return render(request, 'documents.html', {
        'documents': documents
    })
    
@login_required
def documents_remitent(request):
    documents = Document.objects.filter(remitente=request.user)
    # documents = Document.objects.filter(remitente=request.user) PARA LISTAR DOCUMENTOS DEL USUARIO ACTUAL
    # documents = Document.objects.all()
    return render(request, 'documents.html', {
        'documents': documents
    })


@login_required
def signout(request):
    logout(request)
    return render(request, 'home.html')


@login_required
def create_document(request):
    if request.method == 'GET':
        return render(request, 'create_document.html', {
            'form': DocumentForm
        })
    else:
        try:
            form = DocumentForm(request.POST, request.FILES)
            new_document = form.save(commit=False)
            archivo_pdf = request.FILES['archivo']
            new_document.archivo = archivo_pdf
            new_document.remitente = request.user
            # print(request.user)
            new_document.save()
            user = get_object_or_404(User, username=request.user)
            # print(user)

            if user.is_staff:
                return redirect('documents')
            else:
                return redirect('mydocuments')

            
        except ValueError:
            return render(request, 'create_document.html', {
                'form': DocumentForm,
                'error': 'Datos Invalidos'
            })


@login_required
def document_detail(request, document_id):
    # document = get_object_or_404(Document, pk=document_id, remitente=request.user) Restringe el update a las tareas del usuario actual
    document = get_object_or_404(Document, pk=document_id)

    if request.method == 'GET':
        form = DocumentForm(instance=document)
        return render(request, 'document_detail.html', {
            'document': document,
            'form': form
        })
    else:
        try:
            form = DocumentForm(request.POST, request.FILES, instance=document)
            # Si se ha proporcionado un nuevo archivo PDF actualiza el campo archivo del documento
            if 'archivo' in request.FILES:
                document.archivo = request.FILES['archivo']
            form.save()
            return redirect('documents')
        except ValueError:
            return render(request, 'document_detail.html', {
                'document': document,
                'form': form,
                'error': 'Error al Actualizar el Documento'
            })


@login_required
def approved_document(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    if request.method == 'POST':
        document.aprobado = True
        document.aprobador = request.user
        document.save()
        return redirect('documents')


@login_required
def deleted_document(request, document_id):
    document = get_object_or_404( Document, pk=document_id, remitente=request.user)
    if request.method == 'POST':
        document.delete()
        return redirect('mydocuments')


login_required


def descargar_archivo(request, id):
    archivo = get_object_or_404(Document, pk=id)
    response = HttpResponse(
        archivo.archivo, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{archivo.archivo}"'
    return response
