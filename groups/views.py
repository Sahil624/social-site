from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.core.urlresolvers import reverse
from django.views import generic

from django.shortcuts import get_object_or_404
from django.contrib import messages

from .models import Group,GroupMember
# Create your views here.

class CreateGroup(LoginRequiredMixin,generic.CreateView):
    fields = ("name",'description')
    model = Group

class SingleGroup(generic.DetailView):
    model = Group

class ListGroups(generic.ListView):
    model = Group

class JoinGroup(LoginRequiredMixin,generic.RedirectView):

    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'))

        try:
            GroupMember.objects.create(user=self.request.user,group=group)

        except IntegrityError:
            messages.warning(self.request,("warning You Are Already A Member"))

        else:
            messages.success(self.request,("You Are A Member Now"))

        return super().get(request,*args,**kwargs)

class LeaveGroup(LoginRequiredMixin,generic.RedirectView):

    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        try:
            membership = GroupMember.objects.filter(user = self.request.user,group__slug = self.kwargs.get('slug')).get()

        except:
            messages.warning(self.request,("You are Not in this group"))

        else:
            membership.delete()
            messages.success(self.request,"You Have Leaved The group")

        return super().get(request,*args,**kwargs)
