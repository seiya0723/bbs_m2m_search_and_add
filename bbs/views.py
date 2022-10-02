from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .models import Topic,Tag
from .forms import TopicForm,TopicTagForm

from django.db.models import Q



#TODO:LoginRequiredMixinのオーバーライドを使うことで、特定のユーザーの立場からビューの実行を判断することもできる
# https://noauto-nolife.com/post/django-create-origin-mixin/

class IndexView(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):

        context = {}
        context["tags"]     = Tag.objects.all()

        query   = Q()

        if "search" in request.GET:
            search      = request.GET["search"]

            raw_words   = search.replace("　"," ").split(" ")
            words       = [ w for w in raw_words if w != "" ]

            for w in words:
                query &= Q(title__contains=w)



        #ここで一旦queryによる検索を行う
        topics  = Topic.objects.filter(query).order_by("-dt")


        #TODO:タグの検索(指定されたタグが実在するのか確認をする。)
        form    = TopicTagForm(request.GET)

        if form.is_valid():
            cleaned         = form.clean()
            selected_tags   = cleaned["tag"] 


            #タグ検索をする(中間テーブル未使用、指定したタグを全て含む)
            for tag in selected_tags:

                #TODO:指定したタグが、トピックに含まれているかをチェック。含まれていれば追加。
                topics      = [ topic for topic in topics if tag in topic.tag.all() ]




        context["topics"]   = topics

        return render(request,"bbs/index.html",context)

    def post(self, request, *args, **kwargs):

        copied          = request.POST.copy()
        copied["user"]  = request.user.id

        form    = TopicForm(copied)

        if not form.is_valid():
            print("バリデーションNG")
            print(form.errors)
            return redirect("bbs:index")
        
        print("バリデーションOK")
        form.save()

        return redirect("bbs:index")

index   = IndexView.as_view()


class AddTagView(LoginRequiredMixin,View):

    def post(self, request, pk, *args, **kwargs):

        topic   = Topic.objects.filter(id=pk).first()
        form    = TopicTagForm(request.POST)

        if form.is_valid():

            cleaned = form.clean()

            selected_tags   = cleaned["tag"] 

            #タグ検索をする(中間テーブル未使用、指定したタグを全て含む)
            for tag in selected_tags:

                #このtagはTagモデルクラスのオブジェクト。追加する時はこうする。save()は実行しなくても良い
                #https://stackoverflow.com/questions/1182380/how-to-add-data-into-manytomany-field

                if tag in topic.tag.all():
                    topic.tag.remove(tag)
                else:
                    topic.tag.add(tag)


        return redirect("bbs:index")

tag     = AddTagView.as_view()

