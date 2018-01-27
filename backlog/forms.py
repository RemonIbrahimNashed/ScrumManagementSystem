from django import forms


class NewSprint(forms.Form):
    name = forms.CharField(label="Sprint name")
    dead_line = forms.DateField(widget=forms.TextInput(attrs=
                                {
                                    'id': 'datepicker'
                                }))
