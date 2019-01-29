from django.views.generic.edit import View
from django.shortcuts import redirect, render



class AvioSearch(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'avio/avio_search.html', {})