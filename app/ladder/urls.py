from app.ladder.views import PlayerList, PlayersSuccessful, MatchList, LadderStats, LobbyStatus, KimerStats
from app.ladder.views import PlayerOverview, PlayerScores, PlayerTeammates, PlayerOpponents
from app.ladder.views import PlayerAutocomplete
from django.urls import re_path

app_name = 'ladder'

urlpatterns = [
    re_path(r'^players/$', PlayerList.as_view(), name='player-list'),
    re_path(r'^players-successful/$', PlayersSuccessful.as_view(), name='player-list-score'),

    re_path(r'^players/(?P<slug>[-\w]+)/$', PlayerOverview.as_view(), name='player-overview'),
    re_path(r'^players/(?P<slug>[-\w]+)/scores/$', PlayerScores.as_view(), name='player-scores'),
    re_path(r'^players/(?P<slug>[-\w]+)/teammates/$', PlayerTeammates.as_view(), name='player-teammates'),
    re_path(r'^players/(?P<slug>[-\w]+)/opponents/$', PlayerOpponents.as_view(), name='player-opponents'),

    re_path(r'player-autocomplete', PlayerAutocomplete.as_view(), name='player-autocomplete'),

    re_path(r'^matches/$', MatchList.as_view(), name='match-list'),

    re_path(r'^stats/$', LadderStats.as_view(), name='stats'),
    re_path(r'^lobby-status/$', LobbyStatus.as_view(), name='lobby-status'),
    re_path(r'^kimer-stats/$', KimerStats.as_view(), name='kimer-stats'),
]
