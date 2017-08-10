# coding: utf8

from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from main.models import *
from decimal import *
from .templates.main.signin import LoginForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def index(request):
	message=''
	outilList = None
	if (request.method == 'POST'):
		post = request.POST
		b = True
		if ('nomAddFamille' in post):
			nom = post['nomAddFamille']
			if (nom != ''):
				for f in Famille.objects.all():
					if (f.nom == nom):
						b = False;
						message = 'Cette famille existe déjà'
				if b:
					f = Famille(nom=nom)
					f.save();
					message = 'La famille '
					message += nom
					message += ' est ajoutée'.decode('utf-8')
			else:
				message = "Veuillez entrer un nom de famille"
		if ('nomAddSousFamille' in post):
			c = True
			nom = post['nomAddSousFamille']
			if 'nomFamille' in post:
				nomFamille = post['nomFamille']
			else:
				c = False
				message = 'Merci de choisir une famille'
			if c:
				if nom != '':
					for f in SousFamille.objects.all():
						if (f.nom == nom):
							b = False;
							message = 'Cette sous-famille existe déjà'
					if b:
						if nomFamille!='':
							fl = Famille.objects.all().filter(nom=nomFamille)
							if len(fl)>=1:
								f = fl[0]
								n = f.nom
								sf = SousFamille(nom=nom, familleID=f);
								nf = sf.familleID.nom
								sf.save()
								message = 'La sous-famille '
								message += nom
								message += ' est ajoutée'.decode('utf-8')
						else:
							message='Merci de sélectionner une famille'
				else:
					message='Veuillez entrer un nom de sous-famille'
		if ('nomAddFournisseur' in post):
			nom = post['nomAddFournisseur']
			if nom!='':
				for f in Fournisseur.objects.all():
					if f.nom == nom:
						b=False;
						message='Ce fournisseur existe déjà'
				if b:
					f = Fournisseur(nom=nom)
					f.save()
					message = 'Le fournisseur '
					message += nom
					message += ' est ajouté'.decode('utf-8')
			else:
				message='Veuillez entrer un nom de fournisseur'
		if ('nomAddOuvrier' in post):
			nom = post['nomAddOuvrier']
			prenom = post['prenom']
			if nom!='':
				if prenom!='':
					for p in Pignouf.objects.all():
						if p.nom == nom and p.prenom == prenom:
							b = False
							message='Cet ouvrier existe déjà'
					if b:
						o = Pignouf(nom=nom, prenom=prenom)
						o.save()
						message = "Le salarié ".decode('utf-8')
						message += nom +" "+prenom
						message += ' est ajouté'.decode('utf-8')
				else:
					message='Veuillez entrer un prenom'
			else:
				message='Veuillez entrer un nom de famille'
		if ('nomAddOutil' in post):
			c = True
			nom = post['nomAddOutil']
			if 'famille' in post:
				famille = post['famille']
			else:
				c = False
				message = 'Merci de choisir une famille'
			if 'sousfamille' in post:
				sousfamille = post['sousfamille']
			else:
				c = False
				message = 'Merci de choisir une sous-famille'
			numSerie = post['numSerie']
			if 'fournisseur' in post:
				fournisseur = post['fournisseur']
			else:
				c = False
				message = 'Merci de choisir un fournisseur'
			prix = Decimal(post['price'])
			date = post['dateEntreeB']
			dateR = datetime.strptime(date,'%Y-%m-%d')
			if c:
				if nom!='':
					if famille!='':
						if sousfamille!='':
							if numSerie!='':
								if fournisseur!='':
									fl = Famille.objects.all().filter(nom=famille)
									sfl = SousFamille.objects.all().filter(nom=sousfamille)
									fol = Fournisseur.objects.all().filter(nom=fournisseur)
									if len(fl)<1:
										b = False
									else:
										fam = fl[0]
									if len(sfl)<1:
										b = False
									else:
										sfam = sfl[0]
									if len(fol)<1:
										b = False
									else:
										four = fol[0]
									for o in Outil.objects.all():
										if o.nom == nom and o.numSerie == numSerie:
											b = False
											message='Cet outil existe déjà'
									if b:
										out = Outil(nom=nom, numSerie=numSerie, famille=fam, sousfamille=sfam, fournisseurID=four, price=prix)
										out.save()
										message = "L'outil ".decode('utf-8')
										message += nom 
										message += ' est ajouté'.decode('utf-8')
										h = HistoLigne(creationDate=dateR, stockChange='Achat initial',productID = out )
										h.save();
								else:
									message ='Veuillez entrer un fournisseur'
							else:
								message = 'Veuillez entrer un numéro de série'
						else:
							message ='Veuillez sélectionnez une sous-famille'
					else:
						message ='Veuillez sélectionnez une famille'
				else:
					message ='Veuillez entrer un nom'
		if ('nomAddAutre' in post):
			nom = post['nomAddAutre']
			if nom!='':
				for a in Autre.objects.all():
					if a.text == nom:
						b=False;
						message='Cette catégorie existe déjà'.decode('utf-8')
				if b:
					a = Autre(text=nom)
					a.save()
					message = 'La catégorie '.decode('utf-8')
					message += nom
					message += ' est ajouté'.decode('utf-8')
			else:
				message='Veuillez entrer un nom de catégorie'.decode('utf-8')
		if ('edit' in post):
			a = int(post['outilID'])
			outils = Outil.objects.all().filter(id=a)
			outil=outils[0]
			return render(request, 'main/edit.html', {'outil':outil, 'pignoufList':Pignouf.objects.all(), 'autreList':Autre.objects.all()})
		if ('dateSortie' in post and post['dateSortie']!=''):
			date = post['dateSortie']
			dateR = datetime.strptime(date,'%Y-%m-%d')
			pignoufName = post['pignouf']
			outilID = post['outilID']
			outilet = Outil.objects.all().filter(id=int(outilID))
			if len(outilet)<1:
				b = False
			else:
				outil = outilet[0]
			pignouf = None
			pignoufet = Pignouf.objects.all()
			for p in pignoufet:
				if str(p) == pignoufName:

					pignouf = p
			if pignouf == None:
				message = 'Merci de renseigner un ouvrier'
				b = False
			if b:
				h = HistoLigne(creationDate=dateR,stockChange='Sortie de stock', pignoufID=pignouf, productID=outil)
				h.save()
				outil.isDispo = False;
				outil.emprunteur = pignouf
				outil.save();
		if ('dateEntree' in post and post['dateEntree'] != ''):
			date = post['dateEntree']
			dateR = datetime.strptime(date,'%Y-%m-%d')
			outilID = post['outilID']
			outilet = Outil.objects.all().filter(id=int(outilID))
			if len(outilet)<1:
				b = False
			else:
				outil = outilet[0]
			if b:
				if (outil.emprunteur != None):
					pignouf = outil.emprunteur
					autre = ''
					outil.emprunteur = None
					stock = 'Retour ouvrier'
					h = HistoLigne(creationDate=dateR, stockChange=stock, pignoufID=pignouf, productID=outil)
				elif outil.autreId != None:
					autre = outil.autreId
					pignouf = ''
					outil.autreId = None
					stock = 'Retour de '+ str(autre)
					h = HistoLigne(creationDate=dateR, stockChange=stock, productID=outil)
				h.save()
				outil.isDispo = True
				outil.save()
		if ('dateAutre' in post and post['dateAutre'] != ''):
			date = post['dateAutre']
			dateR = datetime.strptime(date, '%Y-%m-%d')
			autreText = post['autre']
			autrepp = None
			autret = Autre.objects.all().filter(text=autreText)
			if len(autret)<1:
				b = False
				message = 'Merci de renseigner une catégorie "Autre"'
			else:
				autrep = autret[0]
			outilID = post['outilID']
			outilet = Outil.objects.all().filter(id=int(outilID))
			if len(outilet)<1:
				b = False
			else:
				outil = outilet[0]
			if b:
				if (outil.emprunteur != None):
					stock = 'De '+str(outil.emprunteur)+' vers '+autreText
					c = True
					pig = outil.emprunteur
				else:
					stock = 'Sortie de stock vers '+autreText
					c = False
				outil.emprunteur = None
				outil.autreId = autrep
				h  = HistoLigne(creationDate=dateR, stockChange=stock, productID=outil)
				if c:
					h.pignoufID= pig
				outil.isDispo = False
				outil.save()
				h.save()
		if ('name' in post and post['name'] == 'trinom'):
			if (request.session['sort'] == 'ASC'):
				request.session['sortby']='nom'
				request.session['sort'] = 'DESC'
			else:
				request.session['sortby']='-nom'
				request.session['sort'] = 'ASC'
		if ('name' in post and post['name'] == 'triid'):
			if (request.session['sort'] == 'ASC'):
				request.session['sortby']='numSerie'
				request.session['sort'] = 'DESC'
			else:
				request.session['sortby']='-numSerie'
				request.session['sort'] = 'ASC'
		if ('name' in post and post['name'] == 'tridispo'):
			if (request.session['sort'] == 'ASC'):
				request.session['sortby']='isDispo'
				request.session['sort'] = 'DESC'
			else:
				request.session['sortby']='-isDispo'
				request.session['sort'] = 'ASC'
		if ('name' in post and post['name'] == 'triemprunteur'):
			if (request.session['sort'] == 'ASC'):
				request.session['sortby']='emprunteur__nom'
				request.session['sort'] = 'DESC'
			else:
				request.session['sortby']='-emprunteur__nom'
				request.session['sort'] = 'ASC'
		if ('name' in post and post['name'] == 'triautre'):
			if (request.session['sort'] == 'ASC'):
				request.session['sortby']='autreId__text'
				request.session['sort'] = 'DESC'
			else:
				request.session['sortby']='-autreId__text'
				request.session['sort'] = 'ASC'
		if ('nomFamilleFilter' in post):
			request.session['filterFamille'] = post['nomFamilleFilter']
		if ('nomSousFamilleFilter' in post):
			request.session['filterSousFamille'] = post['nomSousFamilleFilter']
		if ('nomFournisseurFilter' in post):
			request.session['filterFournisseur'] = post['nomFournisseurFilter']
		if ('nomPignoufFilter' in post):
			request.session['filterPignouf'] = post['nomPignoufFilter']
		if ('nomAutreFilter' in post):
			request.session['filterAutre'] = post['nomAutreFilter']
		if ('nomDispoFilter' in post):
			request.session['filterDispo'] = post['nomDispoFilter']
		if ('reset' in post):
			if ('filterFamille' in request.session):
				request.session['filterFamille'] = ''
			if ('filterSousFamille' in request.session):
				request.session['filterSousFamille'] = ''
			if ('filterFournisseur' in request.session):	
				request.session['filterFournisseur'] = ''
			if ('filterPignouf' in request.session):
				request.session['filterPignouf'] = ''
			if ('filterAutre' in request.session):
				request.session['filterAutre'] = ''
			if ('filterDispo' in request.session):
				request.session['filterDispo'] = ''
			if ('sortby' in request.session):
				request.session['sortby'] = ''
		if ('supprFamille' in post):
			request.session['filterFamille'] = ''
		if ('supprSousFamille' in post):
			request.session['filterSousFamille'] = ''
		if ('supprFournisseur' in post):
			request.session['filterFournisseur'] = ''
		if ('supprPignouf' in post):
			request.session['filterPignouf'] = ''
		if ('supprDispo' in post):
			request.session['filterDispo'] = ''
		if ('supprAutre' in post):
			request.session['filterAutre'] = ''
		if ('login' in post):
			return HttpResponseRedirect('./login')
		if ('logout' in post):
			logout(request)

	else:
		request.session['sort'] = 'ASC'
	if outilList == None:
		outilList = Outil.objects.all()
		if ('filterFamille' in request.session and request.session['filterFamille'] != ''):
			outilList = outilList.filter(famille__nom__exact = request.session['filterFamille'])
		if ('filterSousFamille' in request.session and  request.session['filterSousFamille'] != ''):
			outilList = outilList.filter(sousfamille__nom__exact = request.session['filterSousFamille'])
		if ('filterFournisseur' in request.session and request.session['filterFournisseur'] != ''):
			outilList = outilList.filter(fournisseurID__nom__exact = request.session['filterFournisseur'])
		if ('filterPignouf' in request.session and request.session['filterPignouf'] != ''):
			pignoufName = request.session['filterPignouf']
			pignouf = None
			pignoufet = Pignouf.objects.all()
			for p in pignoufet:
				if str(p) == pignoufName:
					pignouf = p
			outilList = outilList.filter(emprunteur__exact = pignouf)
		if ('filterAutre' in request.session and request.session['filterAutre'] != ''):
			outilList = outilList.filter(autreId__text__exact = request.session['filterAutre'])
		if ('filterDispo' in request.session and request.session['filterDispo'] != ''):
			dispo = request.session['filterDispo']
			if (dispo == 'OUI'):
				outilList = outilList.filter(isDispo__exact = True)
			else:
				outilList = outilList.filter(isDispo__exact = False)
		if ('sortby' in request.session and request.session['sortby'] != ''):
			outilList = outilList.order_by(request.session['sortby'])
	return render(request, 'main/index.html', {'message': message,'init':True, 'outilList': outilList, 'famille': Famille.objects.all(), 'sousFamille':SousFamille.objects.all(), 'fournisseur': Fournisseur.objects.all(), 'pignoufs' : Pignouf.objects.all(), 'autre': Autre.objects.all()})

