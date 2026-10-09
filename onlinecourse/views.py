from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Course, Lesson, Question, Choice, Submission, Enrollment

def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'onlinecourse/course_details_bootstrap.html', {'course': course})

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    
    # Retrieve enrollment for the current user and course
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    
    # Create a new submission instance
    submission = Submission.objects.create(enrollment=enrollment)
    
    # Get selected choice IDs from the POST request form
    selected_ids = request.POST.getlist('choice')
    for choice_id in selected_ids:
        choice = Choice.objects.get(pk=choice_id)
        submission.choices.add(choice)
        
    return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    # Calculate score logic
    score = 0
    total_possible_score = 0
    
    # Get all questions associated with the course's lessons
    for lesson in course.lesson_set.all():
        for question in lesson.question_set.all():
            total_possible_score += question.grade
            # Check if user's selected choices include all correct choices for this question
            correct_choices = set(question.choice_set.filter(is_correct=True))
            user_choices = set(submission.choices.filter(question=question))
            
            if correct_choices and correct_choices == user_choices:
                score += question.grade

    context = {
        'course': course,
        'submission': submission,
        'grade': score,
        'total_score': total_possible_score
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)