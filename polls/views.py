from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question

# every generic view needs to know what mode it will be acting upon
# .DetailView generic view expects the primary key value captured from the URL to be called
# "pk", so we've changed question_id to pj for generic views (see polls/urls.py)

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # return the last five published questions (do not include those set to be published
        # in the future)
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):

    question = get_object_or_404(Question, pk=question_id)

    try:
        # request.POST is a dict like object that lets you access submitted data by key name
        # this with ['choice'] returns the ID of the selected choice as a string
        selected_choice = question.choice_set.get(pk=request.POST['choice'])

    # request.POST['choice'] will raise a keyerror is choice wasn't provided in POST data
    except (KeyError, Choice.DoesNotExist):
        # redisplay the question voting form
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # always return an HttpResponseRedirect after successfully dealing with POST data.
        # this prevents data from being posted twice if a user hits the "BACK" button
        # reverse is used to take us back to the previous page without hardcoding
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))

#OLD CODE
'''
def index(request):
    # -pub_date is order by pub_date in descending order, the first 5 of that list
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
'''