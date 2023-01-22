from django.contrib import admin
#Добавляем поля в админ-панель
from .models import AboutSummit, Country, MountainRange, Profile, MountainImages

#Добавляем поля в админ-панель
#admin.site.register(AboutSummit)
admin.site.register(Country)
admin.site.register(MountainRange)
admin.site.register(Profile)

class MountainImageAdmin(admin.StackedInline):
    model = MountainImages

@admin.register(AboutSummit)
class AboutSummitAdmin(admin.ModelAdmin):
    inlines = [MountainImageAdmin]
    list_display = ('pk', 'title', 'high',)
    search_fields = ('title',)
    list_filter = ('country',)

    class Meta:
       model = AboutSummit

@admin.register(MountainImages)
class MountainImageAdmin(admin.ModelAdmin):
    pass