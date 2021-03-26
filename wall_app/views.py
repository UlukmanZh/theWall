from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Message, Comment
import bcrypt
from datetime import datetime


def index(request):
    request.session.flush()
    return render(request, "index.html")


def register(request):
    
    errors = User.objects.user_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags = 'registration')
        return redirect('/')
    else:
        password = request.POST['reg_password']
        psw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['reg_email'],
            password=psw_hash
        )
        request.session['user_id'] = user.id
        return redirect('/success')


def success(request):

    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    all_messages = Message.objects.all()
    user_messages = user.messages.all()
    context = {
        'all_messages': all_messages,
        'first_name': user.first_name,
        'last_name':user.last_name,
        'id':user.id
        
    }


    return render(request, "success.html", context)


def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags = 'login')
        return redirect('/')
    else:
        user_list = User.objects.filter(email=request.POST['log_email'])
        if len(user_list) != 0:
            logged_user = user_list[0]
            if bcrypt.checkpw(request.POST['log_password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect('/success')
            else:
                messages.error(request, "Password you entered was incorrect. Please try again!", extra_tags = 'login')
                return redirect('/')

        else:
            messages.error(request, "We couldn't find matching email. Please enter correct email or register",extra_tags = 'login')
            return redirect('/')


def logout(request):
    request.session.flush()
    return redirect('/')

def post_message(request):
    errors = Message.objects.message_validator(request.POST)
    logged_user = User.objects.get(id=request.session['user_id'])
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags = 'error_message')
            return redirect('/success')
    else:
        message = Message.objects.create(
            mes_content = request.POST['message'],
            user = logged_user
        )
        return redirect('/success')

def delete_message(request):
    message_id = request.POST['delete']
    chosen_message = Message.objects.get(id=message_id)
    chosen_message.delete()
    return redirect('/success')

def post_comment(request):
    errors = Comment.objects.comment_validator(request.POST)
    message_id = request.POST['message_id']
    logged_user = User.objects.get(id=request.session['user_id'])
    chosen_message = Message.objects.get(id=message_id)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags = 'error_comment')
            return redirect('/success')
    else:
        Comment.objects.create(
            com_content = request.POST['comment'],
            user = logged_user,
            message = chosen_message
        )
        return redirect('/success')

def delete_comment (request):
    comment_id = request.POST['delete']
    chosen_comment = Comment.objects.get(id=comment_id)
    chosen_comment.delete()
    return redirect('/success')