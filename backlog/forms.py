from django import forms


class NewSprint(forms.Form):
    name = forms.CharField(label="Sprint name")
    dead_line = forms.DateField(widget=forms.TextInput(attrs=
    {
        'id': 'datepicker'
    }))


class NewBackLog(forms.Form):
    name = forms.CharField(label="BackLog name")
    dead_line = forms.DateField(widget=forms.TextInput(attrs=
    {
        'id': 'datepicker'
    }))


class NewTask(forms.Form):
    name = forms.CharField(label="task name")
    dead_line = forms.DateField(widget=forms.TextInput(attrs=
    {
        'id': 'datepicker'
    }))
    description = forms.CharField(label="task description", max_length=500)
    importance = forms.IntegerField(max_value=10, min_value=1)
