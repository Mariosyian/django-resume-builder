from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from datetime import datetime
from .forms import CreateResumeForm
from .models import Resume
from ..resume.models import ResumeItem

@login_required
def resume_view(request):
    """
    Main page with all the users resumes sorted alphabetically.
    """
    resumes = Resume.objects\
        .filter(user=request.user)\
        .order_by('name')
        
    # Get the number of items of each resume
    # Current complexity: O(n)
    for resume in resumes:
        # Query database each time for specific resume
        items = ResumeItem.objects\
            .filter(parent_resume_id=resume.id)\
            .all()
        resume.num_items = len(items)
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

    return render(request, 'user_resume/user_resume_create.html', {
      'form': form
    })


@login_required
def resume_edit_view(request, resume_id):
    """
    Handle a request to edit a resume.

    :param resume_id: The database ID of the Resume to edit.
    """
    
    try:
        resume = Resume.objects\
            .filter(user=request.user)\
            .get(id=resume_id)
    except Resume.DoesNotExist:
        raise Http404
      
    template_dict = {}

    if request.method == 'POST':
        if 'delete' in request.POST:
            resume.delete()
            return redirect(resume_view)

        form = CreateResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            form = CreateResumeForm(instance=resume)
            # TODO: Calculate number of items
            template_dict['message'] = 'Resume updated'
    else:
        form = CreateResumeForm(instance=resume)

    template_dict['form'] = form

    return render(request, 'user_resume/user_resume_edit.html', template_dict)

@login_required
def resume_info(request, resume_id):
    """
    Handle a request to view a resume.
    
    :param resume_id: The database ID of the Resume to view.
    """
    try:
        resume = Resume.objects\
            .filter(user=request.user)\
            .get(id=resume_id)
    except Resume.DoesNotExist:
        raise Http404
    
    # Get all resume items of this resume
    resume_items = ResumeItem.objects\
        .filter(parent_resume_id=resume_id)\
        .all()
        
    context = {'resume':resume , 'resume_items': resume_items}
    return render(request, 'user_resume/user_resume_view.html', context)