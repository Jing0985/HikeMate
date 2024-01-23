from django.contrib.auth.decorators import login_required
from django.db.models import Q, Max, Min
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import is_valid_path

from .forms import TrailForm
from .models import Trail, Feature
from .utils import paginateTrails, searchTrails


# Create your views here.
def trails(request):
    # trails, search_query = searchTrails(request)
    # custom_range, trails = paginateTrails(request, trails, 6)
    trails = Trail.objects.all()
    features = Feature.objects.all()

    regions = trails.order_by('-region')
    unique_regions = set()
    length_max = trails.order_by('-length')[0].length
    length_min = trails.order_by('length')[0].length
    duration_max = trails.order_by('-duration')[0].duration
    duration_min = trails.order_by('duration')[0].duration
    for region in regions:
        unique_regions.add(region.region)
    context = {
        # "trails": trails,
        # "search_query": search_query,
        # "custom_range": custom_range,
        "features": features,
        "regions": unique_regions,
        "length_max": length_max,
        "length_min": length_min,
        "duration_max": duration_max,
        "duration_min": duration_min,
    }

    return render(request, "trails/trails.html", context)


def trail(request, pk):
    trailObj = Trail.objects.get(id=pk)
    return render(request, "trails/single-trail.html", {"trail": trailObj})


@login_required(login_url="login")
def createTrail(request):
    form = TrailForm()

    if request.method == "POST":
        form = TrailForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("trails")

    context = {"form": form}
    return render(request, "trails/trail_form.html", context)


@login_required(login_url="login")
def updateTrail(request, pk):
    trail = Trail.objects.get(id=pk)
    form = TrailForm(instance=trail)

    if request.method == "POST":
        form = TrailForm(request.POST, request.FILES, instance=trail)
        if form.is_valid():
            form.save()
            return redirect("trails")

    context = {"form": form}
    return render(request, "trails/trail_form.html", context)


@login_required(login_url="login")
def deleteTrail(request, pk):
    trail = Trail.objects.get(id=pk)

    if request.method == "POST":
        trail.delete()
        return redirect("trails")

    context = {"object": trail}
    return render(request, "trails/delete_template.html", context)
