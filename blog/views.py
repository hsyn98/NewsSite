from django.shortcuts import render, redirect
import requests
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth import login
from django.views.generic import DetailView
from random import shuffle

from .tokens import account_activation_token
from .models import Post, MyUser
from .admin import UserCreationForm, UserChangeForm
import base64
from django.core.mail import send_mail


def home(request):
    context = {}
    if request.user.is_authenticated:
        interests = request.user.interest.__str__().split(',')
        post_list = []
        for interest in interests:
            interest = interest.lower()
            interest = interest.strip()
            post_list.extend(list(Post.objects.filter(category=interest)))
            context['recommended'] = post_list[:3]
            context['recommended'].extend(post_list[-3:])
    result = (list(Post.objects.all()))
    shuffle(result)
    context['post'] = result[:10]
    context['post'].extend(result[-5:])
    return render(request, 'blog/index.html', context)


def about(request):
    return render(request, 'blog/about.html')


def contact(request):
    return render(request, 'blog/contact.html')


def category(request, cat):
    posts = Post.objects.filter(category=cat)
    request.user.is_authenticated
    return render(request, 'blog/category.html', {'first_post': posts[:3], 'posts': posts[3:7], 'cat': cat})


class PostDetailView(DetailView):
    model = Post


def update(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog-home')

    else:
        form = UserChangeForm(instance=request.user)

    return render(request, 'blog/update_user.html', {'form': form})


def register(request):
    if request.user.is_authenticated:
        return redirect('blog-home')
    if request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('blog/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return redirect('blog-home')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})


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
        # return redirect('home')
        return redirect('update_profile')
    else:
        return render(request, 'blog/index.html')


def refresh(request):
    if not request.user.is_staff:
        return redirect('blog-home')
    if request.GET.__len__() == 0:
        r = requests.get("https://newsapi.org/v2/sources?country=us&apiKey=76fe0c04253f44a4ae99a42cde23204e")
        j = r.json()
        return render(request, 'blog/refresh.html', {'source': j['sources']})
    else:
        r = request.GET
        source = r['sources']
        language = r['language']
        q = r['q']
        url = "https://newsapi.org/v2/everything?q="
        url += q
        url += "&sources="
        url += source
        url += "&language="
        url += language
        url += "&pageSize=100&apiKey=76fe0c04253f44a4ae99a42cde23204e"
        api(url, q)
        return redirect('blog-refresh')


def api(url, q):
    r = requests.get(url=url)
    j = r.json()
    all_posts = Post.objects.all()
    for x in j['articles']:
        flag = False
        for ap in all_posts:
            if x['title'] == ap.title or x['description'] is None \
                    or x['urlToImage'] is None or x['urlToImage'] == 'null':
                flag = True
                break
        if flag:
            continue
        else:
            post = Post()
            post.title = x['title']
            post.author = x['author']
            post.content = x['content']
            post.description = x['description']
            post.image_url = x['urlToImage']
            post.publish_date = x['publishedAt']
            post.url = x['url']
            post.category = q
            post.save()
    #Post.objects.all().delete()
    return
