from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.views import View
from django.db.models import Q
from .models import *
from .forms import *

# Create your views here.

class SignUpView(View):
    template_name = 'sign_up.html'

    def get(self, request):
        form = UserRegistrationForm()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            if password == confirm_password:
                form.save()
                return redirect('sign_in')
            else:
                form.add_error('confirm_password', 'Password does not match')
        return render(request, self.template_name, {'form':form})

def sign_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login_type = form.cleaned_data['login_type']
            password = form.cleaned_data['password']

            if login_type == 'username':
                username = form.cleaned_data['username']
                user = NotesUser.objects.filter(username=username, password=password)
                request.session['username']=username
            elif login_type == 'email':
                email = form.cleaned_data['email']
                user =  NotesUser.objects.filter(email=email, password=password)
                request.session['email']=email
        
            if user.exists():
                return redirect('list')
            else:
                form.add_error(None, 'User not found')
    else:
        form = LoginForm()
    return render(request, 'sign_in.html', {'form':form})

def sign_out(request):
    if 'username' in request.session:
        del request.session['username']
    elif 'email' in request.session:
        del request.session['email']
    return redirect('sign_in')

def notes_list(request):
    note = Notes.objects.all()

    # Session
    session = request.session.get('username') or request.session.get('email')
    note = note.filter(Q(user__username__iexact=session) | Q(user__email__iexact=session))

    # Search
    if request.GET.get('query'):
        query = request.GET.get('query','')
        note = note.filter(Q(title__icontains=query) | Q(content__icontains=query))
    if request.GET.get('date'):
        date = request.GET.get('date','')
        note = note.filter(created_at__date=date)

    # Sorting
    sort_by = request.GET.get('sort_by', 'created_at')
    order_by = request.GET.get('order_by', 'desc')
    sort_by = sort_by if sort_by == 'created_at' else 'title'
    sort = f'-{sort_by}' if order_by == 'desc' else sort_by
    note = note.filter(is_archived=False, in_bin=False).order_by('-is_pinned', sort)

    context = {
        'note':note, 
        'session':session,
        'order_by':order_by,
        'sort_by':sort_by
    }
    return render(request, 'notes_list.html', context)

def create(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            title = request.POST.get('title','')
            content = request.POST.get('content','')
            if not title:
                title = content.split()[0] if content else "Untitled"
            note = form.save(commit=False)
            if 'username' in request.session:
                user = get_object_or_404(NotesUser, username=request.session['username'])
            elif 'email' in request.session:
                user = get_object_or_404(NotesUser,email=request.session['email'])
            if user:
                note.user = user  
                note.title = title
                note.content = content                                              
                note.save()
                return redirect('list')
    else:
        form = NotesForm()
    return render(request, 'note_create.html', {'form':form})

def detail(request, id):
    note = get_object_or_404(Notes, pk=id)
    return render(request, 'note_detail.html', {'note':note})

def edit(request, id):
    note = get_object_or_404(Notes, pk=id)
    if request.method == 'POST':
        form = NotesForm(request.POST, instance=note)
        if form.is_valid():
            title = request.POST.get('title','')
            content = request.POST.get('content','')
            if not title:
                title = content.split()[0] if content else "Untitled"
            note = form.save(commit=False)
            if 'username' in request.session:
                user = get_object_or_404(NotesUser, username=request.session['username'])
            elif 'email' in request.session:
                user = get_object_or_404(NotesUser,email=request.session['email'])
            if user:
                note.user = user  
                note.title = title
                note.content = content                                              
                note.save()
                return redirect('list')
    else:
        form = NotesForm(instance=note)
    return render(request, 'note_edit.html', {'form':form, 'note':note})

def delete(request, id):
    note = get_object_or_404(Notes, pk=id)
    if request.method == 'POST':
        note.delete()
        return redirect('list')
    return render(request, 'note_delete.html')

def toggle_pin(request, id):
    note = get_object_or_404(Notes, pk=id)
    note.is_pinned = not note.is_pinned
    note.save()
    if note.is_archived:
        return redirect('archive')
    return redirect('list')

def toggle_archive(request,id):
    note = get_object_or_404(Notes, pk=id)
    note.is_archived = not note.is_archived
    note.save()
    return redirect('list')

def archive(request):
    note = Notes.objects.all()
    session = request.session.get('username') or request.session.get('email')
    note = note.filter(Q(user__username__iexact=session) | Q(user__email__iexact=session) & Q(is_archived=True))
    if request.GET.get('query'):
        query = request.GET.get('query', '')
        note = note.filter(Q(title__icontains=query) | Q(content__icontains=query))
    if request.GET.get('date'):
        date = request.GET.get('date', '')
        note = note.filter(created_at__date=date)
    sort_by = request.GET.get('sort_by', 'created_at')
    order_by = request.GET.get('order_by', 'desc')
    sort_by = sort_by if sort_by == 'created_at' else 'title'
    sort = f'-{sort_by}' if order_by == 'desc' else sort_by
    note = note.filter(is_archived=True, in_bin=False).order_by('-is_pinned', sort)

    context = {
        'note':note, 
        'session':session,
        'order_by':order_by,
        'sort_by':sort_by
    }
    return render(request, 'archive.html', context)

def toggle_bin(request,id):
    note = get_object_or_404(Notes, pk=id)
    note.in_bin = not note.in_bin
    note.save()
    if note.in_bin:
        return redirect('bin')
    return redirect('list')

def bin(request):
    note = Notes.objects.all()
    session = request.session.get('username') or request.session.get('email')
    note = note.filter(Q(user__username__iexact=session) | Q(user__email__iexact=session) & Q(is_archived=True))
    if request.GET.get('query'):
        query = request.GET.get('query', '')
        note = note.filter(Q(title__icontains=query) | Q(content__icontains=query))
    if request.GET.get('date'):
        date = request.GET.get('date','')
        note = note.filter(created_at__date=date)
    sort_by = request.GET.get('sort_by', 'created_at')
    order_by = request.GET.get('order_by', 'desc')
    sort_by = sort_by if sort_by == 'created_at' else 'title'
    sort = f'-{sort_by}' if order_by == 'desc' else sort_by
    note = note.filter(in_bin=True).order_by(sort)

    context = {
        'note':note, 
        'session':session,
        'order_by':order_by,
        'sort_by':sort_by
    }
    return render(request, 'bin.html', context)

def share(request, share_uuid):
    note = get_object_or_404(Notes, share_uuid=share_uuid)
    return render(request, 'note_share.html', {'note':note})

def export_pdf(request, id):
    note = Notes.objects.get(pk=id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{note.title}.pdf"'
    pdf_canvas = canvas.Canvas(response)
    pdf_canvas.setFont("Helvetica", 12)
    pdf_canvas.drawString(100, 800, f"Title: {note.title}")
    pdf_canvas.drawString(100, 780, f"Content: {note.content}")
    pdf_canvas.drawString(100, 760, f"Date Created: {note.created_at.strftime('%d-%m-%Y %H:%M:%S')}")
    pdf_canvas.save()
    return response

def export_txt(request,id):
    note = Notes.objects.get(pk=id)
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{note.title}.txt"'
    response.write(f"Title: {note.title}\n")
    response.write(f"Content: {note.content}\n")
    response.write(f"Date Created: {note.created_at.strftime('%d-%m-%Y %H:%M:%S')}")
    return response