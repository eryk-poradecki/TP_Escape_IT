from django.shortcuts import render

def home(request):

	context = {
		'title': 'Gamemaster home'
	}
	return render(request, 'Escape_IT_Gamemaster/home.html', context)
