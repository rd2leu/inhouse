from django.urls import re_path

from app.balancer.views import BalancerInput, BalancerResult, BalancerInputCustom, MatchCreate, BalancerAnswer, \
    MatchDelete, RecordMatch

app_name = 'balancer_app'

urlpatterns = [
    re_path(r'^$', BalancerInput.as_view(), name='balancer-input'),
    re_path(r'^balancer-input-custom', BalancerInputCustom.as_view(), name='balancer-input-custom'),

    re_path(r'^results/(?P<pk>[0-9]+)/$', BalancerResult.as_view(),
        name='balancer-result'),
    re_path(r'^answers/(?P<pk>[0-9]+)/$', BalancerAnswer.as_view(),
        name='balancer-answer'),

    re_path(r'^answers/(?P<pk>[0-9]+)/match-create/(?P<winner>[0-1])/$', MatchCreate.as_view(),
        name='match-create'),
    re_path(r'^answers/(?P<pk>[0-9]+)/match-delete/$', MatchDelete.as_view(),
        name='match-delete'),

    re_path(r'^record-match/$', RecordMatch.as_view(), name='record-match'),
]
