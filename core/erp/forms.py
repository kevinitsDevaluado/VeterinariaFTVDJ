from datetime import datetime

from django import forms
from django.forms import ModelForm

from core.erp.models import  Client , Mascot
class ClientForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True
        #self.fields['date_birthday'].widget.attrs['autofocus'] = True

  

    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'names': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese sus Nombres',
                }
            ),
            'surnames': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese sus Apellidos',
                }
            ),
            'dni': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su Cédula',
                   
                }
            ),
            'date_birthday': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'date_MaxNacimiento',
                    'data-target': '#date_MaxNacimiento',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'address': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su Dirección',
                }
            ),
            'gender': forms.Select()
        }
    

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    # def clean(self):
    #     cleaned = super().clean()
    #     if len(cleaned['name']) <= 50:
    #         raise forms.ValidationError('Validacion xxx')
    #         # self.add_error('name', 'Le faltan caracteres')
    #     return cleaned



class MascotForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True
        #self.fields['date_birthday'].widget.attrs['autofocus'] = True

  

    class Meta:
        model = Mascot
        
        fields = ['names', 'date_birthday','especie','gender','raza','cli','observacion','image']

        widgets = {
            'names': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese sus Nombres',
                }
            ),
            'date_birthday': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'date_MaxNacimiento',
                    'data-target': '#date_MaxNacimiento',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'especie': forms.Select(),
            'gender': forms.Select(),
            'cli': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
            }),
            'qe': forms.TextInput(
                attrs={
                    'type':'hidden'
                }
            ),
        }
    

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    # def clean(self):
    #     cleaned = super().clean()
    #     if len(cleaned['name']) <= 50:
    #         raise forms.ValidationError('Validacion xxx')
    #         # self.add_error('name', 'Le faltan caracteres')
    #     return cleaned
