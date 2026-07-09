"""
account/urls.py — URL konfiguratsiya va test funksiyalari

Bu faylda ikkita maxsus funksiya mavjud:
- main() — barcha view'larni JSON formatda sinaydi
- test() — batafsil test natijalarini ko'rsatadi

Testlarni ishga tushirish:
    python account/urls.py
"""

from django.urls import path
from django.http import JsonResponse
from django.shortcuts import render
from django.test import RequestFactory

# Django orqali import qilinsa — relative, to'g'ridan-to'g'ri run qilinsa — absolute
try:
    from . import views
except ImportError:
    import views


# ============================================================
# main() — barcha view'larni chaqirib tekshiradi (JSON)
# ============================================================
def main(request=None):
    """Saytdagi barcha asosiy funksiyalarni chaqiradi va natijani qaytaradi."""
    from news.views import (
        home_page, contact, single_page_view,
        sport_view, local_news_view, technology_news,
        edu_news, global_news,
    )
    from intractions.models import Comment, Like
    from news.models import Article, Category
    from .models import User

    if request is None:
        rf = RequestFactory()
        request = rf.get('/')

    results = {}

    # 1. home_page
    try:
        response = home_page(request)
        results['home_page'] = {'status': 'OK', 'code': response.status_code}
    except Exception as e:
        results['home_page'] = {'status': 'ERROR', 'error': str(e)}

    # 2. contact
    try:
        response = contact(request)
        results['contact'] = {'status': 'OK', 'code': response.status_code}
    except Exception as e:
        results['contact'] = {'status': 'ERROR', 'error': str(e)}

    # 3. sport_view
    try:
        response = sport_view(request)
        results['sport_view'] = {'status': 'OK', 'code': response.status_code}
    except Exception as e:
        results['sport_view'] = {'status': 'ERROR', 'error': str(e)}

    # 4. local_news_view
    try:
        response = local_news_view(request)
        results['local_news_view'] = {'status': 'OK', 'code': response.status_code}
    except Exception as e:
        results['local_news_view'] = {'status': 'ERROR', 'error': str(e)}

    # 5. edu_news
    try:
        response = edu_news(request)
        results['edu_news'] = {'status': 'OK', 'code': response.status_code}
    except Exception as e:
        results['edu_news'] = {'status': 'ERROR', 'error': str(e)}

    # 6. technology_news
    try:
        response = technology_news(request)
        results['technology_news'] = {'status': 'OK', 'code': response.status_code}
    except Exception as e:
        results['technology_news'] = {'status': 'ERROR', 'error': str(e)}

    # 7. global_news
    try:
        response = global_news(request)
        results['global_news'] = {'status': 'OK', 'code': response.status_code}
    except Exception as e:
        results['global_news'] = {'status': 'ERROR', 'error': str(e)}

    # 8. single_page_view
    try:
        first_article = Article.objects.filter(status='published').first()
        if first_article:
            response = single_page_view(request, slug=first_article.slug)
            results['single_page_view'] = {
                'status': 'OK',
                'code': response.status_code,
                'article_slug': first_article.slug,
            }
        else:
            results['single_page_view'] = {'status': 'SKIP', 'reason': "Maqola yo'q"}
    except Exception as e:
        results['single_page_view'] = {'status': 'ERROR', 'error': str(e)}

    # 9. Qidiruv
    try:
        search_req = RequestFactory().get('/?q=test')
        response = home_page(search_req)
        results['search'] = {'status': 'OK', 'code': response.status_code}
    except Exception as e:
        results['search'] = {'status': 'ERROR', 'error': str(e)}

    # 10. Modellar soni
    try:
        results['models'] = {
            'articles_count': Article.objects.count(),
            'comments_count': Comment.objects.count(),
            'likes_count':    Like.objects.count(),
            'users_count':    User.objects.count(),
            'categories_count': Category.objects.count(),
        }
    except Exception as e:
        results['models'] = {'status': 'ERROR', 'error': str(e)}

    return JsonResponse(results, json_dumps_params={'ensure_ascii': False})


