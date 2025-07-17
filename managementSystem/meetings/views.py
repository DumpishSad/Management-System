from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.transaction import commit
from django.shortcuts import render, redirect

from meetings.models import Meeting
from meetings.forms import MeetingForm


@login_required
def create_meeting(request):
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            participants = form.cleaned_data['participants']

            for user in participants:
                conflict = Meeting.objects.filter(
                    participants=user,
                    date=date,
                    time=time
                ).exists()

                if conflict:
                    messages.error(request, f"У {user.username} уже есть встреча в это время.")
                    return render(request, 'meetings/meeting_form.html', {'form': form})
            meeting.save()
            form.save_m2m()
            messages.success(request, "Встреча успешно создана.")

            return redirect('my_meetings')
    else:
        form = MeetingForm()

    return render(request, 'meetings/meeting_form.html', {'form': form})


@login_required
def my_meetings(request):
    meetings = request.user.meeting_set.order_by('date', 'time')
    return render(request, 'meetings/my_meetings.html', {'meetings': meetings})


@login_required
def delete_meeting(request, pk):
    meeting = Meeting.objects.get(pk=pk)

    if request.method == 'POST':
        meeting.delete()
        messages.success(request, "Встреча отменена.")
        return redirect('my_meetings')

    return render(request, 'meetings/delete_confirm.html', {'meeting': meeting})