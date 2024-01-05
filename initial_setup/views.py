from django.shortcuts import render
# from django.http import HttpResponse

# Upload all possible htmls with functions
def config(request):
    return render(request, 'views/config.html')

def PDT(request):

    machines = request.GET.get('machine_numb')
    tasks = request.GET.get('tasks')
    

    return render(request, 'views/PDT.html', {'machines': machines, 'tasks': tasks})