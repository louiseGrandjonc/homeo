from django.db.models import Q, OuterRef, Subquery, Count
from django.views.generic.list import ListView
from django.contrib.admin.views.decorators import staff_member_required

from homeo.models import ModeReactionnel, Cible, Medicament


class MedicamentList(ListView):
    model = Medicament
    template_name = "homeo/home.html"

    def get_context_data(self, **kwargs):
        context = super(MedicamentList, self).get_context_data(**kwargs)

        context['mode_list'] = ModeReactionnel.objects.all().order_by('position')
        context['cible_list'] = Cible.objects.all().order_by('position')

        context['selected_mode'] = self.modes
        context['selected_cibles'] = self.cibles

        return context

    def get_queryset(self):
        qs = super(MedicamentList, self).get_queryset()
        mode_ids = self.request.GET.getlist('mode')
        cible_ids = self.request.GET.getlist('cibles')

        self.cibles = None
        self.modes = None

        if mode_ids and 'all' not in mode_ids:
            try:
                self.modes = ModeReactionnel.objects.filter(pk__in=[int(m) for m in mode_ids])
            except:
                pass

        if cible_ids:
            try:
                self.cibles = Cible.objects.filter(pk__in=[int(c) for c in cible_ids])
            except:
                pass


        if self.modes:
            qs = qs.filter(Q(modes__in=self.modes) | Q(modes__isnull=True))

        if self.cibles:
            qs = qs.filter(cibles__in=self.cibles)

            qs = qs.annotate(score=Count('cibles', filter=Q(cibles__in=self.cibles))).order_by('-score', 'nom')

        return qs.prefetch_related('modes', 'cibles')


medicament_list = staff_member_required(MedicamentList.as_view())
