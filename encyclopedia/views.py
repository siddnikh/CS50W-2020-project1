from django.shortcuts import render, redirect

#for the random button
import random

#for turning text to markdown
from markdown2 import Markdown

from . import util

def index(request):
    
    #if they submitted anything in the search bar
    if 'q' in request.GET:
        
        #for search flexibility
        search_query = request.GET['q'].capitalize()
        
        #if the query given is exactly same as one of the titles, it shows them the page, directly
        if search_query in util.list_entries():
            return redirect('encyclopedia:entry', TITLE = search_query)
        
        entries = []
        
        #running through all the titles
        for entree in util.list_entries():
            
            #checking for the query as a substring of the titles
            if search_query in entree:
                entries.append(entree)
        
        return render(request, 'encyclopedia/search.html', {
            "title": "Search results for " + "\"" + search_query + "\"",
            "entries": entries
            })
    
    #if nothing is searched, a normal list of all the articles is provided
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, TITLE):
    
    if 'q' in request.GET:
        
        #for search flexibility
        search_query = request.GET['q'].capitalize()
        
        #if the query given is exactly same as one of the titles, it shows them the page, directly
        if search_query in util.list_entries():
            return redirect('encyclopedia:entry', TITLE = search_query)
        
        entries = []
        
        #running through all the titles
        for entree in util.list_entries():
            
            #checking for the query as a substring of the titles
            if search_query in entree:
                entries.append(entree)
        
        return render(request, 'encyclopedia/search.html', {
            "title": "Search results for " + "\"" + search_query + "\"",
            "entries": entries
            })
    
    #getting the content for the article
    text = util.get_entry(title = TITLE)
    
    #if no such article is found
    if text == None:
        return render(request, "encyclopedia/error.html", {
            "entries": util.list_entries()
        })
    
    #markdown2 class object
    md = Markdown()
    
    #this converts the desired markdown to HTML text
    text = md.convert(text)
    
    return render(request, "encyclopedia/entry.html", {
        "title": TITLE,
        "text": text
    })

def new(request):
    
    #when the submit button is pressed
    if request.method == 'POST':
        
        title = request.POST['title'] #title
        new_article = request.POST.get('new_article') #content of the new article
        
        #checking for an article with the same name
        if title in util.list_entries():
            
            #doesn't allow adding an article with the same name
            return render(request, "encyclopedia/new.html", {
                "message": "An article with this name already exists. Please try again."
            })
            
        #using already provided function from utils.py save this as a markdown file
        util.save_entry(title, new_article)
        
        #redirecting to the newly created page
        return redirect(f"/wiki/{title}")
    
    #before the button is pressed, new.html is rendered on screen
    return render(request, "encyclopedia/new.html")

def edit(request, TITLE):
    
    #when the submit button is pressed
    if request.method == "POST":
        
        #this function is exactly like the new() function except it overwrites the articles with the same titles.
        
        title = request.POST['title']
        new_article = request.POST.get('new_article')
        
        util.save_entry(title, new_article)
        
        return redirect(f"/wiki/{title}")
    
    #won't happen unless a person explicitly types /edit/xyz in the url
    if util.get_entry(TITLE) == None:
        
        return render(request, "encyclopedia/error.html", {
            "message": "No such document exists."
        })
    
    #gets the content entered
    content = util.get_entry(TITLE)
    
    #renders the same page as new.html except, it adds these tags as well.
    return render(request, "encyclopedia/edit.html", {
    "title": TITLE,
    "new_article": content
    })
    
def rand(request):
    
    
    n = len(util.list_entries())
    k = random.randrange(n)
    
    #getting a random index for an article
    title = util.list_entries()[k]
    
    return redirect(f"/wiki/{title}")