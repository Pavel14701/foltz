from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_POST
from .forms import ContactForm
from common.dto import FormData
from common.aplications import SendAplications

def contact_view(request: HttpRequest) -> HttpResponse:
    """Страница «Контакты»: способы связи + форма на консультацию.
    Контактные данные берёт контекст-процессор site_contacts."""
    return render(request, 'forms/contact.html')


def _send(form: ContactForm) -> None:
    """Отправка заявки на email и в Telegram."""
    form_data = FormData(
        name=form.cleaned_data['name'],
        phone=form.cleaned_data['phone'],
        question=form.cleaned_data['question'],
    )
    sendler = SendAplications(form_data)
    sendler.email()
    sendler.tg()


@require_POST
def send_request(request: HttpRequest) -> HttpResponse:
    """Единая точка приёма заявок со страниц товаров и услуг."""
    form = ContactForm(request.POST)
    if form.is_valid():
        _send(form)
        return redirect('forms:success')
    # Некорректные данные (например, телефон): показываем форму с ошибками.
    return render(request, 'forms/request.html', {'form': form}, status=400)


