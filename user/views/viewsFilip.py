from django.views import generic
from django import forms
from user.models import Profile, UserRelationship
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.generic.edit import View
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash


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
def profile(request):
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
        form_user = UserForm(request.POST, instance = request.user)
        form_profile = ProfileForm(request.POST, instance = request.user.profile)
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


