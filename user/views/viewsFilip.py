from django.views import generic
from django import forms
from user.models import Profile, UserRelationship
from avio.models import Ticket, Flight, Seat, PackageReservation
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.generic.edit import View
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
import datetime


class ListProfiles(generic.ListView):
    template_name = 'user/profile_people_list.html'

    def get(self, request):
        q1 = UserRelationship.objects.filter(user_1 = request.user).values_list('user_2', flat=True)
        q2 = UserRelationship.objects.filter(user_2 = request.user).values_list('user_1', flat=True)
        profiles = Profile.objects.all().exclude(id=self.request.user.profile.id).exclude(user__id__in=q1).exclude(user__in=q2)
        name = request.GET.get('src')
        if name != None:
            if len(name) == 0:
                return render(request, self.template_name, {'q_profiles': profiles})

            first_name = name[0]
            last_name = ('',name[1])[len(name)==2]
            profiles = profiles.filter(user__first_name__icontains=first_name, user__last_name__icontains=last_name)
        return render(request, self.template_name, {'q_profiles': profiles})

    def post(self, request):
        reciever = User.objects.get(pk=request.POST.get('adding'))
        UserRelationship.sendRequest(self.request.user, reciever)
        return redirect('user:profile_people_list')


class ListFriendRequests(generic.ListView):
    template_name = 'user/profile_friend_requests.html'

    def get(self, request):
        q1 = UserRelationship.objects.filter(user_1 = request.user, status = 'PF').values_list('user_2', flat=True)
        q2 = UserRelationship.objects.filter(user_2 = request.user, status = 'PS').values_list('user_1', flat=True)
        profiles = Profile.objects.all().filter(user__id__in=q1) | Profile.objects.all().filter(user__id__in=q2)
        return render(request, self.template_name, {'q_profiles': profiles})

    def post(self, request):
        reciever = User.objects.get(pk=request.POST.get('usr'))
        if request.POST.get('option') == 'accept':
            UserRelationship.accept(self.request.user, reciever)
        else:
            UserRelationship.decline(self.request.user, reciever)
        return redirect('user:profile_friend_requests')

@login_required()
def cancel_reservation(request):
    if request.method == 'POST':
        val = request.POST['btn']
        if "ALL" in val:
            val = val.replace("ALL", "")
            res = PackageReservation.objects.get(pk = val)
            for tic in res.ticket_set.all():
                tic.cancelTicket()

            if res.car_reservation != None:
                car_res = res.car_reservation
                car_res.delete()

            if res.hotel_reservation != None:
                hotel_res = res.hotel_reservation
                hotel_res.delete()

            res.delete()
        else:
            t = Ticket.objects.get(pk = val)
            t.cancelTicket()
            t.delete()
    return redirect('user:home')

@login_required()
def profile(request):
    if not Profile.objects.filter(user=request.user).exists():
        return render(request, 'user/admin_edit_page.html')
    q1 = UserRelationship.objects.filter(user_1 = request.user, status = 'FF').values_list('user_2', flat=True)
    q2 = UserRelationship.objects.filter(user_2 = request.user, status = 'FF').values_list('user_1', flat=True)
    profiles = Profile.objects.all().filter(user__id__in=q1) | Profile.objects.all().filter(user__id__in=q2)
    return render(request, 'user/profile_page.html', {'q_profiles': profiles})


class Unfriend(generic.ListView):
    template_name = 'user/profile_unfriend.html'

    def get(self, request):
        q1 = UserRelationship.objects.filter(user_1 = request.user, status = 'FF').values_list('user_2', flat=True)
        q2 = UserRelationship.objects.filter(user_2 = request.user, status = 'FF').values_list('user_1', flat=True)
        profiles = Profile.objects.all().filter(user__id__in=q1) | Profile.objects.all().filter(user__id__in=q2)
        return render(request, self.template_name, {'q_profiles': profiles})

    def post(self, request):
        reciever = User.objects.get(pk=request.POST.get('usr'))
        UserRelationship.decline(self.request.user, reciever)
        return redirect('user:profile_unfriend')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['city', 'phone_number', 'pic']

    
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileEdit(View):
    template_name = 'user/profile_edit.html'
    
    def get(self, request, *args, **kwargs):
        context = {}
        context['form_user'] = UserForm(instance = request.user)
        context['form_profile'] = ProfileForm(instance = request.user.profile)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form_profile = ProfileForm(request.POST, request.FILES, instance = request.user.profile)
        form_user = UserForm(request.POST, instance = request.user)
        if form_profile.is_valid() and form_user.is_valid():
            form_user.save()
            form_profile.save()

        return redirect('user:profile')


@login_required() 
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('user:profile')
        else:
            messages.error(request, 'Something not right')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user/profile_pass_change.html', {'form': form})


class PassportForm(forms.Form):
    passport = forms.CharField(label='passport', max_length=15, )


class Invitation(generic.ListView):
    template_name = 'user/profile_invitations.html'

    def get_queryset(self):
        qs = Ticket.objects.filter(user = self.request.user, status = "R")
        for tic in qs:
            if tic.invitation_too_long():
                tic.cancelTicket()
                tic.delete()
            if not tic.package_reservation.canBeCanceled:
                tic.cancelTicket() 
                tic.delete()
        return qs

    def get_context_data(self, **kwargs):
        context = super(Invitation, self).get_context_data(**kwargs)
        context['form'] = PassportForm()
        return context 

    def post(self, request):
        choice = request.POST.get('btn')
        if choice.startswith("decline"):
            choice = choice.replace('decline', '')
            ticket = Ticket.objects.get(pk = int(choice))
            seat = ticket.seat
            seat.seat_status = "F"
            seat.save()
            ticket.delete()
        else:
            ticket = Ticket.objects.get(pk = int(choice))
            ticket.passport = request.POST.get('passport')
            ticket.time = datetime.datetime.now()
            ticket.status = "B"
            seat = ticket.seat
            seat.seat_status = "T"
            seat.save()
            ticket.save()

        return self.get(request)
