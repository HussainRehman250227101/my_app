from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import project_serializer
from projects.models import Project,Review



def check_api(request):
    return render(request,'check_api.html')


# ALL ROUTES
@api_view(['GET'])
def all_routes(request):
    routes = [
        {'GET':'api/projects'},
        {'GET':'api/projects/id'},
        {'POST':'api/projects/id/vote'},
     
        {'POST':'api/users/token'},
        {'POST':'api/users/token/refresh'},
    ]
    return Response(routes)

# ALL PROJECTS
@api_view(['GET'])
def all_projects(request):
    projects = Project.objects.all()
    serializer = project_serializer(projects,many=True)

    return Response(serializer.data)


# SINGLE PROJECT
@api_view(['GET'])
def single_project(request,pk):
    project = Project.objects.get(id=pk)
    serializer = project_serializer(project,many=False)

    return Response(serializer.data)


# VOTE ADDING 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_vote(request,pk):
    # return Response(pk)
    project = Project.objects.get(id=pk)
    data = request.data

    review, created = Review.objects.get_or_create(
        owner = request.user.profile,
        project = project
    )
    review.value = data["value"]
    
    review.save()

    project.reviews_count

    
    serializer = project_serializer(project, many=False)
    return Response(serializer.data)
    