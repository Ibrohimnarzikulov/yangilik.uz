from datetime import timezone

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from intractions.models import Comment
from .models import Article, ContactMessage
from django.core.paginator import Paginator


def home_page(request):
    lastest_news = Article.published.all()[0]
    lastest_new = Article.published.all()[1:5]
    categories_new = Article.objects.filter(status='published', category__name='Sport')
    technoly_new = Article.objects.filter(status='published', category__name='Technology')
    iqtisod_new = Article.objects.filter(status='published', category__name='Milliy')
    edu_new = Article.objects.filter(status='published', category__name='Education')

    query = request.GET.get('q', '')
    if query:
        article = Article.published.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )
        return render(request, 'search.html', {'article': article})

    context = {
        'lastest_news': lastest_news,
        'lastest_new': lastest_new,
        'categories_new': categories_new,
        'technoly_new': technoly_new,
        'iqtisod_new': iqtisod_new,
        'edu_new': edu_new,
    }
    return render(request, 'index.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if not name or not email or not message:
            messages.error(request, "Iltimos, barcha majburiy maydonlarni to'ldiring.")
            return redirect('contact')

        ContactMessage.objects.create(
            name=name, email=email, subject=subject, message=message,
        )

        return redirect('home')

    return render(request, 'contact.html')


def single_page_view(request, slug):
    article = get_object_or_404(Article, slug=slug)
    comments = Comment.objects.filter(article=article,perent__insull=True).select_related('author').order_by('-created_at')


    viewed = request.session.get('viewed_articles', [])

  
    viewed = request.session.get('viewed_articles', [])


    if article.id not in viewed:
        article.views_count += 1
        article.save()

        viewed.append(article.id)
        request.session['viewed_articles'] = viewed
    if request.method == 'POST':
        body = request.POST.get('body', '').strip()
        perent_id=request.POST.get(parent_id)
        if body:
            Comment.objects.create(
                article=article,
                body=body,
                author=request.user,
                perent_id=perent_id,
            )
            messages.success(request, "Fikringiz qo'shildi!")
            return redirect('single', slug=slug)
        else:
            messages.error(request, "Fikr matni bo'sh bo'lmasligi kerak.")

    context = {
        "article": article,
        "comments": comments,
    }
    return render(request, "single-page.html", context)


def sport_view(request):
    lastest_news = Article.published.filter(category__name='Sport')
    context = {
        'lastest_news': lastest_news,
    }
    return render(request, "sport.html", context)


def local_news_view(request):
    lastest_news = Article.published.filter(category__name='Milliy')
    context = {
        'lastest_news': lastest_news,
    }
    return render(request, "local-news.html", context)


def edu_news(request):
    lastest_news = Article.published.filter(category__name="Ta'lim")
    context = {
        'lastest_news': lastest_news,
    }
    return render(request, "edu-news.html", context)


def technology_news(request):
    technology_news = Article.published.filter(category__name='Technology')
    context = {
        'technology_news': technology_news,
    }
    return render(request, "tech-news.html", context)


def global_news(request):
    global_news = Article.published.filter(category__name='Global')
    context = {
        'global_news': global_news,
    }
    return render(request, "global-news.html", context)



def pagination(request):
    articles = Article.published.filter(category__name='Sport')
    pagination=Paginator(articles, 3)
    page_number = request.GET.get('page')
    page_obj = pagination.get_page(page_number)
    context = {
        'page_obj': page_obj
    }

    return render(request, 'pagination.html', context)
