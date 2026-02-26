from django.shortcuts import render
from posts.models import Post
# def documentos(request):
#     query = request.GET.get('q', '')

#     posts = Post.objects.filter(
#         arquivo__isnull=False
#     ).exclude(
#         arquivo=''
#     ).order_by('-criado_em')

#     return render(request, 'documentos.html', {
#         'posts': posts,
#         'query': query
#     })