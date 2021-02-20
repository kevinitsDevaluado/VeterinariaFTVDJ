from django.urls import path
from core.erp.views.dashboard.views import DashboardView
from core.erp.views.client.views import ClientListView,ClientCreateView,ClientUpdateView,ClientDeleteView
from core.erp.views.mascot.views import MascotListView,MascotCreateView,MascotUpdateView,MascotDeleteView,MascotInvoicePdfView,MascotDetailsView



app_name = 'erp'

urlpatterns = [
    #home Administration
    path('dashboard/', DashboardView.as_view(), name='dashboard'),


     # client
    path('client/list/', ClientListView.as_view(), name='client_list'),
    path('client/add/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),

      # Mascot
    path('mascot/list/', MascotListView.as_view(), name='mascot_list'),
    path('mascot/add/', MascotCreateView.as_view(), name='mascot_create'),
    path('mascot/update/<int:pk>/', MascotUpdateView.as_view(), name='mascot_update'),
    path('mascot/delete/<int:pk>/', MascotDeleteView.as_view(), name='mascot_delete'),
    path('mascot/invoice/pdf/<int:pk>/', MascotInvoicePdfView.as_view(), name='sale_invoice_pdf'),
    path('mascot/details/<int:pk>/', MascotDetailsView.as_view(), name='mascot_Details'),


]