from django.contrib import admin
from avio.models import *
from django import forms
from django.apps import apps
from django.db.models import Count, Sum, Min, Max

from django.db.models.functions import Trunc
from django.db.models import DateTimeField


class AvioCompanyAdmin (admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(id=request.user.adminuser.avio_admin.id)


class FlightAdmin (admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(FlightAdmin, self).get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['avio_company'].initial = request.user.adminuser.avio_admin
            form.base_fields['avio_company'].disabled = True
        return form

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.avio_company = request.user.adminuser.avio_admin
        obj.save()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(avio_company=request.user.adminuser.avio_admin.id)


class FlightLegAdmin (admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "flight" and not request.user.is_superuser:
            kwargs["queryset"] = Flight.objects.filter(
                avio_company=request.user.adminuser.avio_admin)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        for res in qs:
            if res.flight.id != request.user.adminuser.avio_admin.id:
                qs.exclude(res)
        return qs


class SeatA (admin.ModelAdmin):
    list_display = ['flight', 'seat_status', 'seat_number', 'seat_type']
    ordering = ('-seat_number',)
    list_filter = ('flight', 'seat_type', 'seat_status')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "flight" and not request.user.is_superuser:
            kwargs["queryset"] = Flight.objects.filter(avio_company=request.user.adminuser.avio_admin)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        for res in qs:
            if res.flight.id != request.user.adminuser.avio_admin.id:
                qs.exclude(res)
        return qs


class SeatAdmin(admin.ModelAdmin):
    change_list_template = "avio/admin_flight_seats_list.html"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "flight" and not request.user.is_superuser:
            kwargs["queryset"] = Flight.objects.filter(avio_company=request.user.adminuser.avio_admin)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context,)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
            'number_of_seats': Count('id'),
        }

        if not request.user.is_superuser:
            gs = qs.filter(flight = request.user.adminuser.avio_admin.id)
        response.context_data['seats'] = qs.values('flight', 'flight__avio_company__name', 'flight__departure_city__name', 'flight__arrival_city__name', 'flight__departure_date').annotate(**metrics).order_by('flight')
        return response


# Register your models here.
admin.site.register(AvioCompany, AvioCompanyAdmin)
admin.site.register(Flight, FlightAdmin)
admin.site.register(FlightLeg, FlightLegAdmin)
admin.site.register(ManageSeats, SeatAdmin)
admin.site.register(Seat, SeatA)
admin.site.register(City)
admin.site.register(Country)
admin.site.register(Airport)
admin.site.register(Ticket)



@admin.register(ProfitSummary)
class SaleSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'avio/admin_ticket_profit_list.html'
    date_hierarchy = 'time'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
            'total': Count('id'),
            'total_sales': Sum('price'),
        }

        if not request.user.is_superuser:
            gs = qs.filter(flight = request.user.adminuser.avio_admin.id)

        row = list(
            qs
            .values('flight')
            .annotate(**metrics)
            .order_by('flight')
        )

        flights = qs.values('flight').annotate(**metrics).order_by('flight').values('flight')
        flights = Flight.objects.filter(pk__in = flights)
        flight_summary = zip(flights, row)
        response.context_data['flight_summary'] = flight_summary

        response.context_data['summary_total'] = dict(
            qs.aggregate(**metrics)
        )

        period = get_next_in_date_hierarchy(request, self.date_hierarchy)
        response.context_data['period'] = period

        summary_over_time = qs.annotate(
            period=Trunc('time', period, output_field=DateTimeField()),).values('period').annotate(total=Sum('price')).order_by('period')

        print(summary_over_time)

        summary_range = summary_over_time.aggregate(
            low=Min('total'),
            high=Max('total'),
        )

        high = summary_range.get('high', 0)
        low = summary_range.get('low', 0)



        response.context_data['summary_over_time'] = [{'period': x['period'], 'total': x['total'] or 0,'pct':  ((x['total'] or 0)) / (high + low) * 100,} for x in summary_over_time]

        return response

def get_next_in_date_hierarchy(request, date_hierarchy):
    if date_hierarchy + '__day' in request.GET:
        return 'hour'

    if date_hierarchy + '__month' in request.GET:
        return 'week'

    if date_hierarchy + '__year' in request.GET:
        return 'month'

    return 'year'

