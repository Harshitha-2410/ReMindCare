import json
import base64
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils.timezone import now

from .models import (
    Patient, Snapshot, Prescription, Reminder,
    DailyRoutine, FamilyContact, EmergencyContact
)
from .forms import (
    PatientForm, PrescriptionForm, ReminderForm,
    DailyRoutineForm
)

from .helpers.ocr_utils import image_to_text, parse_meds
from .helpers.gemini_helper import generate_gemini_reply


# ---------------- DASHBOARD ---------------- #

@login_required
def dashboard(request):
    if request.user.is_staff:
        return redirect("admin_dashboard")
    return redirect("user_dashboard")


@login_required
def user_dashboard(request):
    patient = Patient.objects.filter(user=request.user).first()
    routines = DailyRoutine.objects.filter(user=request.user).order_by("time")
    return render(request, "dashboard/user_dashboard.html", {
        "patient": patient,
        "routines": routines
    })


@login_required
def admin_dashboard(request):
    return render(request, "dashboard/admin_dashboard.html")


# ---------------- AUTH ---------------- #

def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )
        if user:
            login(request, user)
            return redirect("dashboard")
        return render(request, "auth/login.html", {"error": "Invalid credentials"})
    return render(request, "auth/login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


# ---------------- PATIENT ---------------- #

@login_required
def patient_create(request):
    if request.method == "POST":
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user = request.user
            patient.save()
            return redirect("user_dashboard")
    else:
        form = PatientForm()
    return render(request, "patient_form.html", {"form": form})


# ---------------- EMOTION (SAFE – NO CAMERA) ---------------- #

@csrf_exempt
@login_required
def analyze_emotion(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id, user=request.user)

    data = request.POST.get("image")
    if not data:
        return JsonResponse({"error": "No image"}, status=400)

    header, encoded = data.split(",", 1)
    image_bytes = base64.b64decode(encoded)

    filename = f"{uuid.uuid4().hex}.jpg"
    snapshot = Snapshot.objects.create(
        patient=patient,
        detected_emotion="neutral"
    )
    snapshot.image.save(filename, image_bytes)

    return JsonResponse({"emotion": "neutral"})


# ---------------- PRESCRIPTION ---------------- #

@login_required
def upload_prescription(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id, user=request.user)

    if request.method == "POST":
        form = PrescriptionForm(request.POST, request.FILES)
        if form.is_valid():
            pres = form.save(commit=False)
            pres.patient = patient
            pres.save()

            try:
                text = image_to_text(pres.file.path)
                pres.ocr_text = text
                pres.parsed_meds = parse_meds(text)
                pres.save()
            except Exception:
                pass

            return redirect("user_dashboard")

    else:
        form = PrescriptionForm()

    return render(request, "upload_prescription.html", {
        "form": form,
        "patient": patient
    })


# ---------------- REMINDERS ---------------- #

@login_required
def reminder_page(request):
    reminders = Reminder.objects.filter(user=request.user).order_by("reminder_time")

    if request.method == "POST":
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user
            reminder.save()
            return redirect("reminder_page")
    else:
        form = ReminderForm()

    return render(request, "reminders/reminders.html", {
        "form": form,
        "reminders": reminders,
        "now": now()
    })


# ---------------- CHATBOT (NO GEMINI IMPORT HERE) ---------------- #

@csrf_exempt
@login_required
def chatbot_reply(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
        message = (data.get("message") or "").strip()

        if not message:
            return JsonResponse({"reply": "Please say something."})

        reply = generate_gemini_reply(message)
        return JsonResponse({"reply": reply})

    except Exception:
        return JsonResponse({"reply": "Assistant unavailable right now."})


@login_required
def chatbot_page(request):
    return render(request, "chatbot.html")


# ---------------- FAMILY ---------------- #

@login_required
def family_page(request):
    contacts = FamilyContact.objects.filter(user=request.user)
    return render(request, "app/family.html", {"contacts": contacts})


@login_required
def add_family_contact(request):
    if request.method == "POST":
        FamilyContact.objects.create(
            user=request.user,
            name=request.POST["name"],
            relation=request.POST["relation"],
            phone=request.POST["phone"],
            photo=request.FILES.get("photo")
        )
    return redirect("family")
