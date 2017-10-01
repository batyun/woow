from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from apple.forms import TalkForm, SignupForm
from apple.models import MyUser, SimpleTalk
from apple.tokens import account_activation_token


def home(request):
    talks = SimpleTalk.objects.filter().order_by('-created_date')
    talk_form = TalkForm()
    form = SignupForm()

    if request.method == 'POST':
            print('post_talk')
            talk_form = TalkForm(request.POST)
            if talk_form.is_valid():
                talk = talk_form.save(commit=False)
                talk.author = request.user
                talk.save()
    else:
        print('else')

    return render(request, 'home.html', {'form': form, 'talk_form': talk_form, 'talks': talks})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return HttpResponse('Activation link is invalid!')


def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request, 'registration/acc_active_page.html', {'email': to_email})

    return render(request, 'home.html', {'form': form})

#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
#                                                                   #
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #

#####################################################################


def talk_remove(request, pk):
    talk = get_object_or_404(SimpleTalk, pk=pk)
    talk.delete()
    return redirect('home')