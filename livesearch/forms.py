from django.utils.translation import ugettext_lazy as _
from django import forms
from livesearch.models import AdvancedSearch


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

class AdvancedSearchForm(forms.ModelForm):
  class Meta:
    model = AdvancedSearch
    fields = ('count', 'market')
