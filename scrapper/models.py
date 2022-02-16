from django.db import models

class Article(models.Model):
    article_id = models.IntegerField(primary_key=True)
    tags = models.CharField(max_length=256)
    content = models.TextField(max_length=65536)

