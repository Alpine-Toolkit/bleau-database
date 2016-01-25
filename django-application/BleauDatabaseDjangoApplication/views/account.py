####################################################################################################
#
# Bleau Database - A database of the bouldering area of Fontainebleau
# Copyright (C) Salvaire Fabrice 2016
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

from django.contrib import messages
from django.contrib.auth import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import translation
from django.utils.translation import ugettext as _

####################################################################################################

from ..models import Profile

####################################################################################################

class AuthenticationForm(forms.AuthenticationForm):

    """Override the default AuthenticationForm in order to add HTML5 attributes.  This is the only
    change done and needed

    """

    ##############################################

    def __init__(self, *args, **kwargs):

        super(AuthenticationForm, self).__init__(*args, **kwargs)

        # Add HTML5 attributes
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = _('Password')
        self.fields['username'].widget.attrs['autofocus'] = 'autofocus'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = _('Username')

####################################################################################################

class PasswordChangeForm(forms.PasswordChangeForm):

    """Override the default PasswordChangeForm in order to add HTML5 attributes.  This is the only
    change done and needed

    """

    def __init__(self, *args, **kwargs):

        super(PasswordChangeForm, self).__init__(*args, **kwargs)

        # Add HTML5 attributes
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = _('New password')
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = _('New password')
        self.fields['old_password'].widget.attrs['autofocus'] = 'autofocus'
        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['old_password'].widget.attrs['placeholder'] = _('Old password')

####################################################################################################

class PasswordResetForm(forms.PasswordResetForm):

    """Override the default PasswordResetForm in order to add HTML5 attributes.  This is the only
    change done and needed

    """

    ##############################################

    def __init__(self, *args, **kwargs):

        super(PasswordResetForm, self).__init__(*args, **kwargs)

        # Add HTML5 attributes
        self.fields['email'].widget.attrs['autofocus'] = 'autofocus'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = _('email')

####################################################################################################

class SetPasswordForm(forms.SetPasswordForm):

    """Override the default SetPasswordForm in order to add HTML5 attributes.  This is the only change
    done and needed

    """

    ##############################################

    def __init__(self, *args, **kwargs):

        super(SetPasswordForm, self).__init__(*args, **kwargs)

        # Add HTML5 attributes
        self.fields['new_password1'].widget.attrs['autofocus'] = 'autofocus'
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = _('New password')
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = _('New password')

####################################################################################################

class UserCreationForm(forms.UserCreationForm):

    """Override the default UserCreationForm in order to add HTML5 attributes.

    """

    ##############################################

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')

    ##############################################

    def __init__(self, *args, **kwargs):

        super(UserCreationForm, self).__init__(*args, **kwargs)

        # email, first_name and last_name are required
        self.fields['email'].required = True
        self.fields['first_name'].required = True

        # Add HTML5 attributes
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = _('Password')
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = _('Password')
        self.fields['username'].widget.attrs['autofocus'] = 'autofocus'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = _('Username')

    ##############################################

    def save(self, commit=True):

        """Create the new User and the associated Profile The User is not activated until the
        register_confirm url has been visited

        """

        if not commit:
            raise NotImplementedError('Cannot create Profile and User without commit')
        user = super(UserCreationForm, self).save(commit=False)
        user.is_active = False
        user.save()
        profile = Profile(user=user)
        profile.save()
        return user

####################################################################################################

class UserUpdateForm(ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name')

    ##############################################

    def __init__(self, *args, **kwargs):

        super(UserUpdateForm, self).__init__(*args, **kwargs)

        # first_name and last_name are required
        self.fields['first_name'].required = True

        self.fields['first_name'].widget.attrs['autofocus'] = 'autofocus'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'

####################################################################################################

class ProfileUpdateForm(ModelForm):

    class Meta:
        model = Profile
        fields = ('language',)

    ##############################################

    def __init__(self, *args, **kwargs):

        super(ProfileUpdateForm, self).__init__(*args, **kwargs)

        self.fields['language'].required = True
        self.fields['language'].widget.attrs['class'] = 'form-control'

####################################################################################################

@login_required
def profile(request):

    # Force the user to provide language
    if not request.user.profile.language:
        messages.error(request, _("You should update your language."))
        return HttpResponseRedirect(reverse('accounts.profile.update'))

    return render(request, 'account/profile.html')

####################################################################################################

@login_required
def update(request):

    profile = get_object_or_404(Profile, user__pk=request.user.pk)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save()
            # Update the language code and activate it for the message
            if profile.language:
                request.session['django_language'] = profile.language
                translation.activate(profile.language)
            messages.success(request, _("Personnal information updated"))
            return HttpResponseRedirect(reverse('accounts.profile'))
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

        return render(request, 'account/update.html',
                      {'user_form': user_form, 'profile_form': profile_form})

####################################################################################################

@login_required
def password_change_done(request):

    messages.success(request, _('Password changed successfully'))
    return HttpResponseRedirect(reverse('accounts.profile'))

####################################################################################################

def password_reset_done(request):

    return render(request, 'account/password_reset_done.html')

####################################################################################################

@login_required
def delete(request):

    request.user.delete()
    return HttpResponseRedirect(reverse('index'))

####################################################################################################
#
# End
#
####################################################################################################
