from django.contrib import admin
from .models import *

admin.site.register(Cliente)
admin.site.register(Empresa)
admin.site.register(Categoria)
admin.site.register(Produto)
admin.site.register(Servico)
admin.site.register(OrdemServico)
