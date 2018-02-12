from django.db.models import Q, OuterRef, Subquery, Count
from django.views.generic.list import ListView

from homeo.models import ModeReactionnel, Cible, Medicament


class MedicamentList(ListView):
    model = Medicament
    template_name = "homeo/home.html"

    def get_context_data(self, **kwargs):
        context = super(MedicamentList, self).get_context_data(**kwargs)

        context['mode_list'] = ModeReactionnel.objects.all()
        context['cible_list'] = Cible.objects.all()

        context['selected_mode'] = self.mode
        context['selected_cibles'] = self.cibles

        return context

    def get_queryset(self):
        qs = super(MedicamentList, self).get_queryset()
        mode_id = self.request.GET.get('mode')
        cible_ids = self.request.GET.getlist('cibles')

        self.cibles = None
        self.mode = None

        if mode_id and mode_id != 'all':
            try:
                self.mode = ModeReactionnel.objects.get(pk=int(mode_id))
            except:
                pass

        if cible_ids:
            try:
                self.cibles = Cible.objects.filter(pk__in=[int(c) for c in cible_ids])
            except:
                pass


        if self.mode:
            qs = qs.filter(Q(modes__in=[self.mode]) | Q(modes__isnull=True))

        if self.cibles:
            qs = qs.filter(cibles__in=self.cibles)

            qs = qs.annotate(score=Count('cibles', filter=Q(cibles__in=self.cibles))).order_by('-score', 'nom')

        return qs.prefetch_related('modes', 'cibles')


medicament_list = MedicamentList.as_view()
