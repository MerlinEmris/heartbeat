from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Site

admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()  # type: Set[str]

        if not is_superuser:
            disabled_fields |= {
                'username',
                'is_superuser',
                'user_permissions',
            }

        # Prevent non-superusers from editing their own permissions
        if (
            not is_superuser
            and obj is not None
            and obj == request.user
        ):
            disabled_fields |= {
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form


# Register your models here.
@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url', 'is_active')
    list_display_links = ('id', 'name')
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    search_fields = ('name', 'url')
    ordering = ('-id',)
    save_as = True
    exclude = ('user',)


    def get_queryset(self, request):
        qs = super(SiteAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)