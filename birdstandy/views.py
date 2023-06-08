from django.contrib.auth import login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.views.generic import FormView
from .forms import *
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View


# główny widok witryny
class BirdView(View):
    def get(self, request):
        birds_list = Bird.objects.all()
        ctx = {
            "birds": birds_list
        }
        return render(request, "birdstandy/bird_view.html", ctx)


# lista wszystkich ptaków w bazie
class BirdsView(View):
    def get(self, request):
        birds_list = Bird.objects.all()
        ctx = {
            "birds": birds_list
        }
        return render(request, "birdstandy/birds_list.html", ctx)


# widok dodawania ptaka do bazy
class BirdAddView(View):
    def get(self, request):
        form = BirdForm()
        ctx = {
            'form': form
        }
        return render(request, 'birdstandy/bird_form.html', ctx)

    def post(self, request):
        form = BirdForm(request.POST)
        if form.is_valid():
            bird = Bird.objects.create(
                name=form.cleaned_data['name'],
                scientific_name=form.cleaned_data['scientific_name'],
                weight=form.cleaned_data['weight'],
                length=form.cleaned_data['length'],
                species=form.cleaned_data['species']
            )
            # return redirect(reverse('bird', args=[bird.pk]))
            birds_list = Bird.objects.all()
            ctx = {
                "birds": birds_list
            }
            return render(request, "birdstandy/birds_list.html", ctx)
        ctx = {
            'form': form
        }
        return render(request, 'birdstandy/bird_form.html', ctx)


# widok pojedynczego ptaka w bazie, szczegółowe informacje o ptaku
class BirdDetailView(View):
    def get(self, request, bird_id):
        bird = get_object_or_404(Bird, pk=bird_id)
        birdstands = BirdStand.objects.filter(bird_id=bird_id)
        try:
            birdphoto = BirdPhoto.objects.filter(name_id=bird_id)[0] # jeśli zdjęć ptaka w bazie jest więcej wybiera first
            ctx = {
                    'bird': bird,
                    'birdstands': birdstands,
                    'birdphoto': birdphoto
            }
            return render(request, 'birdstandy/bird.html', ctx)
        except IndexError:
            return HttpResponse(f'Dodaj zdjęcie ptaka "{bird}" do bazy!')


# usuwanie ptaka z bazy, możliwe tylko dla użytkownika zalogowanego
class DeleteBirdView(PermissionRequiredMixin, View):
    success_url = reverse_lazy('birds_list')
    template_name = 'birdstandy/reset_password.html'

    permission_required = 'auth.change_user'
    login_url = reverse_lazy('login')

    def get(self, request, bird_id):
        Bird.objects.filter(pk=bird_id).delete()
        birds_list = Bird.objects.all()
        ctx = {
            'birds_list': birds_list
        }
        return render(request, "birdstandy/birds_list.html", ctx)


# dodanie miejsca wystąpienia ptaka
class PlaceAddView(View):
    def get(self, request):
        form = PlaceForm()
        ctx = {
            'form': form
        }
        return render(request, 'birdstandy/place_form.html', ctx)

    def post(self, request):
        form = PlaceForm(request.POST)
        if form.is_valid():
            place = Place.objects.create(
                name=form.cleaned_data['name'],
                city=form.cleaned_data['city'],
                country=form.cleaned_data['country']
            )
            return redirect(reverse('place', args=[place.pk]))

        ctx = {
            'form': form
        }
        return render(request, 'birdstandy/place_form.html', ctx)


# wyświetlenie szczegółowego widoku miejsca
class PlaceDetailView(View):
    def get(self, request, place_id):
        place = get_object_or_404(Place, pk=place_id)
        ctx = {
            'place': place
        }
        return render(request, 'birdstandy/place.html', ctx)


# główny widok dodawania wystąpienia ptaka do bazy
# ptak, miejsce i obserwator jest pobierany z listy ptaków w bazie
class AddBirdStandView(View):
    def get(self, request):
        form = BirdStandForm()
        ctx = {
            'form': form
        }
        return render(request, 'birdstandy/add_birdstand.html', ctx)

    def post(self, request):
        form = BirdStandForm(request.POST)
        if form.is_valid():
            bird = form.cleaned_data['bird']
            place = form.cleaned_data['place']
            watcher = form.cleaned_data['watcher']
            BirdStand.objects.create(
                bird=bird,
                place=place,
                watcher=watcher
            )
            return redirect('birdstand', bird_id=bird.pk, place_id=place.pk)
        ctx = {
            'form': form
        }
        return render(request, 'birdstandy/add_birdstand.html', ctx)


