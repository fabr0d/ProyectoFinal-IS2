from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Usuario)
admin.site.register(Ingreso)
admin.site.register(Egreso)
admin.site.register(Categoria)
admin.site.register(ControlEgreso)
