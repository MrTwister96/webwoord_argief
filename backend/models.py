from django.db import models
import uuid
import os
from django.dispatch import receiver

class Prediker(models.Model):
    titel = models.CharField(verbose_name="Titel", max_length=20)
    naam = models.CharField(verbose_name="Naam", max_length=20)
    van = models.CharField(verbose_name="Van", max_length=20)
    sel = models.CharField(verbose_name="Selfoon", max_length=10, blank=True, null=True)
    epos = models.EmailField(verbose_name="e-Pos", max_length=50, blank=True, null=True)

    class Meta:
        ordering = ["van"]
        verbose_name = "Prediker"
        verbose_name_plural = "Predikers"

    def __str__(self):
        return f"{self.van}, {self.naam} ({self.titel})"
    
    def preek_count(self):
        return Preek.objects.filter(prediker=self).count()

class Gemeente(models.Model):
    naam = models.CharField(verbose_name="Gemeente Naam", max_length=50)
    prediker = models.ForeignKey("Prediker", on_delete=models.CASCADE)
    adres = models.CharField(verbose_name="Adres", max_length=100, blank=True, null=True)
    webwerf = models.URLField(verbose_name="Webwerf", max_length=100, blank=True, null=True)
    epos = models.EmailField(verbose_name="e-Pos", max_length=50, blank=True, null=True)
    tel = models.CharField(verbose_name="Telefoon", max_length=10, blank=True, null=True)

    class Meta:
        ordering = ["naam"]
        verbose_name = "Gemeente"
        verbose_name_plural = "Gemeentes"

    def __str__(self):
        return f"{self.naam}"
    
    def preek_count(self):
        return Preek.objects.filter(gemeente=self).count()

class Reeks(models.Model):
    naam = models.CharField(verbose_name="Reeks Naam", max_length=50)
    gemeente = models.ForeignKey("Gemeente", on_delete=models.CASCADE)

    class Meta:
        ordering = ["naam"]
        verbose_name = "Reeks"
        verbose_name_plural = "Reekse"

    def __str__(self):
        return f"{self.naam}"
    
    def preek_count(self):
        return Preek.objects.filter(reeks=self).count()

def audio_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/preke/<uuid>_<filename>
    return 'preke/{0}_{1}'.format(str(uuid.uuid4()), filename)

class Preek(models.Model):
    datum = models.DateTimeField(verbose_name="Datum", auto_now=False, auto_now_add=False)
    prediker = models.ForeignKey("Prediker", on_delete=models.CASCADE)
    reeks = models.ForeignKey("Reeks", on_delete=models.SET_NULL, blank=True, null=True)
    gemeente = models.ForeignKey("Gemeente", on_delete=models.CASCADE)
    tema = models.CharField(verbose_name="Tema", max_length=200)
    skriflesing = models.CharField(verbose_name="Skriflesing", max_length=200)
    audio_file = models.FileField(verbose_name="Audio File" ,upload_to=audio_path)

    class Meta:
        ordering = ["-datum"]
        verbose_name = "Preek"
        verbose_name_plural = "Preke"

    def __str__(self):
        return f"{self.tema}"
    
@receiver(models.signals.post_delete, sender=Preek)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.audio_file:
        if os.path.isfile(instance.audio_file.path):
            os.remove(instance.audio_file.path)

@receiver(models.signals.pre_save, sender=Preek)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Preek.objects.get(pk=instance.pk).audio_file
    except Preek.DoesNotExist:
        return False
    
    new_file = instance.audio_file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)