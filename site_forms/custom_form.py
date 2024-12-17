from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=100, required=True)
    phone = forms.CharField(label='Номер телефона', max_length=15, required=True)
    question = forms.CharField(label='Вопрос', widget=forms.Textarea, required=False)