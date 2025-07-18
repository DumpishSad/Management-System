from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import TeamCreateForm
from users.models import User


@login_required
def create_team(request):
    if not request.user.is_admin():
        messages.error(request, "Только для админов =)")
        return redirect('profile')

    if request.method == 'POST':
        form = TeamCreateForm(request.POST)
        if form.is_valid():
            team = form.save()
            request.user.team = team
            request.user.save()
            messages.success(request, f"Команда '{team.name}' создана.")
            return redirect('team_detail')
    else:
        form = TeamCreateForm()

    return render(request, 'teams/create_team.html', {'form': form})


@login_required
def team_detail(request):
    if not request.user.team:
        messages.info(request, "Вы не состоите в команде.")
        return redirect('profile')

    members = request.user.team.user_set.all()
    return render(request, 'teams/team_detail.html', {'members': members})


@login_required
def manage_team(request):
    if not request.user.is_admin():
        messages.error(request, "Только администратор может управлять командой.")
        return redirect('profile')

    team = request.user.team

    current_members = team.user_set.exclude(id=request.user.id)

    available_users = User.objects.filter(team__isnull=True)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            user_id = request.POST.get('user_id')
            user = User.objects.get(id=user_id)

            if user.team:
                messages.warning(request, f"{user.username} уже состоит в команде.")
            else:
                user.team = team
                user.save()
                messages.success(request, f"{user.username} добавлен в команду.")

        elif action == 'set_role':
            user_id = request.POST.get('user_id')
            new_role = request.POST.get('role')
            user = User.objects.get(id=user_id)
            if user.team == team:
                user.role = new_role
                user.save()
                messages.success(request, f"Роль пользователя {user.username} обновлена.")

    return render(request, 'teams/manage_team.html', {
        'members': current_members,
        'available_users': available_users
    })


@login_required
def delete_team(request):
    if not request.user.is_admin():
        messages.error(request, "Только админ может удалить команду.")
        return redirect('profile')

    team = request.user.team
    if request.method == 'POST':
        members = list(team.user_set.all())
        team.delete()

        for member in members:
            member.team = None
            member.save()

        messages.success(request, "Команда удалена.")
        return redirect('profile')

    return render(request, 'teams/confirm_delete.html', {'team': team})