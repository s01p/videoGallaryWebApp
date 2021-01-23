from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Photo,Photoa


admin.site.register(Photo)

@admin.register(Photoa)
class PhotoaAdmin(ImportExportModelAdmin):
    pass
