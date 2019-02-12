from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, F, Sum
from django.db import models
from django.views import generic
from .models import Incoming, Outcoming, Cargo
from .forms import NewForm, PlusForm
from django.views.generic import ListView
from itertools import chain
import datetime
import calendar
import xlwt



class IncomingDetailView(generic.ListView):
    model = Incoming
    template_name = 'cargo.html'
    context_object_name = 'view'


def view(request, id=None):
    view_i = get_object_or_404(Incoming, id=id)
    c = Incoming.objects.filter(id=id).values('incoming_date')
    b = Outcoming.objects.filter(akt_incoming_id=id).values('outcoming_date')
    try:
        a = (b[0]['outcoming_date'] - c[0]['incoming_date']).days
    except:
        a = 404
    f = datetime.date.today()
    d = (f - c[0]['incoming_date']).days
    try:
        view_o = Outcoming.objects.get(akt_incoming_id=id)
    except Outcoming.DoesNotExist:
        view_o = None
    form_o = PlusForm(request.POST or None, initial={'akt_incoming': view_i,})
    if form_o.is_valid():
        form_o.save()
        instance = form_o.save(commit=False)
        instance.save()
        messages.success(request, "Well done my padavan!")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {'view_i': view_i, 'form_o': form_o, 'view_o':view_o, 'a': a, 'd': d}
    return render(request, 'view.html', context)


def samsung(request):
    incomings = Incoming.objects.all()
    outcomings = Outcoming.objects.all()
    allbase = incomings.count()
    out = outcomings.count()
    rest = allbase-out
    query = request.GET.get('search')
    if query:
        incomings = incomings.filter(
            Q(incoming_date__icontains=query)|
            Q(track_i__icontains=query)|
            Q(trailer_i__icontains=query)|
            Q(container_i__icontains=query)|
            Q(cmr__icontains=query)|
            Q(cargo__cargotype__icontains=query)|
            Q(pack__type__icontains=query)|
            Q(akt_i__icontains=query)
            ).distinct()
    page = request.GET.get('page')
    paginator = Paginator(incomings, 50)
    try:
        incomings = paginator.page(page)
    except PageNotAnInteger:
        incomings = paginator.page(1)
    except EmptyPage:
        incomings = paginator.page(paginator.num_pages)
    context = {'incomings': incomings, 'allbase': allbase, 'rest': rest, 'outcomings': outcomings}
    return render(request, 'samsung.html', context)



def new(request):
    form = NewForm(request.POST or None)
    if form.is_valid():
        form.save()
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Well done my padavan!")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {'form': form}
    return render(request, 'new.html', context)



def test(request):
    incomings = Incoming.objects.all()
    outcomings = Outcoming.objects.all()
    # all = incomings.outcoming_set.objects.all()
    all = '1'
    print (outcomings)
    context = {'all': all, 'incomings': incomings, 'outcomings': outcomings, 'all': all}
    return render(request, 'test.html', context)

