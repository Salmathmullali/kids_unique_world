from django.conf import settings
from django.contrib.auth import logout as logouts
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth. models import User
from .forms import parent_regform,loginform,editform,childform,bookform,videoform,child_editform,gameform,video_editform,video_editcategoryform,book_editcategoryform,bookcategoryform,videocategoryform
from .models import parent,child,kids_video,books,Video,video_category,book_category
from django.contrib import messages
import  random
from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def reg(request):
    return render(request,'signin.html')
def parent_regi(request):
    if request.method == 'POST':
        form = parent_regform(request.POST)
        if form.is_valid():
            post_email = form.cleaned_data['email']
            if parent.objects.filter(email=post_email).exists():
                messages.warning(request, "Email Id Already Exist")
                return redirect('/parent_reg/')
            else:
                form.save()
                uname = parent.objects.get(email=post_email)
                User.objects.create_user(username=uname, email=post_email)
                fname = form.cleaned_data['firstname']
                lname = form.cleaned_data['lastname']
                subject = 'welcome to kids unique world'
                message = f'Hi {fname} {lname}, thank you for registering in kids unique world.'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = ['135salma7@gmail.com', ]
                send_mail(subject, message, email_from, recipient_list)
                messages.warning(request, "Registration Successful")
                return redirect('/parent_reg/')

    else:
        form = parent_regform()
        return render(request, "main/parent_reg.html", {'form': form})



def login(request):
    if request.method == 'POST':
        form = loginform(request.POST)
        if form.is_valid():
            email_val = form.cleaned_data['email']
            pswd = form.cleaned_data['password']
            try:
                    user = parent.objects.get(email=email_val)
                    if user:
                        try:
                            user1 = parent.objects.get(Q(reg_id=user.reg_id) & Q(password=pswd))
                            if user1:
                                if user.user_type==1:
                                    request.session['session_id'] = user.reg_id
                                    return redirect('/admin_act/%s' % user.reg_id)
                                else:
                                    if user.status==True:
                                        request.session['session_id'] = user.reg_id
                                        return redirect('/parent_home/%s' % user.reg_id)
                                    else:
                                        return redirect('/login/')
                        except parent.DoesNotExist:
                            user1 = None
                            messages.warning(request, "Incorrect Password")
                            return redirect('/login/')
            except parent.DoesNotExist:
                try:
                    user = child.objects.get(email=email_val)
                    if user:
                        try:
                            user1 = child.objects.filter(child_id=user.child_id).filter(password=pswd)
                            if user1:
                                if user.user_type == 3:
                                    request.session['session_id'] = user.child_id
                                    return redirect('/child_home/%s' % user.child_id)
                                else:
                                    return redirect('/login/')
                        except child.DoesNotExist:
                            user1 = None
                            messages.warning(request, "Incorrect Password")
                            return redirect('/login/')

                except child.DoesNotExist:
                    user = None
                    messages.warning(request, "Invalid Email Id")
                    return redirect('/login/')
    else:
        form1 = loginform()
        return render(request, "login.html", {'form': form1})


def child_home(request,uid):
    if request.session.get('session_id'):
        return render(request, 'child_home.html', {'login_id':uid})
    else:
        return redirect('/login/')

def delete_user(request, id,uid):
    if request.session.get('session_id'):
        delete_user = parent.objects.filter(reg_id=id).delete()
        return redirect('/admin_act/%s' % uid)
    else:
        return redirect('/login/')


def index(request):

        return render(request, 'main/index.html')


def admin_act(request,uid):
    return render(request, 'admin_act.html',{'login_id':uid})



def home(request,uid):
    if request.session.get('session_id'):
        return render(request, 'home.html',{'login_id':uid})
    else:
        return redirect('/login/')


def logout(request):
    del request.session['session_id']
    logouts(request)
    return redirect('/')





