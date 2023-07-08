from django.db import models

# Create your models here.

class Data(models.Model):
	person1 = models.ImageField(upload_to="images/")
	person2 = models.ImageField(upload_to="images/")
	height1 = models.FloatField()
	height2 = models.FloatField()
	final_image = models.ImageField(upload_to="images/", null=True, blank=True)

	def __str__(self):
		return f"Order id: {self.id}"