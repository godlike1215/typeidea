from django.shortcuts import render
from .models import Post, Category, Tag
from config.models import SideBar
from django.views.generic import ListView, DetailView

# Create your views here.


# def post_list(request, category_id=None, tag_id=None):
# 	category = None
# 	tag = None
# 	if tag_id:
# 		posts, tag = Post.get_by_tag(tag_id)
# 	elif category_id:
# 		posts, category = Post.get_by_category(category_id)
# 	else:
# 		posts = Post.latest_posts()
# 	context = {
# 		'category': category,
# 		'tag': tag,
# 		'posts': posts,
# 		'sidebars': SideBar.get_all()
# 	}
# 	# 把字典Category.get_navs()中的内容添加到字典context中
# 	context.update(Category.get_navs())
# 	return render(request, 'blog/post_list.html', context)
#  将post函数改造成类
class CommonViewMixin:
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update({
			'sidebars': SideBar.get_all()
		})
		context.update(Category.get_navs())
		return context


class IndexView(CommonViewMixin, ListView):
	queryset = Post.latest_posts()
	paginate_by = 5
	context_object_name = 'posts'
	template_name = 'blog/post_list.html'


def post_detail(request, post_id):
	try:
		post = Post.objects.get(id=post_id)
	except Post.DoesNotExist:
		post = None

	context = {
		'post': post,
		'sidebars': SideBar.get_all(),
	}
	context.update(Category.get_navs())
	return render(request, 'blog/post_detail.html', context)
