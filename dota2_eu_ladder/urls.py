"""dota2_eu_ladder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from app.ladder.views import PlayersSuccessful
from django.urls import re_path, include
from django.contrib import admin

from app.ladder import urls as ladder_urls
from app.balancer import urls as balancer_urls
from dota2_eu_ladder import settings

app_name = 'rd2l_ladder'

urlpatterns = [
    re_path(r'^$', PlayersSuccessful.as_view(), name='index'),

    re_path(r'^', include(ladder_urls, namespace='ladder')),
    re_path(r'^balancer/', include(balancer_urls, namespace='balancer')),

    re_path(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ]