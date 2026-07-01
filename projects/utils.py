from django.db.models import Q
from .models import Project
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage


def searchproject(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    # tag = Tag.objects.filter(name__icontains=search_query)
    projects = Project.objects.distinct().filter(
        Q(owner__name__icontains=search_query) |
        Q(title__icontains=search_query) |
        Q(tags__name__icontains=search_query) 

    )
    return  projects,search_query



def paginateprojects(request,projects,results):
    page = request.GET.get('page')
    pagination =  Paginator(projects,results)
    try :
        projects = pagination.page(page)
    except PageNotAnInteger:
        page = 1
        projects = pagination.page(page)
    except EmptyPage:
        page = pagination.num_pages
        projects = pagination.page(page)

    leftIndex = (int(page) - 4)
    if leftIndex <1 :
        leftIndex = 1

    rightIndex  = (int(page) + 5)
    if rightIndex > pagination.num_pages:
        rightIndex = pagination.num_pages +1

    custom_range = range(leftIndex,rightIndex)
    return custom_range,projects