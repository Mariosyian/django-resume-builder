from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from datetime import datetime
from .forms import CreateResumeForm
from .models import Resume

@login_required
def resume_view(request):
    """
    Handle a request to view a user's resume.
    """
    resumes = Resume.objects\
        .filter(user=request.user)\
        .order_by('name')

    return render(request, 'user_resume/user_resume.html', {
        'resumes': resumes
    })


@login_required
def resume_create_view(request):
    """
    Handle a request to create a new resume.
    """
    if request.method == 'POST':
        form = CreateResumeForm(request.POST)
        print(form)
        if form.is_valid():
            new_resume = form.save(commit=False)
            new_resume.user = request.user
            new_resume.num_items = 0
            new_resume.date_created = datetime.now().date()
            new_resume.date_modified = datetime.now().date()
            new_resume.save()

            return redirect(resume_view)
    else:
        form = CreateResumeForm()

    return render(request, 'user_resume/user_resume_create.html', {'form': form})


@login_required
def resume_edit_view(request, resume_id):
    """
    Handle a request to edit a resume.

    :param resume_id: The database ID of the Resume to edit.
    """
    
    try:
        resume_item = Resume.objects\
            .filter(user=request.user)\
            .get(id=resume_id)
    except Resume.DoesNotExist:
        raise Http404
    
    print(resume_item)
    template_dict = {}

    if request.method == 'POST':
        if 'delete' in request.POST:
            resume_item.delete()
            return redirect(resume_view)

        form = CreateResumeForm(request.POST, instance=resume_item)
        if form.is_valid():
            form.save()
            form = CreateResumeForm(instance=resume_item)
            # TODO: Calculate number of items
            template_dict['message'] = 'Resume updated'
    else:
        form = CreateResumeForm(instance=resume_item)

    template_dict['form'] = form

    return render(request, 'user_resume/user_resume_edit.html', template_dict)
