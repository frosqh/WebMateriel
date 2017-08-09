from django.db import models
from django.utils import timezone

# Create your models here.

class Famille(models.Model):
	nom = models.CharField(max_length=75, default='Famille')
	def __str__(self):
		return self.nom.encode('utf-8')

class SousFamille(models.Model):
	nom = models.CharField(max_length=75, default='Sous-Famille')
	familleID = models.ForeignKey(Famille, on_delete=models.CASCADE)
	def __str__(self):
		return self.nom.encode('utf-8')

class Pignouf(models.Model):
	nom = models.CharField(max_length=50, default='Nom')
	prenom = models.CharField(max_length=50, default='Prenom')
	def __str__(self):
		return (self.nom+" "+self.prenom).encode('utf-8')

class Fournisseur(models.Model):
	nom = models.CharField(max_length=50, default='Fournisseur')
	def __str__(self):
		return self.nom

class Autre(models.Model):
	text = models.CharField(max_length=25, default='-------------------------')
	def __str__(self):
		return self.text.encode('utf-8')

class Outil(models.Model):
	nom = models.CharField(max_length=75, default='Outil')
	numSerie = models.CharField(max_length=25, default='')
	autreId = models.ForeignKey(Autre, on_delete=models.CASCADE, null=True, blank=True)
	famille = models.ForeignKey(Famille, on_delete=models.CASCADE, blank=True)
	sousfamille = models.ForeignKey(SousFamille, on_delete=models.CASCADE,blank=True)
	isDispo = models.BooleanField(default=True)
	price = models.IntegerField
	fournisseurID = models.ForeignKey(Fournisseur, blank=True)
	emprunteur = models.ForeignKey(Pignouf, blank=True, null=True)
	def __str__(self):
		return self.nom +' ('+self.numSerie+'); '+str(self.autreId)+str(self.fournisseurID)+str(self.isDispo)

class HistoLigne(models.Model):
	creationDate = models.DateTimeField(default=timezone.now)
	stockChange = models.CharField(max_length=250, default='')
	pignoufID = models.ForeignKey(Pignouf, on_delete=models.CASCADE, blank=True, null=True)
	productID = models.ForeignKey(Outil, on_delete=models.CASCADE, blank=True, null=True)
	def __str__(self):
		strr = self.creationDate.strftime("%d-%m-%Y") +"  :  "+self.stockChange + "  --  "
		if (self.pignoufID != None):
			strr += str(self.pignoufID) +"  --  "
		if (self.productID != None):
			strr += self.productID.nom
		return strr.encode('utf-8')


