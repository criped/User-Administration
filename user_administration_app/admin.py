from django.contrib import admin
from django import forms
from django.utils.html import format_html

from user_administration_app.constants import LABEL_IBAN, ERR_IBAN_TOO_LONG
from user_administration_app.models import BankAccount, MyUser


class UserForm(forms.ModelForm):
    """A form for creating and updating users. Includes all the fields on
    the user. Besides, updates or create a bank account for the user.
    """
    iban = forms.CharField(label=LABEL_IBAN, required=True,)

    class Meta:
        model = MyUser
        fields = ('firstname', 'lastname', 'iban',)

    def clean_iban(self):
        # Checks that the iban is shorter than 34
        iban = self.cleaned_data.get('iban')
        if len(iban) >= 34:
            raise forms.ValidationError(ERR_IBAN_TOO_LONG)
        return iban

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()

        BankAccount.objects.update_or_create(
            owner=user,
            defaults={'owner': user,
                      'iban': self.cleaned_data.get('iban')
                      }
        )

        return user

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        try:
            self.fields['iban'] = forms.CharField(label=LABEL_IBAN, required=True,
                                                  initial=self.instance.bankaccount_set.first().iban
                                                  )
        except AttributeError:
            self.fields['iban'] = forms.CharField(label=LABEL_IBAN, required=True)


class UserAdmin(admin.ModelAdmin):
    # The forms to add and change user instances
    form = UserForm

    list_display = ('fullname_link', 'bank_account',)
    list_display_links = None  # The field displaying the link is given by fullname_link()

    fieldsets = (
        ('Personal info', {'fields': ('firstname', 'lastname',)}),
        ('Bank Account info', {'fields': ('iban',)}),
    )

    search_fields = ('firstname', 'lastname', 'bank_account')
    ordering = ('firstname',)
    filter_horizontal = ()

    editable_objs = []

    def bank_account(self, instance):
        try:
            return instance.bankaccount_set.first().iban
        except BankAccount.DoesNotExist:
            return "-"

    def fullname_link(self, obj):
        if obj in self.editable_objs:
            return format_html("<a href='{id}'>{firstname} {lastname}</a>",
                               id=obj.id, firstname=obj.firstname,
                               lastname=obj.lastname
                               )
        else:
            return format_html("{firstname} {lastname}",
                               id=obj.id, firstname=obj.firstname,
                               lastname=obj.lastname
                               )

    def get_queryset(self, request):
        # Stores all the objects that the logged in User has created
        self.editable_objs = MyUser.objects.filter(creator=request.user)
        return super(UserAdmin, self).get_queryset(request)

    def save_model(self, request, obj, form, change):
        """It sets the user's creator to the logged user if the user is being created.
        This occurs when the change flag is False. To make sure, it also checks that the object does not have creator.
        """
        if not change and not obj.creator:
            obj.creator = request.user
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request, obj=None):
        return obj is None or request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return obj is None or obj.creator == request.user

    def has_delete_permission(self, request, obj=None):
        return obj is None or obj.creator == request.user


class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('iban', 'owner')


admin.site.register(BankAccount, BankAccountAdmin)
admin.site.register(MyUser, UserAdmin)

admin.site.disable_action('delete_selected')
admin.site.login_template = 'custom_login.html'
