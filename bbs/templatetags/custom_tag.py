#https://noauto-nolife.com/post/django-paginator/

from django import template
register = template.Library()

#検索時に指定したタグとモデルオブジェクトのtagのidが一致した場合はchecked文字列を返す。
#カスタムテンプレートタグとして機能させるため、.simple_tag()デコレータを付与する
@register.simple_tag()
def tag_checked(request, tag_id):

    #検索時に指定したタグのid(文字列型)のリストを作る
    tags    = request.GET.getlist("tag")

    #tagsにidが含まれる場合
    if str(tag_id) in tags:
        return "checked"


