from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import (UserRegisterForm,
                    UserUpdateForm,
                    ProfileUpdateForm)
from django.contrib.auth.decorators import login_required


from django.conf import settings
import os
from .models import Profile

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            cd = form.cleaned_data
            username = cd['username'] # or cd.get('username')
            messages.success(request, f'Your account has been created. You are now able to log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        # instance = what user and profile we want to update
        u_form = UserUpdateForm(request.POST,
                                instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES, # the image
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():

            # remove the old img
            # old_img_path = User.objects.filter()
            # old_img_path = request.user.profile.image.path
            # os.remove(os.path.join(settings.BASE_DIR, old_img_path))

            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')



            # Always redirect ... otherwise it will submit the form again (POST) if the user refreshes the page
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
