from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile
from countries.models import Country, UsState

import datetime
YEAR_CHOICES = []
for r in range(1974, (datetime.datetime.now().year+5)):
	    YEAR_CHOICES.append((r,r))

MAJOR_CHOICES = []
for r in range(1, 25):
	if r == 13 or r == 19:
		continue
	MAJOR_CHOICES.append((str(r),str(r)))
MAJOR_CHOICES.extend([('STS', 'STS'), ('WGS', 'WGS'), ('CMS', 'CMS')])
#		 ('ES', 'Energy Studies'), ('AADS', 'African & African Diaspora Studies'), ('AIS', 'Applied International Studies'), ('Astronomy', 'Astronomy'), ('MES', 'Middle Eastern Studies'), ('PP', 'Public Policy'), ('RES', 'Russian and Eurasian Studies'), ('TEH', 'Toxicology and Environmental Health')])

MINOR_CHOICES = [
	('AADS', 'African & African Diaspora Studies'),
	('AS', 'American Studies'),
	('AMS', 'Ancient & Medieval Studies'),
	('Anthro', 'Anthropology'),
	('AIS', 'Applied International Studies'),
	('AAS', 'Archaeology and Archaeological Science'),
	('ACT', 'Art, Culture and Technology'),
	('AADS', 'Asian & Asian Diaspora Studies'),
	('CMS', 'Comparative Media Studies'),
	('DE', 'Development Economics'),
	('Econ', 'Economics'),
	('ES', 'Energy Studies'),
	('Ethics', 'Ethics'),
	('French', 'French'),
	('German', 'German'),
	('Spanish', 'Spanish'),
	('Chinese', 'Chinese'),
	('Japanese', 'Japanese'),
	('ELS', 'ELS'),
	('Portuguese', 'Portuguese'),
	('OL', 'Other Language'),
	('SILC', 'Studies in International Literatures and Cultures'),
	('TOL', 'Theory of Languages'),
	('Hist', 'History'),
	('HAA', 'History of Architecture and Art'),
	('LALS', 'Latin American & Latino Studies'),
	('Ling', 'Linguistics'),
	('Lit', 'Literature'),
	('MES', 'Middle Eastern Studies'),
	('Music', 'Music'),
	('Phil', 'Philosophy'),
	('Polisci', 'Political Science'),
	('PP', 'Public Policy'),
	('Psych', 'Psychology'),
	('RS', 'Religious Studies'),
	('RES', 'Russian and Eurasian Studies'),
	('STS', 'Science, Technology, and Society'),
	('Theater', 'Theater Arts'),
	('TOS', 'Toxicology and Environmental Health'),
	('US', 'Urban Studies'),
	('WGS', "Women's and Gender Studies"),
	('Writing', 'Writing'),
	]

DEPT_CHOICES = [('BS', 'BS'), ('MS', 'MS'), ('MEng', 'MEng'), ('PhD', 'PhD'),
		('Exchange', 'Exchange')]

MODIFIER_CHOICES = (
	('1', '1'),
	('2', '2'),
	('3', '3'),
	('7', '7'),
	('A', 'A'),
	('B', 'B'),
	('C', 'C'),
	('E', 'E'),
	('ENG', 'ENG'),
	('F', 'F'),
	('H', 'H'),
	('L', 'L'),
	('M', 'M'),
	('OE', 'OE'),
	('W', 'W'),
)

EXEC_CHOICES = (
	('pres', 'President'),
	('vp', 'Vice President'),
	('secretary', 'Secretary'),
	('hm', 'House Manager'),
	('foodstud', 'Food Steward'),
	('social', 'Social Chair'),
	('treasurer', 'Treasurer'),
	('memco', 'Membership Coordinator'),
	('mal', 'Member at Large'),
	('risk', 'Risk Manager'),
	('rush', 'Rush Chair'),
	)

SEMESTERS = (
	('sp', 'Spring'),
	('su', 'Summer'),
	('fa', 'Fall'),
	('iap', 'IAP'),
	)

def tuplify(x):
	return (x, x) 

def tuplify_list(l):
	return [tuplify(x) for x in l]

class Location(models.Model):
	city = models.CharField(max_length=100, null=True, blank=True)
	state = models.CharField(max_length=100, null=True, blank=True, choices=tuplify_list(UsState.objects.all().values_list('name', flat=True)))
	country = models.CharField(max_length=100, choices=tuplify_list(Country.objects.all().values_list('name', flat=True)))
	major_city = models.CharField(_('Major nearby city'), max_length=70, null=True, blank=True )
	current = models.BooleanField(_('Current location?'), default=False)
	hometown = models.BooleanField(_('Hometown?'), default=False)
	user = models.ForeignKey('MyProfile')

class Affiliation(models.Model):
	institution = models.CharField(max_length=80)
	role = models.CharField(max_length=80)
	start_date = models.DateField()
	end_date = models.DateField(null=True)
	user = models.ForeignKey('MyProfile')

class Major(models.Model):
	number = models.CharField(_('Course'), choices=MAJOR_CHOICES, max_length=15)
	modifier = models.CharField(max_length=5, choices=MODIFIER_CHOICES, null=True, blank=True) # ex. "3", "OE", "C"
	user = models.ForeignKey('MyProfile')
	degree = models.CharField(_('Degree'), choices=DEPT_CHOICES, null=True, blank=True, max_length=10)


class MinorConc(models.Model):
	area = models.CharField(_('Area'), choices=MINOR_CHOICES, max_length=40)
	minortype = models.CharField(_('Association'), choices=[('Minor', 'Minor'), ('Concentration', 'Concentration')], max_length=20)
	user = models.ForeignKey('MyProfile')

class ExecRole(models.Model):
	title = models.CharField(choices=EXEC_CHOICES, max_length=40)
	year = models.IntegerField(_('year'), max_length=4, choices=YEAR_CHOICES, default=datetime.datetime.now().year)
	semester = models.CharField(choices=SEMESTERS, max_length=40)
	user = models.ForeignKey('MyProfile')

class MyProfile(UserenaBaseProfile):
        user = models.OneToOneField(User,unique=True,
                                    verbose_name=_('user'),related_name='my_profile')
	year = models.IntegerField(_('year'), max_length=4, choices=YEAR_CHOICES, default=datetime.datetime.now().year)
        oww = models.ForeignKey('self', null=True, blank=True, related_name='old_wise_one', verbose_name=_('Old wise one'))
	blurb = models.CharField(max_length=500, null=True, blank=True, verbose_name=_('You can ask me about...'))
	school = models.CharField(max_length=500, default='MIT')

	def __unicode__(self):
		return self.user.first_name + ' ' +  self.user.last_name + ' (' + str(self.year) + ')'

	def get_ydos(self):
		return self._default_manager.all().filter(oww__user__username=self.user.username)

	def get_bs_set(self):
		qset = self.major_set.filter(degree="BS")
		if not qset:
			# if they didn't have any BS degrees, they were probably
			# a special case. return all (other) degrees
			return self.major_set.all()
		return qset
