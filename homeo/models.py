from django.db import models


COLORS = (
    ('yellow', 'Jaune'),
    ('red', 'Rouge'),
    ('blue', 'Bleu'),
    ('green', 'Vert'),
)


class ModeReactionnel(models.Model):
    nom = models.CharField(max_length=255)
    color = models.CharField(choices=COLORS, max_length=10)

    def __str__(self):
        return '%s - %s' % (self.nom, self.get_color_display())


class Cible(models.Model):
    nom = models.CharField(max_length=255)

    def __str__(self):
        return self.nom


class Medicament(models.Model):
    nom = models.CharField(max_length=255)
    modes = models.ManyToManyField(ModeReactionnel, related_name='medicaments', blank=True)
    cibles = models.ManyToManyField(Cible, related_name='medicaments', through='MedicamentCibles')

    def __str__(self):
        return self.nom


class MedicamentCibles(models.Model):
    medicament = models.ForeignKey(Medicament, on_delete=models.CASCADE)
    cible = models.ForeignKey(Cible, on_delete=models.CASCADE)

    class Meta:
        db_table = 'homeo_medicament_cibles'
