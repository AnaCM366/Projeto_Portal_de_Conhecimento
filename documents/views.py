from django.shortcuts import render

def documentos(request):
    posts = Post.objects.filter(
        arquivo__isnull=False
    ).exclude(
        arquivo=''
    ).order_by('-criado_em')

    return render(request, 'documentos.html', {
        'posts': posts
    })