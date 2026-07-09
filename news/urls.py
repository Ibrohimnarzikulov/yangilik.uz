from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    home_page, contact,
    single_page_view, sport_view, local_news_view,
    technology_news, edu_news, global_news,pagination
)

urlpatterns = [
    path('', home_page, name='home'),
    path('contact/', contact, name='contact'),
    # Single page faqat login qilgan foydalanuvchilar uchun
    path('new/<slug:slug>', login_required(single_page_view), name='single'),
    path('sports/', sport_view, name='sports'),
    path('technologies/', technology_news, name='technology_news'),
    path('edu/', edu_news, name='edu'),
    path('news/', local_news_view, name='local_news'),
    path('global/', global_news, name='global_news'),
    path('sport/', pagination, name='sport_news'),

]