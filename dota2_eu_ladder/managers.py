from collections import defaultdict
from django.db import models


class PlayerManager(models.Manager):
    # gives player initial score and mmr
    @staticmethod
    def init_score(player):
        from app.ladder.models import ScoreChange

        avg_mmr = 4000  # TODO: calculate it
        initial_mmr = 200 - 30 * (avg_mmr - player.mmr) / 1000

        score = ScoreChange.objects.create(
            player=player,
            amount=25,
            mmr_change=initial_mmr,
            info='Season started',
        )
        player.scorechange_set.add(score)

    def update_ranks(self):
        players = self.filter(matchplayer__isnull=False).distinct()
        players = players or self.all()

        # recalculate player rankings based on ladder-mmr
        mmr_groups = defaultdict(list)
        for player in players:
            mmr_groups[player.ladder_mmr].append(player)

        mmr_groups = sorted(mmr_groups.items(), reverse=True)

        for rank, group in enumerate(mmr_groups):
            for player in group[1]:
                player.rank = rank + 1
                player.save()


class MatchManager(models.Manager):
    @staticmethod
    def add_scores(match):
        from app.ladder.models import ScoreChange

        mmr_diff = match.balance.teams[0]['mmr'] - match.balance.teams[1]['mmr']
        underdog = 0 if mmr_diff <= 0 else 1
        underdog_bonus = abs(mmr_diff) / 5

        print 'mmr diff: %d' % mmr_diff
        print 'underdog: %d' % underdog
        print 'underdog bonus: %d / 50 = %d' % (abs(mmr_diff), underdog_bonus)
        print ''

        for matchPlayer in match.matchplayer_set.all():
            is_victory = 1 if matchPlayer.team == match.winner else -1
            is_underdog = 1 if matchPlayer.team == underdog else -1

            score_change = 1 * is_victory

            mmr_change = 7 * is_victory
            mmr_change += underdog_bonus * is_underdog

            print 'Player: %s  Team: %d' % (matchPlayer.player.name, matchPlayer.team)
            print 'is victory: %d' % is_victory
            print 'is_underdog: %d' % is_underdog
            print 'score change: %d' % score_change
            print 'mmr change: %+d' % mmr_change
            print ''

            ScoreChange.objects.create(
                player=matchPlayer.player,
                amount=score_change,
                mmr_change=mmr_change,
                match=matchPlayer,
            )


class ScoreChangeManager(models.Manager):
    pass