def approve(request,uid, id):
    length_of_string = 12
    sample_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#@$^&*/!"
    pswd = ''.join(random.choices(sample_str, k=length_of_string))
    parent1 = parent.objects.get(reg_id=id)
    parent.objects.filter(reg_id=id).update(password=pswd,status=True)
    subject = 'Kids Unique World'
    message = f'Hi ' + parent1.firstname + ' ' + parent1.lastname + ', Thank you for choosing Kids Unique World.\n' \
              f'Your Email Id and Password has been provided below :\n' \
              f'Email Id : ' + parent1.email +' \n' \
              f'Password : {pswd} \n' \
              f'Thank you..'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['13salma7@gmail.com', ]
    send_mail(subject, message, email_from, recipient_list)
    messages.warning(request, "Registration Successful")
    return redirect('/approve_parent/%s' % uid)

def reject(request, uid,id):
    delete_user = parent.objects.filter(reg_id=id).delete()
    return redirect('/approve_parent/%s' % uid)

def approve_parent_list(request, uid):
    if request.session.get('session_id'):
        parent1 = parent.objects.filter(status=False)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(parent1, 5)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "approve_parent.html",
                      { 'login_id': uid, 'page_obj': page_obj})
    else:
        return redirect('/login/')




def edit(request, uid):
    if request.session.get('session_id'):
        user = parent.objects.get(reg_id=uid)
        if request.method == 'POST':
            form = editform(request.POST or None, instance=user)
            if form.is_valid():
                form.save()
                return redirect('/parent_view/%s' % uid)
        else:
            form = editform(instance=user)
            return render(request, 'parent_edit.html', {'form': form,'login_id':uid})
    else:
        return redirect('/login/')

def child_reg(request,uid):
    if request.method== 'POST' :
        form = childform(request.POST, request.FILES)
        if form.is_valid():
            post_email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['firstname']
            last_name = form.cleaned_data['lastname']
            age = form.cleaned_data['age']
            if User.objects.filter(email=post_email).exists():
                messages.warning(request,"user already exists")
                return redirect('/parent_home/%s' % uid)
            else:
                parent_id=parent.objects.get(reg_id=uid)
                tab=child.objects.create(password=password,firstname=first_name,lastname=last_name,age=age,email=post_email,parent_id=parent_id)
                tab.save()
                return redirect('/parent_home/%s' % uid)
    else:
            form=childform()
            return render(request,'child_reg.html',{'form':form, 'login_id' : uid})


def book_display(request,uid):
    if request.session.get('session_id'):
        user = books.objects.filter(parent_id=uid)
        return render(request, 'book_display.html', {'users': user,'login_id':uid})
    else:
        return redirect('/login/')


def kids_book(request,uid):
    if request.session.get('session_id'):
        if request.method == 'POST':
            form = bookform(request.POST, request.FILES)
            if form.is_valid():
                uploads=form.cleaned_data['upload_name']
                upload_info= form.files['upload_book']
                user=parent.objects.get(reg_id=uid)
                books.objects.create(upload_name=uploads,upload_book=upload_info,parent_id=user)

                return redirect('/book_display/%s' % uid)
        else:
            gal_form = bookform()
            return render(request, 'books.html', {'form': gal_form,'login_id':uid})
    else:
        return redirect('/login/')

def video_display(request,uid):
    if request.session.get('session_id'):
        user = kids_video.objects.all()
        return render(request, 'video_display.html', {'users': user,'login_id':uid})
    else:
        return redirect('/login/')


def kids_videos(request,uid):
    if request.session.get('session_id'):
        if request.method == 'POST':
            form = videoform(request.POST, request.FILES)
            uploads = request.POST.get('upload_name')
            upload_info = request.POST.get('upload_videos')
            print("--------------------------------------------------------------",uploads)
            print("--------------------------------------------------------------",upload_info)
            if form.is_valid():
                uploads=form.cleaned_data['upload_name']
                upload_info= form.files['upload_videos']
                user=parent.objects.get(reg_id=uid)
                kids_video.objects.create(upload_videos=upload_info,upload_name=uploads,parent_id=user)
                return redirect('/video_display/%s' % uid)
        else:
            vid_form = videoform()
            return render(request, 'videos.html', {'form': vid_form,'login_id':uid})
    else:
        return redirect('/login/')

