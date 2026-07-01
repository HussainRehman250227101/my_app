from django.db.models import Q
from .models import Profile,Skill
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

def searchprofile(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    
    profile = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(short_intro__icontains=search_query) |
        Q(skill__skill_name__icontains=search_query) 

    )
    return  profile,search_query


def paginateprofiles(request,profiles,results):
    page = request.GET.get('page')
    pagination =  Paginator(profiles,results)
    try :
        profiles = pagination.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = pagination.page(page)
    except EmptyPage:
        page = pagination.num_pages
        profiles = pagination.page(page)

    leftIndex = (int(page) - 2)
    if leftIndex <1 :
        leftIndex = 1

    rightIndex  = (int(page) + 3)
    if rightIndex > pagination.num_pages:
        rightIndex = pagination.num_pages +1

    custom_range = range(leftIndex,rightIndex)
    return custom_range,profiles