from django.contrib import admin
from .models import Position, Company, Incoming, Outcoming, Cargo, Type

class AddOutcoming(admin.StackedInline):
    model = Outcoming

class IncomingAdmin(admin.ModelAdmin):
    list_display = ('incoming_date', 'track_i', 'trailer_i', 'container_i', 'sender', 'cargo', 'pack', 'cmr', 'akt_i', 'lot')
    inlines = [AddOutcoming]
    extra = 1

class OutcomingAdmin(admin.ModelAdmin):
    list_display = ('outcoming_date', 'track_o', 'trailer_o', 'recepient', 'akt_o', 'ttn')


admin.site.register (Position)
admin.site.register (Company)
admin.site.register (Incoming, IncomingAdmin)
admin.site.register (Outcoming, OutcomingAdmin)
admin.site.register (Cargo)
admin.site.register (Type)

# Register your models here.
