from django.contrib import admin


class BaseOwnAdmin(admin.ModelAdmin):
	"""
	1. 用来自动补充文章、分类、标签、侧边栏、友链这些Model的owner字段
	2. 用来针对queryset过滤当前用户的数据
	"""
	exclude = ('owner',)

	def save_model(self, request, obj, form, change):
		obj.owner = request.user
		return super(BaseOwnAdmin, self).save_model(request, obj, form, change)

	def get_queryset(self, request):
		qs = super(BaseOwnAdmin, self).get_queryset(request)
		return qs.filter(owner=request.user)