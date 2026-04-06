from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, logout as logout_view, login as auth_login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from .models import Bolo, Profile, Order, OrderItem
from decimal import Decimal
from django.db import transaction
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model
from .trie_store import get_trie
import json


@login_required
def home(request):
    return render(request, 'home.html')


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Nome de usuário ou senha incorretos")

    return render(request, 'login.html')


def logout(request):
    logout_view(request)
    return redirect('login')


def cadastro(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Usuário já existe")
            else:
                user = User.objects.create_user(
                    username=username, password=password)
                user.save()
                messages.success(request, "Usuário cadastrado com sucesso")
                return redirect('login')
        else:
            messages.error(request, "As senhas não coincidem")
    return render(request, 'cadastro.html')


@login_required
def catalogo(request):
    bolos = Bolo.objects.all()  # Busca todos os bolos do banco de dados
    return render(request, 'catalogo.html', {'bolos': bolos})


@login_required
def basket(request):
    profile = Profile.objects.get(user=request.user)
    carrinho = profile.listar_carrinho()
    total = profile.obter_valor_total()
    return render(request, 'basket.html', {'carrinho': carrinho, 'total': total})


@login_required
def admin(request):
    return render(request, 'admin.html')


@login_required
@require_POST
def adicionar_ao_carrinho(request):
    data = json.loads(request.body)
    bolo_id = data['bolo_id']
    tamanho = data['tamanho'].upper()

    bolo = get_object_or_404(Bolo, id=bolo_id)

    # Obtém o perfil do usuário
    profile = Profile.objects.get(user=request.user)

    profile.adicionar_bolo_ao_carrinho(bolo, tamanho)

    return JsonResponse({'success': True})


@login_required
def obter_carrinho(request):
    profile = Profile.objects.get(user=request.user)
    carrinho = []
    for item in profile.listar_carrinho():
        bolo = Bolo.objects.get(id=item['bolo_id'])
        carrinho.append({
            'bolo_nome': bolo.sabor,
            'descricao': bolo.descricao,
            'imagem_url': bolo.imagem_url,
            'tamanho': item['tamanho'],
            'preco': item['preco'],
            'quantidade': item['quantidade']
        })
    total = profile.obter_valor_total()
    return JsonResponse({'carrinho': carrinho, 'total': str(total)})


def listar_carrinho(request):
    profile = Profile.objects.get(user=request.user)
    return JsonResponse({'carrinho': profile.listar_carrinho()})


@login_required
def finalizar_compra(request):
    profile = request.user.profile
    carrinho = profile.listar_carrinho()

    if not carrinho:
        return JsonResponse({'success': False, 'error': 'Carrinho vazio'})

    with transaction.atomic():
        order = Order.objects.create(
            user=request.user, total=Decimal('0.00'), status='COMPLETED')
        total = Decimal('0.00')
        for item in carrinho:
            bolo = Bolo.objects.get(id=item['bolo_id'])
            preco = Decimal(str(item.get('preco', 0)))
            quantidade = int(item.get('quantidade', 1))
            OrderItem.objects.create(
                order=order, bolo=bolo, tamanho=item['tamanho'], preco=preco, quantidade=quantidade)
            total += preco * quantidade

        order.total = total
        order.save()

        profile.limpar_carrinho()

    return JsonResponse({'success': True, 'order_id': order.id})


@login_required
def editar_perfil(request):
    if request.method == 'POST':
        user = request.user
        novo_nome = request.POST.get('name')
        nova_senha = request.POST.get('newPassword')

        if novo_nome:
            user.username = novo_nome

        if nova_senha:
            user.set_password(nova_senha)

        user.save()

        logout(request)

        messages.success(
            request, 'Seu perfil foi atualizado com sucesso. Por favor, faça login com suas novas credenciais.')

        return redirect('login')

    return render(request, 'editar_perfil.html')


@login_required
def deletar_perfil(request):
    if request.method == 'POST':
        user = request.user
        user.delete()

        messages.success(request, 'Perfil excluído com sucesso!')
        return redirect('cadastro')

    return redirect('adm')


@login_required
@require_GET
def autocomplete(request):
    # Endpoint de autocomplete via Trie. GET /autocomplete/?q=<prefixo>
    # Retorna {"suggestions": ["Bolo A", ...]} — máx 8 resultados.
    prefix = request.GET.get('q', '').strip()
    if not prefix:
        return JsonResponse({'suggestions': []})

    trie = get_trie()
    resultados = trie.starts_with(prefix, limit=8)

    sugestoes = []
    for item in resultados:
        if isinstance(item, dict):
            label = item.get('label') or item.get(
                'nome') or item.get('sabor') or str(item)
        else:
            label = str(item)
        if label and label not in sugestoes:
            sugestoes.append(label)

    return JsonResponse({'suggestions': sugestoes})
