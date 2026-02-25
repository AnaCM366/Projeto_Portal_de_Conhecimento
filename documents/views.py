from django.shortcuts import render

def documentos(request):
    posts = Post.objects.exclude(arquivo='')
    return render(request, 'documentos.html', {'posts': posts})

posts = Post.objects.filter(arquivo__isnull=False)