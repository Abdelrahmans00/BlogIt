from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView
from .models import Article
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .form import ArticleForm
from django.views.generic.edit import UpdateView


class Index(ListView):
    model = Article
    queryset = Article.objects.all().order_by('-date')
    template_name = 'blog/index.html'
    paginate_by = 1


class Featured(ListView):
    model = Article
    queryset = Article.objects.filter(featured=True).order_by('-date')
    template_name = 'blog/featured.html'
    paginate_by = 1


class DetailArticleView(DetailView):
    model = Article
    template_name = 'blog/blog_post.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        article = self.get_object()
        context['liked_by_user'] = self.request.user.is_authenticated and article.likes.filter(pk=self.request.user.id).exists()
        return context


class LikeArticle(View):
    def post(self, request, pk):
        article = get_object_or_404(Article, id=pk)
        if article.likes.filter(pk=request.user.id).exists():
            article.likes.remove(request.user)
        else:
            article.likes.add(request.user)
        return redirect('detail_article', pk=pk)


class DeleteArticleView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'blog/blog_delete.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author


@login_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('index')
    else:
        form = ArticleForm()
    return render(request, 'blog/create_article.html', {'form': form})

class UpdateArticleView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/edit_article.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author
