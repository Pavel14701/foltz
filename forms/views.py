from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from .forms import ContactForm
from common.dto import FormData
from common.aplications import SendAplications


def contact_view(request: HttpRequest) -> HttpResponseRedirect | HttpResponse:
    """Страница контактов: форма заявки + отправка на email и в Telegram."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form_data = FormData(
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                question=form.cleaned_data['question'],
            )
            sendler = SendAplications(form_data)
            sendler.email()
            sendler.tg()
            return redirect('forms:success')
    else:
        form = ContactForm()
    return render(request, 'forms/contact.html', {'form': form})


