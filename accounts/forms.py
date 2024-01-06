from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django import forms

from .constants import ACCOUNT_TYPES, GENDER_TYPES
from .models import UserBankAccount_Model, UserAddress_Model

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class UserRegistration_Form(UserCreationForm):
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPES)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPES)
    street = forms.CharField(max_length=50)
    house = forms.CharField(max_length=10)
    postal_code = forms.CharField(max_length=10)
    city = forms.CharField(max_length=20)
    state = forms.CharField(max_length=20)
    country = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'birth_date',
            'gender',
            'street',
            'house',
            'postal_code',
            'city',
            'state',
            'country',
            'account_type',
            'email',
            'username',
            'password1',
            'password2',
        ]

    def save(self, commit=True):
        new_user = super().save(commit=False)                       # Not saving data into database, right at this moment.
        if commit:
            new_user.save()                                         # Saving data in User model.
            birth_date = self.cleaned_data.get('birth_date')
            gender = self.cleaned_data.get('gender')
            street = self.cleaned_data.get('street')
            house = self.cleaned_data.get('house')
            postal_code = self.cleaned_data.get('postal_code')
            city = self.cleaned_data.get('city')
            state = self.cleaned_data.get('state')
            country = self.cleaned_data.get('country')
            account_type = self.cleaned_data.get('account_type')

            UserAddress_Model.objects.create(                       # Saving data in UserAddress_Model.
                user=new_user,
                street=street,
                house=house,
                postal_code=postal_code,
                city=city,
                state=state,
                country=country
            )

            UserBankAccount_Model.objects.create(                   # Saving data in UserBankAccount_Model.
                user=new_user,
                account_type=account_type,
                account_number=1000000000+new_user.id,
                birth_date=birth_date,
                gender=gender
            )
        return new_user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            # print(field)
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class UserProfileUpdate_Form(forms.ModelForm):
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPES)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPES)
    street = forms.CharField(max_length=50)
    house = forms.CharField(max_length=10)
    postal_code = forms.CharField(max_length=10)
    city = forms.CharField(max_length=20)
    state = forms.CharField(max_length=20)
    country = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'street',
            'house',
            'postal_code',
            'city',
            'state',
            'country',
            'email',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })

        if self.instance:
            try:
                user_account = self.instance.user_account
                user_address = self.instance.user_address
            except UserBankAccount_Model.DoesNotExist:
                user_account = None
                user_address = None

            if user_account:
                # self.fields['account_type'].initial = user_account.account_type
                self.fields['birth_date'].initial = user_account.birth_date
                self.fields['gender'].initial = user_account.gender

                self.fields['street'].initial = user_address.street
                self.fields['house'].initial = user_address.house
                self.fields['postal_code'].initial = user_address.postal_code
                self.fields['city'].initial = user_address.city
                self.fields['state'].initial = user_address.state
                self.fields['country'].initial = user_address.country

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user_account, created = UserBankAccount_Model.objects.get_or_create(user=user)
            user_address, created = UserAddress_Model.objects.get_or_create(user=user)

            # user_account.account_type = self.cleaned_data['account_type']
            user_account.birth_date = self.cleaned_data['birth_date']
            user_account.gender = self.cleaned_data['gender']
            user_account.save()

            user_address.street = self.cleaned_data['street']
            user_address.house = self.cleaned_data['house']
            user_address.postal_code = self.cleaned_data['postal_code']
            user_address.city = self.cleaned_data['city']
            user_address.state = self.cleaned_data['state']
            user_address.country = self.cleaned_data['country']
            user_address.save()

        return user

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class UserPasswordUpdate_Form(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
