from django.contrib import admin
from avio.models import *
from django import forms
from django.apps import apps
from django.db.models import Count, Sum, Min, Max
import json
from django.db.models.functions import Trunc
from django.db.models import DateTimeField
from .models import FlightRate


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

        qs = qs.filter(seat_status__in = ["T","P","F","O"])
        qs = qs.filter(flight__avio_company = request.user.adminuser.avio_admin.id)

        print("YD&*SDUIAS")

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
            qs = qs.filter(flight__avio_company = request.user.adminuser.avio_admin.id)
        response.context_data['seats'] = qs.values('flight', 'flight__avio_company__name', 'flight__departure_city__name', 'flight__arrival_city__name', 'flight__departure_date').annotate(**metrics).order_by('flight')
        return response

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
            qs = qs.filter(flight__avio_company = request.user.adminuser.avio_admin)


        row = list(qs.values('flight').annotate(**metrics).order_by('flight'))

        flights = qs.values('flight').annotate(**metrics).order_by('flight').values('flight')
        flights = Flight.objects.filter(pk__in = flights)
        flight_summary = zip(flights, row)
        response.context_data['flight_summary'] = flight_summary

        response.context_data['summary_total'] = dict(qs.aggregate(**metrics))

        period = get_next_in_date_hierarchy(request, self.date_hierarchy)
        response.context_data['period'] = period

        summary_over_time = qs.annotate(period=Trunc('time', period, output_field=DateTimeField()),).values('period').annotate(total=Sum('price')).order_by('period')
        tickets_sold = qs.annotate(period=Trunc('time', period, output_field=DateTimeField()),).values('period').annotate(total=Count('id')).order_by('period')

        if period == "month":
            response.context_data['label_list'] = json.dumps(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'Novemer', 'December'])
            val_list = [0,0,0,0,0,0,0,0,0,0,0,0]
            tic_list = [0,0,0,0,0,0,0,0,0,0,0,0]
            for x in summary_over_time:
                val_list[int(x['period'].strftime('%m'))-1] = x['total']
            response.context_data['val_list'] = json.dumps(val_list)

            for x in tickets_sold:
                tic_list[int(x['period'].strftime('%m'))-1] = x['total']
            response.context_data['tic_list'] = json.dumps(tic_list)

            response.context_data['week'] = True
            week_label_list = []
            for x in range(1,53):
                week_label_list.append(str(x) + "week")
            response.context_data['week_label_list'] = json.dumps(week_label_list)
            summary_over_time = qs.annotate(period=Trunc('time', 'week', output_field=DateTimeField()),).values('period').annotate(total=Sum('price')).order_by('period')
            tickets_sold = qs.annotate(period=Trunc('time', 'week', output_field=DateTimeField()),).values('period').annotate(total=Count('id')).order_by('period')

            week_val_list = [0] * 52
            week_tic_list = [0] * 52
            for x in summary_over_time:
                week_val_list[int(x['period'].strftime('%U'))] = x['total']
            response.context_data['week_val_list'] = json.dumps(week_val_list)
            for x in tickets_sold:
                week_tic_list[int(x['period'].strftime('%U'))] = x['total']
            response.context_data['week_tic_list'] = json.dumps(week_tic_list)
            
        elif period == "day":
            response.context_data['week'] = False
            label_list = []
            for x in range(1,32):
                label_list.append(str(x))
            response.context_data['label_list'] = json.dumps(label_list)

            val_list = [0] * 31
            tic_list = [0] * 31
            for x in summary_over_time:
                val_list[int(x['period'].strftime('%d'))-1] = x['total']
            response.context_data['val_list'] = json.dumps(val_list)
            for x in tickets_sold:
                tic_list[int(x['period'].strftime('%d'))-1] = x['total']
            response.context_data['tic_list'] = json.dumps(tic_list)


        return response

def get_next_in_date_hierarchy(request, date_hierarchy):
    if date_hierarchy + '__day' in request.GET:
        return 'hour'

    if date_hierarchy + '__month' in request.GET:
        return 'day'

    if date_hierarchy + '__year' in request.GET:
        return 'month'

    return 'month'

class TicketAdmin(admin.ModelAdmin):
    list_display = ['flight', 'status', 'seat', 'first_name', 'last_name']
    list_filter = ('flight', 'status',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "flight" and not request.user.is_superuser:
            kwargs["queryset"] = Flight.objects.filter(avio_company=request.user.adminuser.avio_admin)
        
        if db_field.name == "package_reservation" and not request.user.is_superuser:
            kwargs["queryset"] = PackageReservation.objects.none()
        
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        qs = qs.filter(flight__avio_company = request.user.adminuser.avio_admin.id)
        return qs


# Register your models here.
admin.site.register(AvioCompany, AvioCompanyAdmin)
admin.site.register(Flight, FlightAdmin)
admin.site.register(FlightLeg, FlightLegAdmin)
admin.site.register(ManageSeats, SeatAdmin)
admin.site.register(Seat, SeatA)
admin.site.register(ProfitSummary, SaleSummaryAdmin)
admin.site.register(City)
admin.site.register(Country)
admin.site.register(Airport)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(FlightRate)
admin.site.register(PackageReservation)




