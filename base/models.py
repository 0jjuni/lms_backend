from django.db import models
# Create your models here.


class Batch(models.Model):
    name = models.CharField(
        max_length=4,
        blank=False
    )

    class Meta:
        verbose_name_plural = "batches"

    def __str__(self) -> str:
        return self.name