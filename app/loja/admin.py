from django.contrib import admin
from .models import Bolo
from .models import Order, OrderItem

# Registrar o modelo Bolo no admin
@admin.register(Bolo)
class BoloAdmin(admin.ModelAdmin):
    # Exibe colunas adicionais, incluindo os preços para cada tamanho
    list_display = ('sabor', 'descricao', 'imagem_url', 'preco_pequeno', 'preco_medio', 'preco_grande')
    
    # Permite pesquisar pelo sabor
    search_fields = ('sabor',)
admin.site.register(Order)
admin.site.register(OrderItem)
