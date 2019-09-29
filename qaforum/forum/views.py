from django.shortcuts import render, redirect, HttpResponse, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django import template
from django.template.loader import get_template
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


def index(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'forum/index.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'forum/index.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'forum/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



class DraftListView(LoginRequiredMixin, ListView):
    template_name = 'forum/post_draft_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.order_by('created_date')


def about(request):
    return render(request, 'forum/about.html', {'title': 'About'})


# redirect success page
def Success(request):
    return render(request, 'forum/success.html')


# sign up form
def SignUp(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('success')
    else:
        form = UserRegisterForm()
    return render(request, "registration/signup.html", {'form': form})


# Contact form view

def Contact(request):
    Contact_Form = ContactForm
    if request.method == 'POST':
        form = Contact_Form(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get('contact_name')
            contact_email = request.POST.get('contact_email')
            contact_content = request.POST.get('content')

            template = get_template('forum/contact_form.txt')
            context = {
                'contact_name' : contact_name,
                'contact_email' : contact_email,
                'contact_content' : contact_content,
            }

            content = template.render(context)

            email = EmailMessage(
                "New contact form email",
                content,
                "Amit Kushwaha" + '',
                ['amitkushwaha1097@gmail.com'],
                headers = { 'Reply To': contact_email }
            )

            email.send()

            return redirect('success')
    return render(request, 'forum/contact.html', {'form':Contact_Form })


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'forum/comment_form.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post-detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post-detail', pk=post_pk)
