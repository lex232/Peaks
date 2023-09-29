from django.contrib import admin
from .models import AboutSummit, Country, MountainRange
from .models import Profile, MountainImages, Post


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


admin.site.register(Country)
admin.site.register(MountainRange)
admin.site.register(Profile)
admin.site.register(Post)
