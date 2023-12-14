from django import forms
from datetime import date

from catalog.models import Gun


# форма для добавления в БД новых авторов
class Form_add_author(forms.Form):
 title = forms.CharField(label="Название экспоната")
 summary = forms.CharField(label="Описане", widget=forms.Textarea)
 photo = forms.ImageField(label="Фото автора")


class Form_edit_author(forms.ModelForm):
 class Meta:
  model = Gun
  fields = '__all__'
