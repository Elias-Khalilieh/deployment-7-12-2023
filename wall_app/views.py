import bcrypt
from django.shortcuts import render,redirect
from django.contrib import messages
from wall_app.models import User,Message,Comment


def display_log_reg(request):
    return render (request, "log_reg.html")

def display_home(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        context = {
            'allmessages':Message.objects.all().order_by("-created_at"),
        }
        return render(request,'logged.html',context)

def new_sign_up(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['inputpass']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user1 = User.new_user(first_name = request.POST['fname'],
        last_name = request.POST['lname'],
        email_address = request.POST['useremail'],
        password = pw_hash)
        request.session['id'] = user1.id
        request.session['username'] = user1.first_name
        return render(request,'logged.html')

def new_sign_in(request):
    user = User.objects.filter(email_address=request.POST['useremail'])
    if user: 
        logged_user = user[0] 
        if bcrypt.checkpw(request.POST['inputpass'].encode(), logged_user.password.encode()):
            request.session['id'] = logged_user.id
            request.session['username'] = logged_user.first_name
            return redirect('/success')
        else:
            messages.error(request,"Invalid Password")
            return redirect("/")
    else:
        messages.error(request,"Invalid email")
        return redirect("/")

def create_msg(request):
    logged_user = User.objects.get(id=request.session['id'])
    msg1 = Message.new_msg(message_entry=request.POST['message_add'],user = logged_user)
    return redirect ('/success')

def create_cmnt(request,msgid):
    logged_user = User.objects.get(id=request.session['id'])
    user_msg = Message.objects.get(id = msgid)
    cmnt1 = Comment.new_cmnt(comment_entry=request.POST['comment_add'],user = logged_user,message=user_msg)
    return redirect('/success')

def destroysession(request):
    request.session.flush()
    return redirect('/')

def delete_this_message(request,msgid):
    Message.delete_msg(msgid)
    return redirect("/success")

def delete_this_comment(request,cmntid):
    Comment.delete_cmnt(cmntid)
    return redirect("/success")
