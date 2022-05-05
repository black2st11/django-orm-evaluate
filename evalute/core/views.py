from django.shortcuts import render, HttpResponse
from django.views import View
from .models import Dump, Ground
from rest_framework.views import APIView
from rest_framework.response import Response 
# Create your views here.

class MainView(APIView):
    def get(self, request):
        retrieves = ['filter', 'all', 'get']
        detail_retireves = ['full-scan', 'solid-scan', 'bool', 'wrapper']
        creates = ['bulk-by-manager', 'bulk-by-python', 'solid-by-object', 'solid-by-manager']
        updates = ['bulk-by-object', 'bulk-by-bulkmanager', 'bulk-by-manager']
        deletes = ['by-object', 'by-manager']
        joins = ['prefetch', 'none', 'selected']

        reset = {
            'name' : "Reset 리셋",
            'list' : [{'name' : 'reset', 'href' : f'/lab/reset/'}]
        }

        retrieve = {
            'name' : 'Retrieve 조회',
            'list' : [{'name' : f'{item} active = True' if i >= 1 else f'{item} active = False', 'href' : f'/lab/retrieve/{item}/{i}/'} for i in range(2) for item in retrieves ]
        }

        detail_retrieve = {
            'name' : 'Detail Retrieve 상세 조회',
            'list' : [{'name' : item, 'href' : f'/lab/detail-retrieve/{item}/'} for item in detail_retireves]
        }

        create = {
            'name' : "Create 생성",
            'list' : [{'name' : item, 'href' : f'/lab/create/{item}/'} for item in creates]
        }

        update = {
            'name' : "Update 수정",
            'list' : [{'name' : item, 'href' : f'/lab/update/{item}/'} for item in updates]
        }

        delete = {
            'name' : "Delete 삭제",
            'list' : [{'name' : item ,'href' : f'/lab/delete/{item}/'} for item in deletes]
        }

        join = {
            'name' : 'Join 연결',
            'list' : [{'name' : item , 'href' : f'/lab/join/{item}/'} for item in joins]
        }

        href_list = [reset, retrieve, detail_retrieve , update, join, create, delete  ]
        context = {"title" : "ORM의 Query는 언제 동작하나" , 'href_list' : href_list}
        return render(request, 'core/index.html', context)

class ResetView(APIView):
    def get(self, request):
        Ground.objects.all().delete()
        ground = Ground.objects.create(name='test_ground')
        dumps = [Dump(name='test_dump', ground=ground) for i in range(100)]
        dumps.append(Dump(name='test_dump_unique', ground=ground))
        Dump.objects.bulk_create(dumps)

        return Response(data='good')
class RetrieveView(APIView):
    def get(self, request, get_type, active):
        if get_type == 'filter':
            dumps = Dump.objects.filter(name='test_dump')
        elif get_type == 'all':
            dumps = Dump.objects.all()
        else :
            dumps = Dump.objects.get(name='test_dump_unique')

        if active >= 1 :
            print(dumps)

        return Response(data = f'type : {get_type}')

class RetrieveDetailView(APIView):
    def get(self, request, get_type):
        if get_type == 'full-scan':
            dumps = Dump.objects.all()
            for dump in dumps :
                dump
        elif get_type == 'solid-scan':
            dumps = Dump.objects.all()
            for i in range(100):
                dumps[i]
        elif get_type == 'bool':
            dumps = Dump.objects.all()
            if dumps:
                dumps[50]
                dumps[99]
        else :
            dumps = Dump.objects.all()
            list(dumps)
            dumps[50]
            dumps[1]

        return Response(data = f'type : {get_type}')

class CreateView(APIView):
    def get(self, request, create_type):

        if create_type == 'bulk-by-create':
            dump_bulks = [Dump(name = 'dump_test_bulk') for i in range(100)]
            Dump.objects.bulk_create(dump_bulks)
        elif create_type == 'bulk-by-python':
            dump_bulks = [i for i in range(100)]
            for item in dump_bulks:
                Dump.objects.create(name=f'dump_by_python{item}')
        elif create_type == 'solid-by-object':
            Dump(name='test_dump_by_object')
        else :
            Dump.objects.create(name='test_dump_by_manage_create')

        return Response(data = f'type : {create_type}')
        
class UpdateView(APIView):
    def get(self, request, update_type):
        if update_type == 'bulk-by-object':
            dumps = Dump.objects.all()
            for dump in dumps:
                dump.name = 'test_dump'
                dump.save()
        elif update_type == 'bulk-by-bulkmanager':
            dumps = Dump.objects.all()
            for dump in dumps:
                dump.name = 'test_dump'
            Dump.objects.bulk_update(dumps, fields=['name'])
        else:
            Dump.objects.all().update(name='test_dump')
        return Response(data= f'type : {update_type}')

class DeleteView(APIView):
    def get(self, request, delete_type):
        if delete_type == 'by-object':
            dumps = Dump.objects.filter(ground_id=None)
            for dump in dumps:
                dump.delete()
        else :
            dumps = Dump.objects.filter(ground_id=None)
            dumps.delete()
        return Response(data= f'type : {delete_type}')

class JoinView(APIView):
    def get(self, request, join_type):
        if join_type == 'none':
            dumps = Dump.objects.all()
            for dump in dumps:
                dump.ground
        elif join_type == 'prefetch':
            dumps = Dump.objects.all().prefetch_related('ground')
            for dump in dumps:
                dump.ground
        else :
            dumps = Dump.objects.select_related('ground').all()
            for dump in dumps:
                dump.ground
        return Response(data=f'type : {join_type}')