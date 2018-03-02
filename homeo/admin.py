from django.contrib import admin
from django import forms

from homeo.models import ModeReactionnel, Cible, Medicament


class MedicamentAdminForm(forms.ModelForm):
   modes = forms.ModelMultipleChoiceField(queryset=ModeReactionnel.objects.order_by('position'))
   cibles = forms.ModelMultipleChoiceField(queryset=Cible.objects.order_by('position'))

   class Meta:
      model = Medicament
      fields = ('modes', 'cibles', 'nom')


class MedicamentAdmin(admin.ModelAdmin):
    ordering = ('nom',)
    form = MedicamentAdminForm

admin.site.register(ModeReactionnel)
admin.site.register(Cible)
admin.site.register(Medicament, MedicamentAdmin)
