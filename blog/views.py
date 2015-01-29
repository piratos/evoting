from django.shortcuts import render, Http404
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from blog.forms import UserForm, VotantForm, CondidateForm
import datetime
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render_to_response
from .models import *
from blog.forms import ContactForm


def register_votant(request):
    register = False
    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = VotantForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            register = True
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = VotantForm()
    return render(request,
                  'registerV.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'register': register})


def register_condidate(request):
    if request.method == 'POST':
        register = False
        date = False
        event = evenement.objects.get(id=int(request.POST["evenement"]))
        date = test(event.date_fin_register)
        user_form = UserForm(data=request.POST)
        profile_form = CondidateForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            register = True
        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = CondidateForm()
    return render(request,
                  'registerC.html',
                  locals(),)


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:

                return HttpResponse("Your account is disabled.")
        else:

            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:

        return render(request, 'login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def home(request):
    events = evenement.objects.all()
    return render(request, 'home.html', locals())


def test_vote(date1, date2):
    date_courant = datetime.datetime.now().date()
    if (date_courant >= date1) & (date_courant <= date2):
        return True
    return False


def test_register(date1, date2):
    date_courant = datetime.datetime.now().date()
    if (date_courant >= date1) & (date_courant <= date2):
        return True
    return False


@login_required
def vote(request, name_condidate):
    user = request.user
    erreur = False
    voted = False
    try:
        person = Votant.objects.get(user=user)
    except Votant.DoesNotExist:
        try:
            person = Condidate.objects.get(user=user)
        except Condidate.DoesNotExist:
            erreur = True
    try:
        condidate = Condidate.objects.get(user=User.objects.get(username=name_condidate))
    except Condidate.DoesNotExist:
        erreur = True
    event = condidate.evenement
    if test_vote(event.date_debut_vote, event.date_fin_vote) and not erreur:
        if person.did_voted(event):
            voted = True
        else:
            condidate.nb_vote += 1
            condidate.save()
            person.list_vote.append(event.id)
            person.save()
    return render(request, 'vote.html', locals())

@login_required()
def choice(request, Event):
    try:
        event = evenement.objects.get(nom=Event)
    except evenement.DoesNotExist:
        raise Http404
    try:
        person = Condidate.objects.get(user=request.user)
    except Condidate.DoesNotExist:
        try:
            person = Votant.objects.get(user=request.user)
            voted = person.did_voted(event)
        except Votant.DoesNotExist:
            pass
    condidats = Condidate.objects.filter(evenement=event)
    date = not test(event.date_fin_vote)
    return render(request, 'choice.html', locals())


def profil(request, id_condidate):
    try:
        condidate = Condidate.objects.get(id=id_condidate)
    except Condidate.DoesNotExist:
        raise Http404
    return render(request, 'profil.html', locals())


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            topic = form.cleaned_data['topic']
            message = form.cleaned_data['message']
            email = form.cleaned_data['renvoi']
            name = form.cleaned_data['name']
            try:
                send_mail(name, topic, message, email, ['sirine.ghanmi@hotmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

    else:  # GET
        form = ContactForm()
    return render(request, 'contact.html', locals())


def thankyou(request):
    return render_to_response('thankyou.html')


def result(request, id_event):
    date_courant = datetime.datetime.now().date()
    event = evenement.objects.get(id=id_event)
    if date_courant > event.date_fin_vote:
        condidats = Condidate.objects.filter(evenement=event).order_by('-nb_vote')
        somme = 0
        for condidat in condidats:
            somme += condidat.nb_vote
        for condidat in condidats:
            condidat.pourcentage = condidat.nb_vote*100/somme
            condidat.save()

    return render(request, 'result.html', locals())


def list_approved(candids):
    for can in candids:
        if not can.approved:
            candids.remove(can)
    return candids


def test(date):
    date_courante = datetime.datetime.now().date()
    if date_courante > date:
        return False
    return True


def about(request):
    return render(request, 'about.html', locals())


def base(request):
    return render(request, 'base.html', {})