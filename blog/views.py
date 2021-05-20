from django.shortcuts import redirect, render,HttpResponse
from blog.models import BlogComment, Post
from django.contrib import messages
# Create your views here.

def blogHome(request):
    allPosts = Post.objects.all()
    context = {'allpost':allPosts}
    return render(request,'blog/blog.html',context)

def blogPost(request, slug):
    post=Post.objects.filter(slug=slug).first()
    post.views = post.views + 1
    post.save()
    
    comments = BlogComment.objects.filter(post=post)
    context={"post":post,"comments":comments,'user': request.user}
    return render(request, "blog/blogPost.html", context)

def postComment(request):
    if request.method=='POST':
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        post = Post.objects.get(sno = postSno)
        parentSno = request.POST.get("parentSno")

        comment = BlogComment(comment=comment, user=user,post=post)
        comment.save()
        messages.success(request,'your comments have been posted successfully.')

    return redirect(f'/blog/{post.slug}')
    



