from django.views import generic
from django.db.models import Q
from user.models import Profile, UserRelationship
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

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
    return render(request, 'user/profile_page.html',{'q_profiles': profiles})
