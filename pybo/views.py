from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from .models import Question

# Create your views here.


def index(request):
    question_list = Question.objects.order_by('-create_date')
    context = { "question_list" : question_list }
    
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = { 'question' : question }
    
    return render(request, 'pybo/question_detail.html', context)

def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    '''
    아래와 같이 변경하여 사용할 수 있다.
    
        from .models import Answer
        
        answer = Answer(question = question, content = request.POST.get('content'), create_date=timezone.now())
        answer.save()
    
    '''
    
    return redirect('pybo:detail', question_id=question.id)