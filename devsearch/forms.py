from django import forms


class SearchForm(forms.Form):
    keyword = forms.CharField(label='Enter a keyword', max_length=100, required=True,
                              widget=forms.TextInput(attrs={'class': "form-control",
                                                            'placeholder': "Eg. full-stack developer"}))
