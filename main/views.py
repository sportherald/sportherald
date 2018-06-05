from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, UpdateView
from .models import Post, Sport
from .forms import PostForm
from django.http import JsonResponse, HttpResponseRedirect, Http404
import pdb
from django.conf import settings
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
# Create your views here.

class ViewMixin:
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'

    def get_context_data(self, *args, **kwargs):
        context = super(ViewMixin, self).get_context_data(*args, **kwargs)
        context['sports'] = Sport.objects.all()
        return context

    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            offset = int(request.POST.get('offset'))
            sport_id = (request.POST.get('sport_id'))
            new_offset = offset + settings.PAGE_LENGTH
            if sport_id == '*':
                posts = self.main_queryset
            else:
                posts = self.main_queryset.filter(sport_id=sport_id)[offset:new_offset]
                #pdb.set_trace()
            response = render_to_string('includes/post_list.html', {'posts': posts})
            return JsonResponse({'data': response, 'offset': new_offset})
        else:
            return Http404('Invalid Access')


@method_decorator(csrf_exempt, name='dispatch')
class homeView(ViewMixin, ListView):
    main_queryset=Post.objects.filter(status='approved').order_by('-approved_date')
    queryset =main_queryset[:settings.PAGE_LENGTH]


@method_decorator(csrf_exempt, name='dispatch')
class BlogView(LoginRequiredMixin, ViewMixin, ListView):

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-approved_date')[:settings.PAGE_LENGTH]

    def post(self, request, *args, **kwargs):
        self.main_queryset=Post.objects.filter(author=self.request.user).order_by('-approved_date')
        return  super(BlogView, self).post(request, *args, **kwargs)







@method_decorator(csrf_exempt, name='dispatch')
class reviewView(ViewMixin,ListView):
    main_queryset=Post.objects.filter(status='submitted').order_by('-created_date')
    queryset = main_queryset[:settings.PAGE_LENGTH]

    def get_context_data(self, *args, **kwargs):
        context=super(reviewView, self).get_context_data(*args, **kwargs)
        context['page']='review'
        return context


class CreatePost(CreateView):
    model=Post
    form_class=PostForm

    def form_valid(self, form):
        post=form.save(commit=False)
        post.author=self.request.user
        post.status='submitted'
        post.save()
        form.save_m2m()
        messages.success(self.request, 'Post Submitted and under review')
        return HttpResponseRedirect('/')



    def form_invalid(self,form):
        pdb.set_trace()

@method_decorator(csrf_exempt, name='dispatch')
class PostStatus(View):
    def post(self, request,*args, **kwargs):
        id = request.POST.get('id')
        status=request.POST.get('status')
        try:
            post=Post.objects.get(id=id)
            post.status=status
            post.approved_date= timezone.now()
            post.save()
            posts=Post.objects.filter(status='submitted')[:settings.PAGE_LENGTH]
            response=render_to_string('includes/post_list.html', {'posts':posts})
            return  JsonResponse({'status':200, 'message':'Successfully Updated',
                                  'data':response})
        except Post.DoesNotExist:
            return JsonResponse({'status':404, 'message':'Post not found'})





