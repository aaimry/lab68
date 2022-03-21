from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import ArticleForm, ArticleDeleteForm
from webapp.models import Article, ArticleLike
from webapp.views.base import SearchView


class IndexView(SearchView):
    model = Article
    context_object_name = "articles"
    template_name = "articles/index.html"
    paginate_by = 3
    paginate_orphans = 0
    search_fields = ["title__icontains", "author__icontains"]
    ordering = ["-updated_at"]


class ArticleCreateView(PermissionRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "articles/create.html"
    permission_required = "webapp.add_article"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleView(DetailView):
    template_name = 'articles/view.html'
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = self.object.comments.order_by("-created_at")
        context['comments'] = comments
        return context


class ArticleUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "webapp.change_article"
    form_class = ArticleForm
    template_name = "articles/update.html"
    model = Article

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author


class ArticleDeleteView(PermissionRequiredMixin, DeleteView):
    model = Article
    template_name = "articles/delete.html"
    success_url = reverse_lazy('webapp:index')
    form_class = ArticleDeleteForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == "POST":
            kwargs['instance'] = self.object
        return kwargs


class ArticleLikeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        article = get_object_or_404(Article, id=kwargs.get('pk'))
        user_likes = user.article_likes.all()
        if user_likes.filter(article=article).count() > 0:
            return HttpResponseForbidden('Вы уже постаивли лайк :)')
        else:
            ArticleLike.objects.create(user=user, article=article).save()
        return JsonResponse({"likes": article.likes.count(), 'id': article.pk})


class ArticleUnlikeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        article = get_object_or_404(Article, id=kwargs.get('pk'))
        user_likes = user.article_likes.all()
        if user_likes.filter(article=article).count() > 0:
            ArticleLike.objects.get(user=user, article=article).delete()
        else:
            return HttpResponseForbidden('Кажется, вашего лайка тут и не было :(')
        return JsonResponse({"likes": article.likes.count(), 'id': article.pk})