# ============================================================
# test() — batafsil test natijalari (HTML sahifa)
# ============================================================
def test(request=None):
    """Barcha funksiyalarni alohida-alohida tekshiradi."""
    from news.views import (
        home_page, contact, single_page_view,
        sport_view, local_news_view, technology_news,
        edu_news, global_news,
    )
    from intractions.models import Comment, Like
    from news.models import Article, Category
    from .models import User

    rf = RequestFactory()
    test_results = []

    def add_result(name, ok, detail=''):
        test_results.append({
            'name': name,
            'status': '✅ PASS' if ok else '❌ FAIL',
            'detail': detail,
        })
        # Konsolga ham chiqaramiz
        print(f"  {test_results[-1]['status']} {name}: {detail}")

    print("\n" + "=" * 60)
    print("🧪  YANGILIK.UZ SAYTI TESTLARI")
    print("=" * 60)

    # 1. Bosh sahifa
    try:
        response = home_page(rf.get('/'))
        add_result('Bosh sahifa (home_page)', response.status_code == 200,
                   f'Status: {response.status_code}')
    except Exception as e:
        add_result('Bosh sahifa (home_page)', False, str(e))

    # 2. Aloqa
    try:
        response = contact(rf.get('/contact/'))
        add_result('Aloqa (contact)', response.status_code == 200,
                   f'Status: {response.status_code}')
    except Exception as e:
        add_result('Aloqa (contact)', False, str(e))

    # 3. Sport
    try:
        response = sport_view(rf.get('/sports/'))
        add_result('Sport yangiliklari', response.status_code == 200,
                   f'Status: {response.status_code}')
    except Exception as e:
        add_result('Sport yangiliklari', False, str(e))

    # 4. Mahalliy
    try:
        response = local_news_view(rf.get('/news/'))
        add_result('Mahalliy yangiliklar', response.status_code == 200,
                   f'Status: {response.status_code}')
    except Exception as e:
        add_result('Mahalliy yangiliklar', False, str(e))

    # 5. Texnologiya
    try:
        response = technology_news(rf.get('/technologies/'))
        add_result('Texnologiya yangiliklari', response.status_code == 200,
                   f'Status: {response.status_code}')
    except Exception as e:
        add_result('Texnologiya yangiliklari', False, str(e))

    # 6. Ta'lim
    try:
        response = edu_news(rf.get('/edu/'))
        add_result("Ta'lim yangiliklari", response.status_code == 200,
                   f'Status: {response.status_code}')
    except Exception as e:
        add_result("Ta'lim yangiliklari", False, str(e))

    # 7. Global
    try:
        response = global_news(rf.get('/global/'))
        add_result('Global yangiliklar', response.status_code == 200,
                   f'Status: {response.status_code}')
    except Exception as e:
        add_result('Global yangiliklar', False, str(e))

    # 8. Bitta maqola
    try:
        first_article = Article.objects.filter(status='published').first()
        if first_article:
            response = single_page_view(
                rf.get(f'/new/{first_article.slug}/'),
                slug=first_article.slug,
            )
            add_result('Bitta maqola sahifasi', response.status_code in [200, 302],
                       f"Slug: {first_article.slug}, Status: {response.status_code}")
        else:
            add_result('Bitta maqola sahifasi', False, "Maqola yo'q")
    except Exception as e:
        add_result('Bitta maqola sahifasi', False, str(e))

    # 9. Qidiruv
    try:
        response = home_page(rf.get('/?q=django'))
        add_result('Qidiruv funksiyasi', response.status_code == 200,
                   f'Status: {response.status_code}')
    except Exception as e:
        add_result('Qidiruv funksiyasi', False, str(e))

    # 10. Maqola yaratish
    try:
        test_user = User.objects.first()
        test_category = Category.objects.first()
        if test_user and test_category:
            article = Article.objects.create(
                title='TEST: Test maqolasi',
                body='Bu test maqolasi.',
                author=test_user,
                category=test_category,
                status='draft',
            )
            add_result('Maqola yaratish', article.pk is not None, f"ID: {article.pk}")
            article.delete()
        else:
            add_result('Maqola yaratish', False, 'User yoki Category yo\'q')
    except Exception as e:
        add_result('Maqola yaratish', False, str(e))

    # 11. Comment yaratish
    try:
        first_article = Article.objects.filter(status='published').first()
        test_user = User.objects.first()
        if first_article and test_user:
            comment = Comment.objects.create(
                article=first_article,
                author=test_user,
                body='TEST: Test izoh',
            )
            add_result('Comment yaratish', comment.pk is not None, f"ID: {comment.pk}")
            comment.delete()
        else:
            add_result('Comment yaratish', False, 'Maqola yoki User yo\'q')
    except Exception as e:
        add_result('Comment yaratish', False, str(e))

    # 12. Like yaratish
    try:
        first_article = Article.objects.filter(status='published').first()
        test_user = User.objects.first()
        if first_article and test_user:
            like, created = Like.objects.get_or_create(
                article=first_article,
                user=test_user,
            )
            add_result('Like yaratish', like.pk is not None,
                       f"ID: {like.pk}, Yangi: {created}")
            like.delete()
        else:
            add_result('Like yaratish', False, 'Maqola yoki User yo\'q')
    except Exception as e:
        add_result('Like yaratish', False, str(e))

    # 13. Login required
    try:
        first_article = Article.objects.filter(status='published').first()
        if first_article:
            response = single_page_view(
                rf.get(f'/new/{first_article.slug}/'),
                slug=first_article.slug,
            )
            add_result('Login talab qilish', response.status_code == 302,
                       f"Redirect status: {response.status_code}")
        else:
            add_result('Login talab qilish', False, 'Maqola yo\'q')
    except Exception as e:
        add_result('Login talab qilish', False, str(e))

    # Yakuniy statistika
    total = len(test_results)
    passed = sum(1 for r in test_results if '✅' in r['status'])
    failed = sum(1 for r in test_results if '❌' in r['status'])

    print("=" * 60)
    print(f"📊  NATIJA: Jami: {total} | ✅ O'tdi: {passed} | ❌ Xato: {failed}")
    print("=" * 60 + "\n")

    # Agar Django orqali chaqirilgan bo'lsa — HTML sahifa qaytaramiz
    if hasattr(request, 'META') and 'HTTP_HOST' in request.META:
        context = {
            'test_results': test_results,
            'total': total,
            'passed': passed,
            'failed': failed,
        }
        return render(request, 'test_results.html', context)

    # Aks holda — dict qaytaramiz
    return {
        'test_results': test_results,
        'total': total,
        'passed': passed,
        'failed': failed,
    }


# ============================================================
# URL patterns — main va test sahifalariga yo'l
# ============================================================
urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/',    views.login_view,    name='login'),
    path('logout/',   views.logout_view,   name='logout'),
    path('profile/',  views.profile_view,  name='profile'),
    path('main/',     main,                name='main'),
    path('test/',     test,                name='test'),
]


# ============================================================
# python account/urls.py  —  to'g'ridan-to'g'ri ishga tushirish
# ============================================================
if __name__ == '__main__':
    import django
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    test()