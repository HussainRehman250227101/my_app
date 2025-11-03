from django.db import models
import uuid
from users.models import Profile


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique = True, primary_key = True,  editable = False)

    def __str__(self):
        return self.name


class Project(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    image = models.ImageField( null = True, blank=True, default='images/default.jpg')
    Description = models.TextField(max_length=2000 , null = True, blank=True )
    tags = models.ManyToManyField(Tag,null=True, blank=True)
    demo_link = models.CharField(max_length=1000 , null = True, blank=True )
    source_link = models.CharField(max_length=1000 , null = True, blank=True )
    vote_total  = models.IntegerField(default=0 ,null = True,blank=True)
    vote_ratio = models.IntegerField(default=0 ,null = True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique = True, primary_key = True,  editable = False)
    
    class Meta:
        ordering = ['-vote_ratio','-vote_total','title']

    def __str__(self):
        return self.title
    
    @property
    def reviews_count(self):
    
        reviews = self.review_set.all()
        total_votes = reviews.count()
        up_votes = reviews.filter(value = 'up').count()
        ratio = (up_votes/total_votes)*100
        self.vote_total = total_votes
        self.vote_ratio = ratio
        self.save()
        

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

class Review(models.Model):
    votes = [
        ('up', 'Up Vote'),
        ('down', 'Down vote')
    ]
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True , blank = True)
    value = models.CharField(max_length=200 , choices = votes)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique = True, primary_key = True,  editable = False)

    def __str__(self):
        return f'{self.project.title} ---- {self.body}'

    class Meta:
        unique_together = [['owner','project']]
    

