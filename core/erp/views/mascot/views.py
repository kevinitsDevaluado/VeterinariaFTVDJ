from django.shortcuts import render, redirect 

import json
import os
from django.http import HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, View
from django.conf import settings
from xhtml2pdf import pisa
from django.template.loader import get_template

from core.erp.forms import MascotForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Mascot


class MascotListView(LoginRequiredMixin, ListView):
    model = Mascot
    form_class = MascotForm

    template_name = 'mascot/list.html'
    permission_required = 'view_mascot'



    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []               
                for i in Mascot.objects.all():
                    data.append(i.toJSON())
            elif action == 'search_details_prod':
                data = []
                for i in Mascot.objects.filter(sale_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
  
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Mascotas'
        context['create_url'] = reverse_lazy('erp:mascot_create')
        context['list_url'] = reverse_lazy('erp:mascot_list')
        context['entity'] = 'Mascotas'
        context['curso'] = self.get_queryset()
        return context


class MascotCreateView(LoginRequiredMixin, CreateView):
    model = Mascot
    form_class = MascotForm
    template_name = 'mascot/create.html'
    success_url = reverse_lazy('erp:mascot_list')
    permission_required = 'add_mascot'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación una Mascota'
        context['entity'] = 'Mascota'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class MascotUpdateView(LoginRequiredMixin, UpdateView):
    model = Mascot
    form_class = MascotForm
    template_name = 'mascot/create.html'
    success_url = reverse_lazy('erp:mascot_list')
    permission_required = 'change_client'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición una Mascota'
        context['entity'] = 'Mascota'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class MascotDeleteView(LoginRequiredMixin, DeleteView):
    model = Mascot
    template_name = 'mascot/delete.html'
    success_url = reverse_lazy('erp:mascot_list')
    permission_required = 'delete_mascot'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Mascota'
        context['entity'] = 'Mascota'
        context['list_url'] = self.success_url
        return context




class MascotInvoicePdfView(View):

    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        # use short variable names
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /static/media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('mascot/envoice.html')
            context = {
                'sale': Mascot.objects.get(pk=self.kwargs['pk']),
                'comp': {'name': 'ALGORISOFT S.A.', 'ruc': '9999999999999', 'address': 'Milagro, Ecuador'},
                'icon': '{}{}'.format(settings.MEDIA_URL, 'logo.png')
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:mascot_list'))


class MascotDetailsView(View):

    model = Mascot
    form_class = MascotForm
    template_name = 'mascot/detalles.html'


    def get_context_data(self, **kwargs):
        """Retorna un contexto a enviar a template.
        Aquí definimos todas las variables que necesitamos enviar a nuestro template definido en TEMPLATE_NAME,
        se agregan a un diccionario general para poder ser enviados en la funcion RENDER.


        :return: un contexto
        :rtype: dict
        """


        context = {
            'sale': Mascot.objects.get(pk=self.kwargs['pk']),
            'comp': {'name': 'ALGORISOFT S.A.', 'ruc': '9999999999999', 'address': 'Milagro, Ecuador'},
            'icon': '{}{}'.format(settings.MEDIA_URL, 'logo.png')
        }
        return context
        
    def get(self, request, *args, **kwargs):
        """Renderiza un template con un contexto dado.
        Se encarga de manejar toda petición enviada del navegador a Django a través del método GET
        del protocolo HTTP, en este caso renderiza un template definido en TEMPLATE_NAME junto con
        el contexto definido en GET_CONTEXT_DATA.


        :return: render
        :rtype: func
        """


        return render(request, self.template_name, self.get_context_data())

