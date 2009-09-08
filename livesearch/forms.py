from django.utils.translation import ugettext_lazy as _
from django import forms
from models import AdminSearchOption

formatChoices = (('html', 'html format'),
                 ('json', 'json format'),
                 ('both', 'both html&json'),)
class SearchForm(forms.Form):
    """
    """
    key_words =  forms.CharField(label=_("Search by Google"),)
    format = forms.ChoiceField(label=_("Please select the response fomat"),
                               choices = formatChoices)
    def get_keywords(self):
        return self.cleaned_data['key_words']

    def get_format(self):
        return self.cleaned_data['format']

class SearchesForm(forms.Form):
    """
    """
    key_words =  forms.CharField(label=_("Search by Google&Bing"),)


    def get_keywords(self):
        return self.cleaned_data['key_words']



search_option_choices=(
                ('DisableLocationDetection', 'DisableLocationDetection'),
                ('EnableHighlighting', 'EnableHighlighting'),
            )

adult_option_choices=(('Off', 'Off'), ('Moderate', 'Moderate'), ('Strict', 'Strict'), ('None', 'None'))

web_search_choices=(
                        ('DisableHostCollapsing', 'DisableHostCollapsing'),
                        ('DisableQueryAlterations', 'DisableQueryAlterations'),
                    )

video_search_choices=(
                            ('Date', 'Date'),
                            ('Relevance', 'Relevance'),
                      )

class AdminOptions(forms.ModelForm):
    """
    the options that admin can use to define a search
    """
    class Meta:
        model = AdminSearchOption
        exclude = ('muaccount')

    def __init__(self, *args, **kwargs):
        super(AdminOptions, self).__init__(*args, **kwargs)
        self.fields['search_option'].widget = forms.RadioSelect(choices = self.fields['search_option'].choices)
        self.fields['adult_option'].widget = forms.RadioSelect(choices = AdminOptions.base_fields['adult_option'].choices)
        self.fields['web_search'].widget = forms.RadioSelect(choices = AdminOptions.base_fields['web_search'].choices)
        self.fields['video_search'].widget = forms.RadioSelect(choices = AdminOptions.base_fields['video_search'].choices)


    def clean_search_option(self):
        so = self.cleaned_data.get('search_option', None)
        if not so:
            return 'None'
        return so

    def clean_web_search(self):
        ws = self.cleaned_data.get('web_search', None)
        if not ws:
            return 'None'
        return ws



