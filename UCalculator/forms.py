from django import forms
from .models import Material, Component, Composite

class NewComponentForm(forms.ModelForm):
    add_material = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = Component
        fields = ['material', 'thickness']

class ClearForm(forms.Form):
    clear_material_view = forms.BooleanField(widget=forms.HiddenInput, initial=True)

class SaveForm(forms.ModelForm):
    save_composite = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = Composite
        fields = ['name']

class LoadForm(forms.ModelForm):
    load_composite = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = Component
        fields = ['composite']

class InsulatorForm(forms.Form):
    calculate_insulation = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    target_u = forms.FloatField()

class DeleteForm(forms.Form):
    delete_composite = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    to_delete = forms.CharField(widget=forms.HiddenInput)