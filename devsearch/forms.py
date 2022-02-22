from django import forms


class SearchForm(forms.Form):
    keyword = forms.CharField(label='Enter a keyword (Required)', max_length=100, required=True,
                              widget=forms.TextInput(attrs={'class': "form-control",
                                                            'placeholder': "Eg. full-stack developer"}))
    location = forms.CharField(label='Enter a location', max_length=100, required=False,
                               widget=forms.TextInput(attrs={'class': "form-control",
                                                             'placeholder': "Eg. Turkey"}))
    language = forms.CharField(label='Enter a primary language', max_length=100, required=False,
                               widget=forms.TextInput(attrs={'class': "form-control",
                                                             'placeholder': "Eg. JavaScript"}))
    experience = forms.IntegerField(label='Years of experience:', max_value=20, required=False,
                               widget=forms.TextInput(attrs={'class': "form-control",
                                                             'placeholder': "Eg. 4"}))