def summary_mounth(request):
    incomings = Incoming.objects.all()
    outcomings = Outcoming.objects.all()
    all = incomings.count()
    out = outcomings.count()
    rest = all - out
    carton_p = Incoming.objects.filter(cargo__cargotype__contains='Картон', pack__type__contains='Паллет').count()
    carton_r = Incoming.objects.filter(cargo__cargotype__contains='Картон', pack__type__contains='Рулон').count()
    polietilen_p = Incoming.objects.filter(cargo__cargotype__contains='Полиетилен', pack__type__contains='Паллет').count()
    carton_p_o = Outcoming.objects.filter(akt_incoming__cargo__cargotype__contains='Картон', akt_incoming__pack__type__contains='Паллет').count()
    carton_r_o = Outcoming.objects.filter(akt_incoming__cargo__cargotype__contains='Картон', akt_incoming__pack__type__contains='Рулон').count()
    polietilen_p_o = Outcoming.objects.filter(akt_incoming__cargo__cargotype__contains='Полиетилен', akt_incoming__pack__type__contains='Паллет').count()
    start_date = request.GET.get('start_date')
    carton_p_r = carton_p-carton_p_o
    carton_r_r = carton_r-carton_r_o
    polietilen_p_r = polietilen_p-polietilen_p_o

    a = 0
    b = 0
    z = 0
    x = 0
    test = incomings.annotate(
            some_test=F('quantity_i') * F('quantity_i')
            )

    incoming_date = Incoming.objects.values('incoming_date')

    end_date = request.GET.get('end_date')
    if start_date or end_date:
        incomings = Incoming.objects.filter(Q(incoming_date__range=(start_date, end_date)))
        outcomings = Outcoming.objects.filter(Q(outcoming_date__range=(start_date, end_date)))
        carton_p = Incoming.objects.filter(Q(incoming_date__range=(start_date, end_date)),
        cargo__cargotype__contains='Картон', pack__type__contains='Паллет').count()
        carton_r = Incoming.objects.filter(Q(incoming_date__range=(start_date, end_date)),
        cargo__cargotype__contains='Картон', pack__type__contains='Рулон').count()
        polietilen_p = Incoming.objects.filter(Q(incoming_date__range=(start_date, end_date)),
        cargo__cargotype__contains='Полиетилен', pack__type__contains='Паллет').count()
        carton_p_o = Outcoming.objects.filter(Q(outcoming_date__range=(start_date, end_date)),
        akt_incoming__cargo__cargotype__contains='Картон', akt_incoming__pack__type__contains='Паллет').count()
        carton_r_o = Outcoming.objects.filter(Q(outcoming_date__range=(start_date, end_date)),
        akt_incoming__cargo__cargotype__contains='Картон', akt_incoming__pack__type__contains='Рулон').count()
        polietilen_p_o = Outcoming.objects.filter(Q(outcoming_date__range=(start_date, end_date)),
        akt_incoming__cargo__cargotype__contains='Полиетилен', akt_incoming__pack__type__contains='Паллет').count()
        all = incomings.count()
        out = outcomings.count()
        print (incomings)
        test = incomings.annotate(
                some_test=Sum(F('quantity_i') * F('cargo__count'), output_field = FloatField()),
                t = F('quantity_i'),
                v = F('cargo__count'),
                # z = (F('outcoming__outcoming_date') - F('incoming_date'))
                )

        for item in incomings:
            print (Incoming.incoming_date)
        # print (test.some_test)

        incoming_date = Incoming.objects.filter(incoming_date__icontains=start_date).values('incoming_date')
        # z = incoming_date[0]['incoming_date']
        z = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        x = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        b = 0
        if (z > x) == True:
            print ('z больше x')
            a = ('z больше x')
            # b = (datetime.datetime.strptime(end_date, '%Y-%m-%d').date() - x).days
            b = (z - x).days
        elif (z < x) == True:
            print ('z меньше x')
            a = ('z меньше x')
            # b = (datetime.datetime.strptime(end_date, '%Y-%m-%d').date() - x).days
            b = (x - z).days
    print (a, b, start_date, end_date, z)
    context = {'all': all, 'out': out, 'rest': rest, 'incomings': incomings, 'test': test,
                'a': a, 'b': b, 'start_date': start_date, 'end_date': end_date, 'z': z, 'x': x, 'incoming_date': incoming_date,
            'carton_p': carton_p, 'carton_r': carton_r,  'polietilen_p': polietilen_p,
            'carton_p_o': carton_p_o, 'carton_r_o': carton_r_o,  'polietilen_p_o': polietilen_p_o,
            'carton_p_r': carton_p_r, 'carton_r_r': carton_r_r,  'polietilen_p_r': polietilen_p_r}
    return render(request, 'summary_mounth.html', context)

def exel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Samsung.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Поступления')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['id', 'Дата разгрузки', 'Номер грузовика', 'Номер прицепа', 'Номер контейнера', 'Контейнер', 'Company', 'Cargo', 'Type', 'Количество', 'Position', 'CMR/TTH', 'Номер акта', 'Лот']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    incoming = Incoming.objects.all().values_list('id', 'incoming_date', 'track_i', 'trailer_i', 'container_i', 'upload', 'sender', 'cargo', 'pack', 'quantity_i', 'cell_position', 'cmr', 'akt_i', 'lot')
    for row in incoming:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)


    wb.save(response)
    return response
