from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.utils import timezone
from django.forms import ValidationError
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.db.models import Q
from django.core.paginator import Paginator

from backend.models import Gemeente, Prediker, Reeks, Preek
from frontend.forms import PreekForm, ReeksForm, PredikerForm
from datetime import datetime

# General Views
class HomeView(View):
    template_name = 'home.html'

    def get(self, request):

        return render(request, self.template_name)

class ArgiefView(View):
    template_name = 'argief.html'

    def get(self, request):

        context = {
            'gemeentes': Gemeente.objects.all(),
            'predikers': Prediker.objects.all()
        }

        return render(request, self.template_name, {'context': context})

class GemeenteView(View):
    template_name = 'general/gemeente_view.html'

    def get(self, request, pk):
        gemeente = Gemeente.objects.get(pk=pk)

        

        preke = Preek.objects.filter(gemeente=gemeente)

        query = self.request.GET.get("q", None)
        if query is not None:
            preke = preke.filter(
                Q(tema__icontains=query) |
                Q(skriflesing__icontains=query) |
                Q(prediker__naam__icontains=query) |
                Q(prediker__van__icontains=query)
            )

        preke_paginator = Paginator(preke, 20)
        preke_page_num = self.request.GET.get('page')
        preke_page = preke_paginator.get_page(preke_page_num)

        

        reekse = Reeks.objects.filter(gemeente=gemeente)

        context = {
            'preke': preke_page,
            'reekse': reekse,
            'gemeente': gemeente
        }

        return render(request, self.template_name, {'context': context})








# Administration Views
class Administration(LoginRequiredMixin, View):
    template_name = 'administration/index.html'

    def get(self, request):

        # Get user data
        user = request.user

        context = {
            'reekse': Reeks.objects.filter(gemeente=user.profile.gemeente),
            'predikers': Prediker.objects.all(),
            'preke': Preek.objects.filter(gemeente=user.profile.gemeente)
        }

        return render(request, self.template_name, {'context': context})

AdministrationView = Administration.as_view()


class NewPreek(LoginRequiredMixin, View):
    template_name = 'administration/new_preek.html'

    def get(self, request):

        # Get user data
        user = request.user

        context = {
            'reekse': Reeks.objects.filter(gemeente=user.profile.gemeente),
            'dateform': PreekForm
        }

        return render(request, self.template_name, {'context': context})
    
    def post(self, request):

        context = {}

        try:
            # Get Data from Post
            data = request.POST
            # Get user data
            user = request.user
            # Check audio file
            file = request.FILES['audio_file']
            if not file.name.endswith(".mp3"):
                raise ValidationError("Please select an MP3 file.")
            elif file.size > 60*1024*1024:
                raise ValidationError("File is too large ( > 60mb ).")
            try:
                reeks = get_object_or_404(Reeks, pk=data['reeks'])
            except Exception as e:
                reeks = None

            Preek.objects.create(
                datum=datetime.strptime(data['datum'],  '%m/%d/%Y %H:%M'),
                prediker=Prediker.objects.get(pk=data['prediker']),
                gemeente=user.profile.gemeente,
                reeks=reeks,
                tema=data['tema'],
                skriflesing=data['skriflesing'],
                audio_file=request.FILES['audio_file']
            )
        except Exception as e:
            context['error'] = e
            context['reekse'] = Reeks.objects.filter(gemeente=user.profile.gemeente)
            context['dateform'] = PreekForm

            return render(request, self.template_name, {'context': context})

        # context['notification'] = 'Preek Suksesvol bygevoeg'
        # context['reekse'] = Reeks.objects.filter(gemeente=user.profile.gemeente)
        # context['predikers'] = Prediker.objects.all()
        # context['preke'] = Preek.objects.filter(gemeente=user.profile.gemeente)

        # return render(request, 'administration/index.html', {'context': context})
        return HttpResponseRedirect('/administration')

NewPreekView = NewPreek.as_view()


class NewReeks(LoginRequiredMixin, View):
    template_name = 'administration/new_reeks.html'

    def get(self, request):
        context = {
            "form": ReeksForm
        }

        return render(request, self.template_name, {'context': context})
    
    def post(self, request):

        context = {}

        try:
            reeks_naam = request.POST['naam']
            gemeente = request.user.profile.gemeente

            Reeks.objects.create(
                naam=reeks_naam,
                gemeente=gemeente
            )
        except Exception as e:
            context['error'] = e
            context['form'] = ReeksForm

            return render(request, self.template_name, {'context': context})
        return HttpResponseRedirect('/administration')

NewReeksView = NewReeks.as_view()


class NewPrediker(LoginRequiredMixin, View):
    template_name = 'administration/new_prediker.html'

    def get(self, request):
        context = {
            "form": PredikerForm
        }

        return render(request, self.template_name, {'context': context})
    
    def post(self, request):

        context = {}

        try:
            titel = request.POST['titel']
            naam = request.POST['naam']
            van = request.POST['van']
            sel = request.POST['sel']
            epos = request.POST['epos']

            Prediker.objects.create(
                titel=titel,
                naam=naam,
                van=van,
                sel=sel,
                epos=epos
            )
        except Exception as e:
            context['error'] = e
            context['form'] = PredikerForm

            return render(request, self.template_name, {'context': context})
        return HttpResponseRedirect('/administration')

NewPredikerView = NewPrediker.as_view()


class DeletePreek(LoginRequiredMixin, View):
    def get(self, request, pk):
        preek_obj = Preek.objects.get(pk=pk)
        preek_obj.delete()
        return HttpResponseRedirect('/list_preek')

DeletePreekView = DeletePreek.as_view()


class DeleteReeks(LoginRequiredMixin, View):
    def get(self, request, pk):
        gemeente = request.user.profile.gemeente

        reeks_obj = Reeks.objects.get(pk=pk)

        if gemeente == reeks_obj.gemeente:
            reeks_obj.delete()
            
        return HttpResponseRedirect('/administration')

DeleteReeksView = DeleteReeks.as_view()



class ListPreek(LoginRequiredMixin, ListView):
    paginate_by = 20
    template_name = 'administration/list_preek.html'

    def get_queryset(self):
        gemeente = self.request.user.profile.gemeente
        preke = Preek.objects.filter(gemeente=gemeente)

        query = self.request.GET.get("q", None)
        if query is not None:
            preke = preke.filter(
                Q(tema__icontains=query) |
                Q(skriflesing__icontains=query) |
                Q(prediker__naam__icontains=query) |
                Q(prediker__van__icontains=query)
            )

        return preke

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

ListPreekView = ListPreek.as_view()

class ListReeks(LoginRequiredMixin, ListView):
    paginate_by = 20
    template_name = 'administration/list_reeks.html'

    def get_queryset(self):
        gemeente = self.request.user.profile.gemeente
        reekse = Reeks.objects.filter(gemeente=gemeente)

        query = self.request.GET.get("q", None)
        if query is not None:
            reekse = reekse.filter(
                Q(naam__icontains=query)
            )

        return reekse

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

ListReeksView = ListReeks.as_view()

class ListPrediker(LoginRequiredMixin, ListView):
    paginate_by = 20
    template_name = 'administration/list_prediker.html'

    def get_queryset(self):
        predikers = Prediker.objects.all()

        query = self.request.GET.get("q", None)
        if query is not None:
            predikers = predikers.filter(
                Q(naam__icontains=query) |
                Q(van__icontains=query) |
                Q(sel__icontains=query) |
                Q(epos__icontains=query)
            )

        return predikers

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

ListPredikerView = ListPrediker.as_view()

