from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Coupon(models.Model):
    # Code that users have to enter in order to apply the coupon.
    code = models.CharField(max_length=50, unique=True)
    # The datetime value that indicates when the coupon becomes valid.
    valid_from = models.DateTimeField()
    # When the coupon becomes invalid.
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField()

    def __str__(self):
        return self.code