def outil(request, id=-1):
	if id == -1:
		return HttpResponse(status=404)
	outilet = Outil.objects.all().filter(id=id)
	if len(outilet) < 1:
		return HttpResponse(status=404)
	l = outilet[0]
	return render(request, 'main/outil.html', {'outil': l, 'histo': HistoLigne.objects.all().filter(productID=l)})
	

def ouvrier(request, id=-1):
	if id == -1:
		return HttpResponse(status=404)
	outilet = Pignouf.objects.all().filter(id=id)
	if len(outilet) < 1:
		return HttpResponse(status=404)
	l = outilet[0]
	return render(request, 'main/ouvrier.html', {'outil': l, 'histo': HistoLigne.objects.all().filter(pignoufID=l)})

def loginn(request):
	if (request.method=='POST'):
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username,password=password)
			if user is not None:
				login(request,user)
				clear(request)
				return HttpResponseRedirect("./")
			else:
				return render(request, 'main/login.html', {'form' : form, 'message' : 'Authentication failed'})
	else:
		form = LoginForm()
	if (request.user.is_authenticated):
		request.session['message'] = 'You are already connected'
		return HttpResponseRedirect('/')
	clear(request)
	return render(request, 'main/login.html', {'form' : form})

def clear(request):
	if ('message' in request.session):
		request.session.pop('message')