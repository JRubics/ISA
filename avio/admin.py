from django.contrib import admin
from avio.models import *
from django import forms
from django.apps import apps


class AvioCompanyAdmin (admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(id=request.user.profile.avio_admin.id)


class FlightAdmin (admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(FlightAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['avio_company'].initial = request.user.profile.avio_admin
        form.base_fields['avio_company'].disabled = True
        return form

    def save_model(self, request, obj, form, change):
        obj.avio_company = request.user.profile.avio_admin
        obj.save()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(avio_company=request.user.profile.avio_admin.id)


class FlightLegAdmin (admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "flight":
            kwargs["queryset"] = Flight.objects.filter(avio_company=request.user.profile.avio_admin)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        for res in qs:
            if res.flight.id != request.user.profile.avio_admin.id:
                qs.exclude(res)
        return qs


class SeatAdmin (admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "flight":
            kwargs["queryset"] = Flight.objects.filter(avio_company=request.user.profile.avio_admin)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        for res in qs:
            if res.flight.id != request.user.profile.avio_admin.id:
                qs.exclude(res)
        return qs


# Register your models here.
admin.site.register(AvioCompany, AvioCompanyAdmin)
admin.site.register(Flight, FlightAdmin)
admin.site.register(FlightLeg, FlightLegAdmin)
admin.site.register(Seat, SeatAdmin)
admin.site.register(City)
admin.site.register(Country)
admin.site.register(Airport)
