from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from site_forms.custom_form import ContactForm
from common.dto import FormData
from common.aplications import SendAplications


def contact_view(request:HttpRequest) -> HttpResponseRedirect|HttpResponse:
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form_data = FormData(
                name = form.cleaned_data['name'],
                phone = form.cleaned_data['phone'],
                question = form.cleaned_data['question']
            )
            sendler = SendAplications(form_data)
            sendler.email()
            sendler.tg()
            return redirect('success')
    else:
        form = ContactForm()
    return render(request, 'forms/contact.html', {'form': form})


