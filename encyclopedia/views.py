from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
import random
from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    page = util.get_entry(title)
    if page is None:
        return render(request, "encyclopedia/error.html",
                      {"message": "Page not found."})
    else:
        return render(request, "encyclopedia/title.html", {
            "title": title,
            "entry": page
        })

def search(request):
    s = request.POST.get('q')
    if request.method == "POST":
        search_result = []
        for entry in util.list_entries():
            if s.lower() in entry.lower():
                search_result.append(entry)
            if s.lower() == entry.lower():
                return redirect('entry', title=s)
        return render(request, "encyclopedia/search.html", {
            "entries": search_result,
            "num": len(search_result)
        })

def newpage(request):
    if request.method == "POST":
        t = request.POST.get("t")
        content = request.POST.get("content")
        ti = f"#{t}\n"
        if t in util.list_entries():
            return render(request, "encyclopedia/error.html", {"message": "Your title is existed in this site. Please change to another one"})
        else:
            util.save_entry(t, ti + content)
            return HttpResponseRedirect(f"wiki/{t}")

    return render(request, "encyclopedia/newpage.html")

def r(request):
    rand = random.randint(0, len(util.list_entries())-1)
    return redirect('entry', title=util.list_entries()[rand])

def edit(request, title):
    if request.method == "POST":
        content = request.POST.get("content")
        ti = f"#{title}\n"
        util.save_entry(title, ti + content)
        return redirect('entry', title=title)
    else:
        with open(f'./entries/{title}.md') as entry:
            entry_content = entry.readlines()
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "entry": ''.join(entry_content[1:])
        })