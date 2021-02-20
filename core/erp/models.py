from datetime import datetime

import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw


from django.db import models
from django.forms import model_to_dict

from config.settings import MEDIA_URL, STATIC_URL
from core.erp.choices import gender_choices,gender_unid,gender_especie
from core.erp.validators import vcedula,validacionCantidad,validacionNacimiento,validacionFechaActual,validarLetras,validarLetrass

#TABLA CLIENTE
class Client(models.Model):
    dni = models.CharField(max_length=10, unique=True, verbose_name='Cédula',validators=[vcedula])
    names = models.CharField(max_length=150, verbose_name='Nombres',validators=[validarLetrass])
    surnames = models.CharField(max_length=150, verbose_name='Apellidos',validators=[validarLetras])
    date_birthday = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento' )
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    gender = models.CharField(max_length=10, choices=gender_choices, default='male', verbose_name='Sexo')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} {} / {}'.format(self.names, self.surnames, self.dni)

    def toJSON(self):
        item = model_to_dict(self)
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['date_birthday'] = self.date_birthday.strftime('%Y-%m-%d')
        item['full_name'] = self.get_full_name()
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']


class Mascot(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombres')
    date_birthday = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento' )
    especie = models.CharField(max_length=10, choices=gender_especie, default='perro', verbose_name='Especie')
    gender = models.CharField(max_length=10, choices=gender_choices, default='male', verbose_name='Sexo')
    raza = models.CharField(max_length=10,  null=True, blank=True, verbose_name='Raza')
    cli = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Dueño')
    image = models.ImageField(upload_to='mascot/%Y/%m/%d', null=True, blank=True)
    qr = models.ImageField(upload_to='qr/%Y/%m/%d', null=True, blank=True)

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.names)
        canvas = Image.new('RGB',(290,290), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr-{self.names}.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.qr.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)
    
    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    def __str__(self):
        return self.cli.names

    def toJSON(self):
        item = model_to_dict(self)
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['especie'] = {'id': self.especie, 'name': self.get_gender_display()}
        item['cli'] = self.cli.toJSON()
        item['image'] = self.get_image()
        item['qr'] = self.get_image()
        item['date_birthday'] = self.date_birthday.strftime('%Y-%m-%d')
        return item
   
    class Meta:
        verbose_name = 'Mascota'
        verbose_name_plural = 'Mascotas'
        ordering = ['id']