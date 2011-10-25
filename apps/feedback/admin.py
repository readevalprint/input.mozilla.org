from django.contrib import admin

from .models import Opinion, Term, VersionCount


class OpinionAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('_type', 'truncated_description', 'created',
                    'product_name', 'version', 'platform_name', 'locale',
                    'manufacturer', 'device')
    list_display_links = ('truncated_description',)
    list_filter = ('_type', 'version', 'platform', 'locale', 'manufacturer',
                   'device')
    ordering = ('-created',)
    search_fields = ['description']

    fieldsets = (
        (None, {
            'fields': ('_type', 'description', 'created')
        }),
        ('Build Info', {
            'fields': ('user_agent', 'product_name', 'version',
                       'platform_name', 'locale')
        }),
        ('Device Info', {
            'fields': ('manufacturer', 'device')
        }),
        ('Terms', {
            'fields': ('terms',)
        }),
    )
    readonly_fields = ('created', 'product_name', 'platform_name', 'version',
                       'locale')

admin.site.register(Opinion, OpinionAdmin)


class TermAdmin(admin.ModelAdmin):
    list_display = ('term', 'hidden')
    list_filter = ('hidden',)
    search_fields = ['term']
admin.site.register(Term, TermAdmin)


class VersionCountAdmin(admin.ModelAdmin):
    list_display = ('product', 'version', 'num_opinions', 'active')
    list_filter = ('active', 'product')
    ordering = ('-version', 'product')
    readonly_fields = ('product', 'version', 'num_opinions', 'version_int')
    search_fields = ['version']

admin.site.register(VersionCount, VersionCountAdmin)
