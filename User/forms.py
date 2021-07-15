from django.contrib.auth import forms as auth_forms
from django import forms
from django.contrib.auth.middleware import AuthenticationMiddleware
from User.middleware import AuthRequiredMiddleware
from User.models import *


class UserLoginForm(auth_forms.AuthenticationForm):
    def _init_(self, *args, **kwargs):
        super(UserLoginForm, self)._init_(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control h-auto py-7 px-6 rounded-lg',
            'placeholder': 'Username',
            'id': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control h-auto py-7 px-6 rounded-lg',
            'placeholder': 'Password',
            'id': 'password',
        }
    ))

    def confirm_login_allowed(self, user):
        if not user.is_superuser:
            raise forms.ValidationError(("Icazen yoxdu bla"),
                                        code='inactive',
                                        )


class SchemaForm(forms.ModelForm):
    # Schema Title
    schemaTitle = forms.CharField(label='Schema Name', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id':'schemaTile'
        }
    ))
    # Separator form
    separator = forms.ModelChoiceField(queryset=Separator.objects.filter(status=1), label='Separator', widget=forms.Select(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'separator'
        }
    ))
    # String Character form
    stringCharacter = forms.ModelChoiceField(queryset=StringCharacter.objects.filter(status=1),widget=forms.Select(
        attrs={
            'class': 'form-control ',
            'placeholder': '',
            'id': 'schemaTile'
        }
    ))

    class Meta:
        model = Schema
        fields = ['schemaTitle', 'separator', 'stringCharacter', 'schemaColumns']


class SchemaColumnsForm(forms.ModelForm):
    columnName = forms.CharField(label='Column name', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'columnName'
        }
    ))

    type = forms.ModelChoiceField(queryset=InputType.objects.filter(status=1), label='Type',
                                       widget=forms.Select(
                                           attrs={
                                               'class': 'form-control types',
                                               'placeholder': '',
                                               'id': 'type'
                                           }
                                       ))

    from_int = forms.IntegerField(label='From', required=False, widget=forms.NumberInput(
        attrs={
            'class': 'form-control changable',
            'placeholder': '',
            'id': 'from_int'
        }
    ))

    to_int = forms.IntegerField(label='To', required=False, widget=forms.NumberInput(
        attrs={
            'class': 'form-control changable',
            'placeholder': '',
            'id': 'to_int'
        }
    ))

    sentence = forms.IntegerField(label='Sentence', required=False, widget=forms.NumberInput(
        attrs={
            'class': 'form-control changable',
            'placeholder': '',
            'id': 'sentence'
        }
    ))

    order = forms.CharField(label='Order', widget=forms.NumberInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'order'
        }
    ))

    class Meta:
        model = SchemaColumn
        fields = ['columnName', 'type', 'from_int', 'to_int', 'sentence', 'order']


class Generated_csvForm(forms.ModelForm):

    class Meta:
        model = Generated_csv
        fields = '__all__'