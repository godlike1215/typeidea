from django.contrib import admin
from django.contrib.admin.models import LogEntry

from .models import Category, Tag, Post
from django.utils.html import format_html
from django.urls import reverse
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnAdmin

# Register your models here.


class PostInline(admin.TabularInline):
	fields = ('title', 'desc')
	extra = 1
	model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnAdmin):
	inlines = [PostInline, ]
	list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
	fields = ('name', 'status', 'is_nav')

	def post_count(self, obj):
		return obj.post_set.count()
	post_count.short_description = '文章数量'


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnAdmin):
	list_display = ('name', 'status', 'created_time')
	fields = ('name', 'status')


class CategoryOwnerFilter(admin.SimpleListFilter):
	title = '分类过滤去'
	parameter_name = 'owner_category'

	def lookups(self, request, model_admin):
		# 获取当前用户下的所有分类的列表
		res = Category.objects.filter(owner=request.user).values_list('id', 'name')
		return res

	def queryset(self, request, queryset):
		category_id = self.value()
		if category_id:
			return queryset.filter(category_id=self.value())
		return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnAdmin):
	form = PostAdminForm
	list_display = [
		'title', 'category', 'status',
		'created_time', 'owner', 'operator',
	]
	fieldsets = (
		('基础配置', {
			'description': '基础描述',
			'fields': (
				('title', 'category'),
				'status',
			),
		}),
		('内容', {
			'fields': (
				'desc',
				'content',
			),
		}),
		('额外信息', {
			'classes': ('wide',),
			'fields': ('tag',),
		})
	)
	filter_horizontal = ('tag',)
	# 设置那些字段可以作为编辑页面的链接
	list_display_links = []

	list_filter = [CategoryOwnerFilter]
	search_fields = ['title', 'category__name']

	actions_on_top = True
	# actions_on_bottom = True

	# 编辑页面
	save_on_top = True

	def operator(self, obj):
		return format_html(
			'<a href="{}">编辑</a>',
			reverse('cus_admin:blog_post_change', args=(obj.id, ))
		)
	operator.short_description = '操作'

	def get_queryset(self, request):
		qs = super(BaseOwnAdmin, self).get_queryset(request)
		return qs.filter(owner=request.user)


@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
	list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']