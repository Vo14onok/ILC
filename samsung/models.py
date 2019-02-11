from django.db import models
from django.urls import reverse



class Position(models.Model):
    class Meta():
        db_table = 'position'
    cell = models.CharField(max_length=8, null=False, verbose_name='Ячейка')

    def __str__(self):
        return '%s' % (self.cell)



class Company(models.Model):
    class Meta():
        db_table = 'company'
    company = models.CharField(max_length=20, verbose_name='Компания', help_text='Отправитель/получатель')

    def __str__(self):
        return '%s' % (self.company)



class Cargo(models.Model):
    class Meta():
        db_table = 'cargo'
    cargotype = models.CharField('Наименование груза', max_length=12)
    count = models.DecimalField('Стоимость', max_digits=4, decimal_places=2)

    def __str__(self):
        return '%s' % (self.cargotype)

class Type(models.Model):
    class Meta():
        db_table = 'type'
    type = models.CharField('Вид упаковки', max_length=12)

    def __str__(self):
        return '%s' % (self.type)



class Incoming(models.Model):
    class Meta():
        db_table = 'incoming'
    incoming_date = models.DateField('Дата разгрузки')
    track_i = models.CharField('Номер грузовика', max_length=8)
    trailer_i = models.CharField('Номер прицепа', max_length=8)
    container_i = models.CharField('Номер контейнера', max_length=11)
    uploading = (
        ('0', 'Нет'),
        ('1', 'Да'),
    )
    upload = models.CharField('Контейнер', max_length=3, blank=False, choices=uploading, default='d', help_text='Снятие контейнера')
    sender = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True, verbose_name='Отправитель')
    cargo = models.ForeignKey('Cargo', on_delete=models.SET_NULL, null=True, verbose_name='Наименование груза')
    pack = models.ForeignKey('Type', on_delete=models.SET_NULL, null=True, verbose_name='Вид упаковки')
    quantity_i = models.PositiveIntegerField('Количество')
    cell_position = models.ForeignKey('Position', on_delete=models.SET_NULL, null=True, verbose_name='Ячейка', help_text='Место размещения на складе')
    cmr = models.CharField('CMR/TTH', max_length=12)
    akt_i = models.CharField('Номер акта', max_length=5)
    lot = models.CharField('Лот', max_length=19)

    def get_absolute_url(self):
        return reverse('detail', kwargs={"id": self.id})

    def __str__(self):
        return '%s' % (self.id)



class Outcoming(models.Model):
    class Meta():
        db_table = 'outcoming'
    akt_incoming = models.OneToOneField(Incoming, on_delete=models.SET_NULL, null=True)
    outcoming_date = models.DateField('Дата отгрузки')
    track_o = models.CharField('Номер грузовика', max_length=8)
    trailer_o = models.CharField('Номер прицепа', max_length=8)
    recepient = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True, verbose_name='Получатель')
    akt_o = models.CharField('Номер акта', max_length=5)
    quantity_o = models.PositiveIntegerField('Количество')
    ttn = models.CharField('TTH', max_length=12)
    comments = models.TextField('Примечания', max_length=50, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('detail', kwargs={"id": self.akt_incoming_id})

    def __str__(self):
        return '%s %s %s %s' % (self.outcoming_date, self.track_o, self.trailer_o, self.ttn)

# Create your models here.
