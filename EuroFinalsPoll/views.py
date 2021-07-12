from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

# import the required fields from the database
from .models import Question, Choice


# this is the landing page. this method tells the page to load the
# template index.html
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    # returns a rendered request
    return render(request, 'EuroPoll/index.html', context)


# this method tells the page to load the detail.html
# template where the questions are served
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)  # 404 is error handler
    # just in case a non existent page is requested
    return render(request, 'EuroPoll/detail.html', {'question': question})


# When the page visitor clicks on a question from the detail page, voting page
# is loaded. This method defines the procedure
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'EuroPoll/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('EuroFinalsPoll:results', args=(question.id,)))


# this method loads the result page after voting is concluded
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'EuroPoll/results.html', {'question': question})
