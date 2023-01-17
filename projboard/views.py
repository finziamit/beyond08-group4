from .models.article import Article
from django.shortcuts import render, redirect
from .models.user import User
from .forms import CreateArticleForm, EditArticleForm
from django.http import Http404
from django.http import HttpResponse
from django.template import loader


def error_404(request, exception):
    template = loader.get_template('404.html')
    return HttpResponse(content=template.render(), content_type='text/html; charset=utf-8', status=404)


def search(request):
    search_title = ''
    articles = []
    message = ''
    if request.method == 'POST':
        search_title = request.POST['title']
        if search_title != '':
            articles = Article.search_by_title(search_title)
        else:
            message = "please enter a title!"

    num_articles = len(articles)
    return render(request, 'searchArticle/search_article.html', {'articles': articles,
                                                                 'num_articles': num_articles,
                                                                 'search_title': search_title,
                                                                 'message': message})


def create_article(request):
    # TODO when we end to create authentication and authorization, change "User1"
    user = User.get_user_by_nickname("User1")

    if request.method == "POST":
        form = CreateArticleForm(request.POST, initial={'user_id': user})
        if form.is_valid():
            form.save()
            # TODO when we end to create the "my articles" page, change the redirect
            return render(request, 'landing/homepage.html', {'articles': Article.search_by_user(user)})
    elif request.method == "DELETE":
        raise Http404()
    else:
        form = CreateArticleForm(initial={'user_id': user})

    return render(request, 'article/article.html', {
        "user": user,
        'form': form,
    })


def my_articles(request, nickname=''):
    try:
        user = User.get_user_by_nickname(nickname)
        my_articles = Article.search_by_user(user)
        num_articles = len(my_articles)

        return render(request, 'myArticles/my_articles.html', {
            'user': user,
            'my_articles': my_articles,
            'num_articles': num_articles
        })
    except User.DoesNotExist:
        raise Http404()


def home_page(request):
    articles = []
    articles = Article.objects.all()
    return render(request, 'landing/homepage.html', {'articles': articles})


def about_page(request):
    return render(request, 'about/about.html', {})


def delete_article(request, article_pk):
    try:
        article = Article.objects.get(id=article_pk)
        article.delete()
        return redirect(home_page)

    except User.DoesNotExist:
        raise Http404()


def edit_article(request, article_pk):
    try:
        article = Article.objects.get(article_pk)

        initial = {'article_id': article, 'title': article.title,
                   'subject': article.subject_id, 'content': article.content}
        if request.method == "POST":
            form = EditArticleForm(request.POST, initial=initial)
            if form.is_valid():
                form.save()
                return render(request, 'editArticle/edit_article.html', initial)
        # elif request.method == "DELETE":
        #     raise Http404()
        else:
            form = EditArticleForm(initial=initial)

        return render(request, 'editArticle/edit_article.html', {
            'article_pk': article_pk,
            'form': form,
        })
    except User.DoesNotExist:
        # raise Http404()
        return redirect(home_page)
