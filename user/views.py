from django.shortcuts import render, redirect
from user.forms import UserAdminCreationForm
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.views import View
from django.urls import reverse_lazy


def register(req):
    form = UserAdminCreationForm()
    if req.method == 'POST':
        form = UserAdminCreationForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(req, 'register.html', {'form': form})


class RegisterView(CreateView):
    template_name = 'register.html'
    success_url = reverse_lazy('register')
    form_class = UserAdminCreationForm
    def post(self, request, *args, **kwargs):
        form = UserAdminCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            ip = request.META.get('REMOTE_ADDR')
            user.location = ip
            user.save()
        return render(request, self.template_name, {'form': form})

