from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.models import User
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        UserPassesTestMixin)



def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    # it is looking for a template in blog/post_list.html
    #                              # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    # ordering = ['-date_posted'] we overwrite this with get_queryset
    paginate_by = 5

    def get_queryset(self):
        # looks in the url for a parameter 'username'
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    # it is looking for a template in blog/post_detail.html
    #                              # <app>/<model>_<viewtype>.html
    # If I don't add context_object_name then
    #   in the template I will call the 'post' ---> object
    #           !!!!


# if you go to the ...post/new url it will still let you make the post unless you inherit from LoginRequiredMixin
# It's the same as using @login_required decorator on a function
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    # it is looking for a template in blog/post_form.html .. same for UpdateView

    # overwrite the form_valid method to add the author
    # before the form is submitted
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    # success_url = '' to redirect to a certain template after the form was submitted successfully
    # or make the get_absolute_url function inside the model



# add UserPassesTestMixin to let the users edit only their OWN posts
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    # it is looking for a template in blog/post_form.html ... same for CreateView

    # overwrite the form_valid method to add the author
    # before the form is submitted
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    # success_url = '' to redirect to a certain template after the form was submitted successfully
    # or make the get_absolute_url function inside the model

    # UserPassesTestMixin will run this function to see if our user passes a certain test condition
    # get_object is a method of PostUpdateView
    def test_func(self):
        post = self.get_object()
        # if the current user == the author of the post to update
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    # it is looking for a template in blog/ called post_confirm_delete.html
    success_url = '/' # send then to the homepage after deletion

    def test_func(self):
        post = self.get_object()
        # if the current user == the author of the post to update
        if self.request.user == post.author:
            return True
        return False

    # If I don't add context_object_name then
    #   in the template I will call the 'post' ---> object
    #  just like in the DetailView



def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


# CUSTOM ERRORS
def handler404(request, exception=None):
    return render(request, 'blog/404.html', status=404)
def handler500(request, exception=None):
    return render(request, 'blog/500.html', status=500)
