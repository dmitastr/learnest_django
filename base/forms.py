import logging

from django.contrib.auth.models import AbstractUser
from django.forms import ModelForm
from django.core.exceptions import ObjectDoesNotExist
from base.models import Package, Purchase, Student


logger = logging.getLogger("base")


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = "__all__"


class PackageForm(ModelForm):
    class Meta:
        model = Package
        exclude = ['teacher', ]

    def save(self, commit: bool = True, *args, **kwargs):
        instance = super(PackageForm, self).save(commit=False)
        try:
            if not instance.teacher:
                request = kwargs.pop("request", None)
                if request and request.user.is_authenticated:
                    self.instance = request.user

        except ObjectDoesNotExist:
            request = kwargs.pop("request", None)
            logger.debug(request or "No request found")
            if request and request.user.is_authenticated:
                self.instance.teacher = request.user

        if commit:
            instance.save()
        return instance


class PurchaseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.teacher = kwargs.pop('teacher', None)
        super(PurchaseForm, self).__init__(
            *args, **kwargs)
        if self.teacher:
            self.fields['package'].queryset = Package.objects.filter(
                teacher=self.teacher)

    class Meta:
        model = Purchase
        fields = "__all__"
