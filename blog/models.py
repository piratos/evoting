from django.db import models
from django.contrib.auth.models import User
import ast

class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return unicode(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


class Votant(models.Model):
    user= models.OneToOneField(User)
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    num_cin=models.IntegerField()
    nationality=models.CharField(max_length=30)
    adress=models.CharField(max_length=300)
    sex =(
    ('F', 'Femme'),
    ('M', 'Homme'),
    )
    sex = models.CharField(max_length=128, choices=sex, default="M")
    age=models.DateField()
    list_vote=ListField()

    def __unicode__(self):
        return self.user.username
    def did_voted(self, event):
        for i in self.list_vote:
            if i == event.id:
                return True
        return False

class Condidate(models.Model):
    user= models.OneToOneField(User)
    first_name = models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    age= models.DateField()
    num_cin=models.IntegerField()
    nationality=models.CharField(max_length=30)
    adress=models.CharField(max_length=300)
    sex =(
    ('F', 'Femme'),
    ('M', 'Homme'),
    )
    sex = models.CharField(max_length=128, choices=sex, default="M")
    nb_vote=models.IntegerField(default=0, null=True)
    pourcentage=models.IntegerField(default=0, null=True)
    picture=models.ImageField(upload_to='profile_images/',blank=True)
    contenu = models.TextField(null=True)
    evenement = models.ForeignKey('evenement')
    job=models.CharField(max_length=50)
    list_vote=ListField(blank=True, null=True)
    def __unicode__(self):
        return self.user.username




class evenement(models.Model):
    nom = models.CharField(max_length=30)
    date_fin_register = models.DateField()
    date_debut_vote = models.DateField()
    date_fin_vote = models.DateField()
    description=models.TextField()


    def __unicode__(self):
         return self.nom




