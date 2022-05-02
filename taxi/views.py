from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Driver, Car, Manufacturer
from .forms import CarForm, DriverCreationForm, DriverUpdateForm, CarSearchForm


@login_required
def index(request):
    """View function for the home page of the site."""

    num_drivers = Driver.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_drivers": num_drivers,
        "num_cars": num_cars,
        "num_manufacturers": num_manufacturers,
        "num_visits": num_visits,
    }

    return render(request, "taxi/index.html", context=context)


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view for a list of manufacturers."""

    model = Manufacturer
    context_object_name = "manufacturer_list"
    template_name = "taxi/manufacturer_list.html"
    paginate_by = 10


class ManufacturerCreateView(LoginRequiredMixin, generic.CreateView):
    """Generic class-based view for creating a new manufacturer."""

    model = Manufacturer
    fields = "__all__"
    template_name = "taxi/manufacturer_form.html"
    success_url = reverse_lazy("taxi:manufacturer-list")


class ManufacturerUpdateView(LoginRequiredMixin, generic.UpdateView):
    """Generic class-based view for updating a manufacturer."""

    model = Manufacturer
    fields = "__all__"
    template_name = "taxi/manufacturer_form.html"
    success_url = reverse_lazy("taxi:manufacturer-list")


class ManufacturerDeleteView(LoginRequiredMixin, generic.DeleteView):
    """Generic class-based view for deleting a manufacturer."""

    model = Manufacturer
    success_url = reverse_lazy("taxi:manufacturer-list")
    template_name = "taxi/manufacturer_confirm_delete.html"


class CarListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view for a list of cars."""

    model = Car
    paginate_by = 10
    queryset = Car.objects.all().select_related("manufacturer")

    def get_context_data(self, *, objects_list=None, **kwargs):
        """Add car search form to context."""
        context = super(CarListView, self).get_context_data(**kwargs)
        model = self.request.GET.get("model", "")
        context["search_form"] = CarSearchForm(initial={
            "model": model
        })
        return context

    def get_queryset(self):
        """Return queryset filtered by search form."""
        form = CarSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                model__startswith=form.cleaned_data["model"]
            )
        return self.queryset


class CarCreateView(LoginRequiredMixin, generic.CreateView):
    """Generic class-based view for creating a new car."""

    model = Car
    form_class = CarForm
    template_name = "taxi/car_form.html"
    success_url = reverse_lazy("taxi:car-list")


class CarUpdateView(LoginRequiredMixin, generic.UpdateView):
    """Generic class-based view for updating a car."""

    model = Car
    form_class = CarForm
    template_name = "taxi/car_form.html"
    success_url = reverse_lazy("taxi:car-list")


class CarDeleteView(LoginRequiredMixin, generic.DeleteView):
    """Generic class-based view for deleting a car."""

    model = Car
    success_url = reverse_lazy("taxi:car-list")
    template_name = "taxi/car_confirm_delete.html"


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    """Generic class-based detail view for a car."""

    model = Car


class DriverListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view for a list of drivers."""

    model = Driver
    paginate_by = 10


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    """Generic class-based view for creating a new driver."""

    model = Driver
    form_class = DriverCreationForm
    template_name = "taxi/driver_form.html"


class DriverUpdateView(LoginRequiredMixin, generic.UpdateView):
    """Generic class-based view for updating a driver."""

    model = Driver
    form_class = DriverUpdateForm
    template_name = "taxi/driver_form.html"


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    """Generic class-based view for deleting a driver."""

    model = Driver
    success_url = reverse_lazy("taxi:driver-list")
    template_name = "taxi/driver_confirm_delete.html"


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    """Generic class-based detail view for a driver."""

    model = Driver
    queryset = Driver.objects.all().prefetch_related("cars__manufacturer")
