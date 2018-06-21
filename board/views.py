from django.shortcuts import render, redirect, get_object_or_404
from board.models import Post, Comment
from board.forms import PostForm, SignupForm, CommentForm
from django.http import HttpResponse
from django.contrib.auth.models import User

from django.views.generic import TemplateView, ListView

from django.utils import timezone

from django.contrib.auth.decorators import login_required
# Create your views here.



# ListView로 게시물 리스트 구현
class index(ListView):
    model = Post
    paginate_by = 10
    def get_queryset(self):
        return Post.objects.order_by('-pk')

# 게시물 내용
def post_detail(request, pk):
    post_detail = get_object_or_404(Post, pk=pk)
    context = {
        'post_detail': post_detail,
    }
    return render(request, 'board/post_detail.html', context)


# 새 글 작성
@login_required
def new_post(request):
    if request.method =="POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.generate()
            return redirect('board:post_detail', pk=post.pk)
    else:
            form = PostForm()
    return render(request, 'board/form.html', {'form': form})

# 글 수정
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author == User.objects.get(username=request.user.get_username()):
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.regdate = timezone.now()
                post.generate()
                return redirect('board:post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'board/form.html', {'form': form})
    else:
        return render(request, 'board/warning.html')

# 글 삭제
@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author == User.objects.get(username = request.user.get_username()):
        post.delete()
        return redirect('board:index')
    else:
        return render(request, 'board/warning.html')


# 회원가입
def signup(request):
    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            signup_form.signup()
            return redirect('board:index')
    else:
        signup_form = SignupForm()

    return render(request, 'registration/signup.html', {'signup_form': signup_form,})

# TemplateView로 회원가입 완료 페이지 구현
class RegisteredView(TemplateView):
    template_name = 'registration/signup_done.html'


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('board:post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'board/add_comment_to_post.html', {'form': form})