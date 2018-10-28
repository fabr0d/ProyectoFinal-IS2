from django.contrib import admin

from .models import Question,Choice,Usuario,Ingreso,Egreso,Categoria

# Register your models here.

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Usuario)
admin.site.register(Ingreso)
admin.site.register(Egreso)
admin.site.register(Categoria)