def uploads_approve(request,uid):
    if request.session.get('session_id'):
        user = kids_video.objects.filter(Status=False)
        return render(request, 'uploads_approve.html', {'users': user,'login_id':uid})
    else:
        return redirect('/login/')


def child_list(request, uid):
    if request.session.get('session_id'):
        child1 = child.objects.filter(parent_id=uid)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(child1, 1)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, 'child_list.html', { 'page_obj': page_obj,'login_id':uid})
    else:
        return redirect('/login/')

def child_edit(request, uid):
    if request.session.get('session_id'):
        user = child.objects.get(child_id=uid)
        if request.method == 'POST':
            form = child_editform(request.POST or None, instance=user)
            if form.is_valid():
                form.save()
                return redirect('/child_list/%s' % uid)
        else:
            form = child_editform(instance=user)
            return render(request, 'child_edit.html', {'form': form,'login_id':uid})
    else:
        return redirect('/login/')

def parent_home(request,uid):
    return render(request,'parent/parent_home.html',{'login_id':uid})
def parent_view(request,uid):
    user = parent.objects.get(reg_id=uid)
    return render(request,'parent/parent_view.html',{'login_id':uid,'users':user})
# def child_list(request,uid):
#     user = parent.objects.get(reg_id=uid)
#     return render(request,'child_list.html',{'login_id':uid,'users':user})
def video_approve(request, uid,id):
    user=kids_video.objects.filter(video_id=id).update(Status=True)
    return redirect('/uploads_approve/%s' % id)



def video_reject(request,uid,id):
    user = kids_video.objects.filter(video_id=id).delete()
    return redirect('/uploads_approve/%s' % id)

def games(request,uid):
    if request.session.get('session_id'):
        user = books.objects.filter(game_id=uid)
        return render(request, 'kids_game.html', {'users': user,'login_id':uid})
    else:
        return redirect('/login/')

def parent_video_display(request,uid):
    if request.session.get('session_id'):
        user = kids_video.objects.filter(video_id=uid)
        return render(request, 'parent_video_display.html', {'users': user,'login_id':uid})
    else:
        return redirect('/login/')

def parent_book_display(request,uid):
    if request.session.get('session_id'):
        user = books.objects.filter(books_id=uid)
        return render(request, 'book_display.html', {'users': user,'login_id':uid})
    else:
        return redirect('/login/')
def kids_game(request,uid):
        if request.session.get('session_id'):
            if request.method == 'POST':
                form = gameform(request.POST, request.FILES)
                if form.is_valid():
                    uploads = form.cleaned_data['upload_name']
                    upload_info = form.files['upload_game']
                    user = parent.objects.get(reg_id=uid)
                    kids_game.objects.create(upload_name=uploads, upload_game=upload_info, parent_id=user)

                    return redirect('/games/%s' % uid)
            else:
                gform = gameform()
                return render(request, 'kids_game.html', {'form': gform, 'login_id': uid})
        else:
            return redirect('/login/')


def video_detail(request, video_id):
    video = kids_video.objects.filter(video_id=id)
    # Increment the view count when the video is accessed
    video.view_count += 1
    video.save()

    return render(request, 'video_detail.html', {'video': video})
def uploads_edit(request, uid):
    if request.session.get('session_id'):
        user = parent.objects.get(reg_id=uid)
        if request.method == 'POST':
            form = video_editform(request.POST or None, instance=user)
            if form.is_valid():
                form.save()
                return redirect('/parent_video_display/%s' % uid)
        else:
            form = video_editform(instance=user)
            return render(request, 'uploads_edit.html', {'form': form,'login_id':uid})
    else:
        return redirect('/login/')
