# from django.db.models.signals import post_save,post_delete
# from .models import Review,Project


# def refresh_review(sender,instance,created,**kwargs):
#     if created:
#         Project.reviews_count


# post_save.connect(refresh_review, sender=Review)