# widok pojedynczego obserwatora ptaków
class WatcherView(View):
    def get(self, request, watcher_id):
        watcher = get_object_or_404(Watcher, pk=watcher_id)
        ctx = {
            'watcher': watcher,

        }
        return render(request, 'birdstandy/watcher.html', ctx)


# dodawanie obserwatora do bazy
class WatcherAddView(PermissionRequiredMixin, FormView):
    form_class = PasswordForm
    success_url = reverse_lazy('list_users')
    template_name = 'birdstandy/reset_password.html'

    permission_required = 'auth.change_user'
    login_url = reverse_lazy('login')

    def get(self, request):
        form = WatcherForm()
        ctx = {
            'form': form
        }
        return render(request, 'birdstandy/watcher_form.html', ctx)

    def post(self, request):
        form = WatcherForm(request.POST)
        if form.is_valid():
            watcher = Watcher.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            return redirect(reverse('watcher', args=[watcher.pk]))

        ctx = {
            'form': form
        }
        return render(request, 'birdstandy/watcher_form.html', ctx)


# widok wystąpienia ptaka
# wyświetla ptaka, obserwatora i miejsce wystąpienia
class BirdStandView(View):
    def get(self, request, bird_id, place_id):
        bird = get_object_or_404(Bird, pk=bird_id)
        place = get_object_or_404(Place, pk=place_id)
        birdstands = BirdStand.objects.filter(place_id=place_id, bird_id=bird_id)

        ctx = {
            "bird": bird,
            "place": place,
            "birdstands": birdstands
        }
        return render(request, "birdstandy/birdstand.html", ctx)


# widok użytkownika pojedynczego w bazie
class UsersView(View):
    def get(self, request):
        users = User.objects.order_by('username')
        ctx = {
            'users': users
        }
        return render(request, 'birdstandy/users.html', ctx)


# widok logowania użytkownika
class LoginView(FormView):
    form_class = LoginForm
    success_url = reverse_lazy('index')
    template_name = 'birdstandy/login.html'

    def form_valid(self, form):
        login(self.request, form.cleaned_data['user'])
        return super().form_valid(form)


# widok wylogowania użytkownika
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


# widok dodawania użytkownika do bazy
class CreateUserView(FormView):
    form_class = UserForm
    success_url = reverse_lazy('list_users')
    template_name = 'birdstandy/user_form.html'

    def form_valid(self, form):
        User.objects.create_user(
            username=form.cleaned_data['user_name'],
            password=form.cleaned_data['password'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            email=form.cleaned_data['email']
        )
        return super().form_valid(form)


# widok zmiany hasła użytkownika, dostępny tylko dla zalogowanych użytkowników
class ResetPasswordView(PermissionRequiredMixin, FormView):
    form_class = PasswordForm
    success_url = reverse_lazy('list_users')
    template_name = 'birdstandy/reset_password.html'

    permission_required = 'auth.change_user'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        u = User.objects.get(pk=1)
        u.set_password(form.cleaned_data['password'])
        u.save()
        return super().form_valid(form)


# dodawanie zdjęcia ptaka do bazy
class AddBirdPhotoView(View):
    def get(self, request):
        form = BirdPhotoForm()
        ctx = {
            'form': form
        }
        return render(request, 'birdstandy/addbirdphoto_form.html', ctx)

    def post(self, request):
        form = BirdPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            birdphoto = BirdPhoto.objects.create(
                image=form.cleaned_data['image'],
                name=form.cleaned_data['name'],
            )
            birdphoto.save()
            return redirect(reverse('bird_photo', args=[birdphoto.pk]))

        ctx = {
            'form': form
        }
        return render(request, 'birdstandy/addbirdphoto_form.html', ctx)


# widok ptaka z dodanym do bazy zdjęciem
class BirdPhotoView(View):
    def get(self, request, photo_id):
        birdphoto = get_object_or_404(BirdPhoto, pk=photo_id)
        ctx = {
            'birdphoto': birdphoto
        }
        return render(request, 'birdstandy/bird_photo.html', ctx)
