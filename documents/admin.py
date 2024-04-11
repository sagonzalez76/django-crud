from django.contrib import admin


from .models import Document

# Register your models here.


class DocumentAdmin(admin.ModelAdmin):
    readonly_fields = ("fecha_creacion",)


admin.site.register(Document, DocumentAdmin)
