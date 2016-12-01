from django.contrib.auth.mixins import PermissionRequiredMixin
from app.balancer import models
from app.balancer.balancer import balance_teams
from app.balancer.forms import BalancerForm, BalancerCustomForm
from app.balancer.models import BalanceResult, BalanceAnswer
from app.ladder.models import Player, Match, MatchPlayer
from django.core.paginator import PageNotAnInteger
from django.core.urlresolvers import reverse_lazy, reverse
from django.db import transaction
from django.http import Http404, HttpResponseBadRequest
from django.views.generic import FormView, DetailView, RedirectView
from pure_pagination import Paginator


class BalancerInput(FormView):
    form_class = BalancerForm
    template_name = 'balancer/balancer-input.html'

    def form_valid(self, form):
        players = [(p.name, p.mmr) for p in form.cleaned_data.values()]

        # balance teams and save result
        answers = balance_teams(players)

        self.result = models.BalanceResult.objects.create()
        for answer in answers:
            models.BalanceAnswer.objects.create(
                answer=answer,
                result=self.result
            )

        return super(BalancerInput, self).form_valid(form)

    def get_success_url(self):
        return reverse('balancer:balancer-result', args=(self.result.id,))


class BalancerInputCustom(FormView):
    form_class = BalancerCustomForm
    template_name = 'balancer/balancer-input-custom.html'

    def form_valid(self, form):
        players = [form.cleaned_data['player_%s' % i] for i in xrange(1, 11)]
        mmrs = [form.cleaned_data['MMR_%s' % i] for i in xrange(1, 11)]

        # balance teams and save result
        answers = balance_teams(zip(players, mmrs))

        self.result = BalanceResult.objects.create()
        for answer in answers:
            BalanceAnswer.objects.create(
                answer=answer,
                result=self.result
            )

        return super(BalancerInputCustom, self).form_valid(form)

    def get_success_url(self):
        return reverse('balancer:balancer-result', args=(self.result.id,))


class BalancerResult(DetailView):
    model = BalanceResult
    template_name = 'balancer/balancer-result.html'
    context_object_name = 'result'

    def get_context_data(self, **kwargs):
        context = super(BalancerResult, self).get_context_data(**kwargs)

        # paginate
        page_num = self.request.GET.get('page', 1)
        try:
            answers = context['result'].answers.all()
            page = Paginator(answers, 1, request=self.request).page(page_num)
        except PageNotAnInteger:
            raise Http404

        answer = page.object_list[0].answer

        # TODO: make a result.mmr_exponent DB field,
        # TODO: make an Answer model
        mmr_exponent = 3

        players = [p for team in answer['teams'] for p in team['players']]
        mmr_max = max([player[1] ** mmr_exponent for player in players])

        for team in answer['teams']:
            for i, player in enumerate(team['players']):
                mmr_percent = float(player[1] ** mmr_exponent) / mmr_max * 100
                team['players'][i] = {
                    'name': player[0],
                    'mmr': player[1],
                    'mmr_percent': mmr_percent
                }
                print player

        context.update({
            'answer': answer,
            'pagination': page,
        })

        return context


class MatchCreate(PermissionRequiredMixin, RedirectView):
    url = reverse_lazy('ladder:player-list')
    permission_required = 'ladder.add_match'

    def get(self, request, *args, **kwargs):
        answer = int(kwargs['answer'])

        try:
            result = BalanceResult.objects.get(id=kwargs['pk'])
            answer = result.answers.all()[answer]
        except (BalanceResult.DoesNotExist, IndexError):
            return HttpResponseBadRequest(request)

        if answer.match:
            # we already created a match from this BalanceAnswer
            return HttpResponseBadRequest(request)

        # check that players from balance exist
        # (we don't allow CustomBalance results here)
        players = [p[0] for t in answer.answer['teams'] for p in t['players']]
        players = Player.objects.filter(name__in=players)

        if len(players) < 10:
            return HttpResponseBadRequest(request)

        with transaction.atomic():
            match = Match.objects.create(winner=int(kwargs['winner']))

            for i, team in enumerate(answer.answer['teams']):
                for player in team['players']:
                    player = next(p for p in players if p.name == player[0])

                    MatchPlayer.objects.create(
                        match=match,
                        player=player,
                        team=i
                    )
                    answer.save()

            Player.objects.update_ranks()

            answer.match = match
            answer.save()

        return super(MatchCreate, self).get(request, *args, **kwargs)
