from django.db import models
from django.conf import settings

from django.utils import timezone


class Tag(models.Model):
    name        = models.CharField(verbose_name="タグ名",max_length=10)

    def __str__(self):
        return self.name


    def str_id(self):
        return str(self.id)


class Topic(models.Model):

    title       = models.CharField(verbose_name="タイトル",max_length=100)
    comment     = models.CharField(verbose_name="コメント",max_length=2000)

    dt          = models.DateTimeField(verbose_name="投稿日時",default=timezone.now)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="投稿者",on_delete=models.CASCADE)

    #TODO:中間テーブルのモデルを独自に作らないやり方

    # トピックに割り当てられているタグ(タグの指定は必須ではない(ManyToManyFieldにnullは意味なし))
    tag         = models.ManyToManyField(Tag,verbose_name="タグ",blank=True)

    # 良いねを押したユーザー(related_nameを付けないとここでエラーが起こる)
    #good        = models.ManyToManyField(settings.AUTH_USER_MODEL,verbose_name="良いねしたユーザー",blank=True)


    def __str__(self):
        return self.title