def delete(request,uid,id):
    user = kids_video.objects.filter(video_id=id).delete()
    return redirect('/parent_video_display/%s' % id)

def book_delete(request,uid,id):
    user = books.objects.filter(book_id=id).delete()
    return redirect('/parent_book_display/%s' % id)
def add_video_category(request, uid):
    if request.session.get('session_id'):
        if request.method == 'POST':
            form = videocategoryform(request.POST)
            if form.is_valid():
                form.save()
                messages.warning(request, "Category Added Successfully")
                return redirect('/add_video_category/%s' % uid)
        else:
            form_value = videocategoryform()
            return render(request, "add_video_category.html", {'form_key': form_value, 'login_id': uid})
    else:
        return redirect('/login/')

def video_edit_category(request, uid):
    if request.session.get('session_id'):
        categories = video_category.objects.get(video_category_id=uid)
        if request.method == 'POST':
            form = video_editcategoryform(request.POST, instance=categories)
            if form.is_valid():
                form.save()
                messages.warning(request, "Updated Successfully")
                return redirect('/video_category_list/%s' % uid)
        else:
            form_value = video_editcategoryform(instance=categories)
            return render(request, "video_edit_category.html", {'form_key': form_value, 'login_id': uid})
    else:
        return redirect('/login/')


def video_catogery_list(request, uid):
    if request.session.get('session_id'):
        categories = video_category.objects.all()
        page_num = request.GET.get('page', 1)
        paginator = Paginator(categories, 5)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "video_catogery_list.html",
                      {'categories': categories, 'login_id': uid, 'page_obj': page_obj})
    else:
        return redirect('/login/')


def video_delete_category(request, uid, id):
    if request.session.get('session_id'):
        video_category.objects.get(video_category_id=id).delete()
        return redirect('/category_list/%s' % uid)
    else:
        return redirect('/login/')

def add_book_category(request, uid):
    if request.session.get('session_id'):
            if request.method == 'POST':
                form = bookcategoryform(request.POST)
                if form.is_valid():
                    form.save()
                    messages.warning(request, "Category Added Successfully")
                    return redirect('/add_book_category/%s' % uid)
            else:
                form_value = bookcategoryform()
                return render(request, "add_book_category.html", {'form_key': form_value, 'login_id': uid})
    else:
            return redirect('/login/')

def book_edit_category(request, uid, id):
    if request.session.get('session_id'):
        categories = book_category.objects.get(book_category_id=id)
        if request.method == 'POST':
            form = book_editcategoryform(request.POST, instance=categories)
            if form.is_valid():
                form.save()
                messages.warning(request, "Updated Successfully")
                return redirect('/category_list/%s' % uid)
        else:
            form_value = book_editcategoryform(instance=categories)
            return render(request, "book_edit_category.html", {'form_key': form_value, 'login_id': uid})
    else:
        return redirect('/login/')

def book_category_list(request, uid):
    if request.session.get('session_id'):
            categories = book_category.objects.all()
            page_num = request.GET.get('page', 1)
            paginator = Paginator(categories, 5)  # 6 employees per page
            try:
                page_obj = paginator.page(page_num)
            except PageNotAnInteger:
                # if page is not an integer, deliver the first page
                page_obj = paginator.page(1)
            except EmptyPage:
                # if the page is out of range, deliver the last page
                page_obj = paginator.page(paginator.num_pages)
            return render(request, "book_category_list.html",
                          {'categories': categories, 'login_id': uid, 'page_obj': page_obj})
    else:
            return redirect('/login/')

def book_delete_category(request, uid, id):
    if request.session.get('session_id'):
        book_category.objects.get(book_category_id=id).delete()
        return redirect('/book_category_list/%s' % uid)
    else:
        return redirect('/login/')



