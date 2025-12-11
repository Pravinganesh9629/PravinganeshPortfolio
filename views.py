from django.shortcuts import redirect, render
from .models import ProfileFields
import pdfkit
from django.http import HttpResponse
from django.template import loader
import io

config = pdfkit.configuration(
    wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
)


def index(request):

    if request.method == 'POST':
        action = request.POST.get("action")   

        data = {
            "name": request.POST.get("name"),
            "email": request.POST.get("email", ""),
            "phone": request.POST.get("phone", ""),
            "summary": request.POST.get("summary", ""),
            "degree": request.POST.get("degree", ""),
            "school": request.POST.get("school", ""),
            "university": request.POST.get("university", ""),
            "experience": request.POST.get("experience", ""),
            "skills": request.POST.get("skills", ""),
        }

        if action == "preview":
            return render(request, "resume.html", {"user_profile": data})

        if action == "save":
            profile = ProfileFields(**data)
            profile.save()
            return redirect("list")

    return render(request, "index.html")


def resume(request, id):
    user_profile = ProfileFields.objects.get(id=id)
    template = loader.get_template('resume.html')
    html = template.render({'user_profile': user_profile})

    options = {
        "page-size": "Letter",
        "encoding": "UTF-8",
        "enable-local-file-access": True,
        "load-error-handling": "ignore",
        "print-media-type": True,    
    }

    pdf = pdfkit.from_string(html, False, options=options, configuration=config)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
    return response


def List(request):
    profiles = ProfileFields.objects.all()
    return render(request,'list.html',{'profiles':profiles})


def delete_profile(request, id):
    profile = ProfileFields.objects.get(id=id)
    profile.delete()
    return redirect('list')

def preview_by_id(request, id):
    profile = ProfileFields.objects.get(id=id)
    return render(request, "resume.html", {"user_profile": profile})


def update_profile(request, id):
    profile = ProfileFields.objects.get(id=id)

    if request.method == "POST":
        profile.name = request.POST.get("name")
        profile.email = request.POST.get("email")
        profile.phone = request.POST.get("phone")
        profile.summary = request.POST.get("summary")
        profile.degree = request.POST.get("degree")
        profile.school = request.POST.get("school")
        profile.university = request.POST.get("university")
        profile.experience = request.POST.get("experience")
        profile.skills = request.POST.get("skills")

        profile.save()
        return redirect("list")

    return render(request, "update.html", {"profile": profile})

