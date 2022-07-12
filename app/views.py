
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

#Página Inicial
def home(request):
   return render(request, 'home.html')

#Criação do usuário   
def create(request):
   return render(request, 'create.html')

#Inserção do usuário no banco de dados 
def store(request):
   if (request.method == 'POST'):
      data = {}
      if(request.POST['senha'] != request.POST['repsenha']):
         data['msg'] = 'Senhas Diferentes'
         data['alertaerr'] = 'alert-danger'
         return render(request, 'create.html', data)
      else:
         try:
            user = User.objects.create_user(request.POST['nome'], request.POST['email'], request.POST['senha'])
            user.pais= request.POST['country']
            user.estado= request.POST['es']
            user.municipio= request.POST['municipio']
            user.cep= request.POST['cep']
            user.rua= request.POST['rua']
            user.num= request.POST['num']
            user.complemento= request.POST['complemento']
            user.cpf= request.POST['CPF']
            user.pis= request.POST['PIS']
            user.save()
            data['msg'] = 'Usuário cadastrado com sucesso'
            data['alertaerr'] = 'alert-success'
            data ['formsome'] = 1
            return render(request, 'create.html', data)
         except:
            data['error'] = 'CPF, PIS ou E-mail já cadastrado no sistema'
            return render(request, 'create.html', data)
   else:
      return redirect('/')




#Processa o Login   
def log(request):
   data = {}
   try:
      user = User.objects.get(cpf=request.POST['user'])
      usernames = user.username
      user = authenticate(username=usernames, password=request.POST['senha'])
      if user is not None:
          login(request, user)
          data['msg'] = user.username 
          return render(request, 'dashboard.html', data)
      else:
         data['msg'] =  'Usuário ou senha errado'
         data['alertaerr'] = 'alert-danger' 
         return render(request, 'painel.html', data)
   except:
      try:
         user = User.objects.get(email=request.POST['user'])
         usernames = user.username
         user = authenticate(username=usernames, password=request.POST['senha'])
         if user is not None:
            login(request, user)
            data['msg'] = user.username 
            return render(request, 'dashboard.html', data)
         else:
            data['msg'] =  'Usuário ou senha errado'
            data['alertaerr'] = 'alert-danger' 
            return render(request, 'painel.html', data)
      except:
         try:
            user = User.objects.get(pis=request.POST['user'])
            usernames = user.username
            user = authenticate(username=usernames, password=request.POST['senha'])
            if user is not None:
               login(request, user)
               data['msg'] = user.username 
               return render(request, 'dashboard.html', data)
            else:
               data['msg'] =  'Usuário ou senha errado'
               data['alertaerr'] = 'alert-danger' 
               return render(request, 'painel.html', data)
         except:
            data['msg'] =  'Usuário ou senha errado'
            data['alertaerr'] = 'alert-danger' 
            return render(request, 'painel.html', data)
#Página de login
def painel(request):
   return render(request, 'painel.html')


#Página Inicial do Dashboard
def dashboard(request):
   if (request.user.is_authenticated):
      data = {}
      data['msg'] = request.user.username
      return render(request, 'dashboard.html', data)
   else:
      return redirect('/')
 

#Logout do usuário 
def logout_(request):
   logout(request)
   #return render(request, 'home.html')
   return redirect('/')


#Altera dados cadastrais
def modif(request):
   data = {}
   user = User.objects.get(username=request.user.username)
   data['user'] = user.username
   data['email'] = user.email
   data['pais'] = user.pais
   data['es'] = user.estado
   data['municipio'] = user.municipio
   data['cep'] = user.cep
   data['rua'] = user.rua
   data['num'] = user.num
   data['complemento'] = user.complemento
   data['cpf'] = user.cpf
   data['pis'] = user.pis
   if (request.method == 'POST'):
      if(request.POST['senha'] != request.POST['repsenha']):
         data['msg'] = 'Senhas Diferentes'
         data['alertaerr'] = 'alert-danger'
         return render(request, 'modif.html', data)
      else:
         user.username = request.POST['nome']
         user.email = request.POST['email']
         user.pais= request.POST['country']
         user.estado= request.POST['es']
         user.municipio= request.POST['municipio']
         user.cep= request.POST['cep']
         user.rua= request.POST['rua']
         user.num= request.POST['num']
         user.complemento= request.POST['complemento']
         user.cpf= request.POST['CPF']
         user.pis= request.POST['PIS']
         user.set_password(request.POST['senha'])
         user.save()
         logout(request)
         return render(request, 'painel.html')
   else:
      data = {}
      data['user'] = user.username
      data['email'] = user.email
      data['pais'] = user.pais
      data['es'] = user.estado
      data['municipio'] = user.municipio
      data['cep'] = user.cep
      data['rua'] = user.rua
      data['num'] = user.num
      data['complemento'] = user.complemento
      data['cpf'] = user.cpf
      data['pis'] = user.pis
      return render(request, 'modif.html', data)

#Logout do usuário 
def delet(request):
   if (request.user.is_authenticated):
      user = User.objects.get(username=request.user.username)
      logout(request)
      user.delete()
      return redirect('/')
   else:
      return redirect('/')