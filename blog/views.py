from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Character, Equipement
from django.contrib import messages

def character_list(request):
    characters = Character.objects.all()
    return render(request, 'blog/character_list.html', {'characters': characters})

def character_detail(request, id_character):
    character = get_object_or_404(Character, id_character=id_character)
    lieu = character.lieu
    form=MoveForm(request.POST, instance=character)
    lieux = {"église": "en manque d'aura noire", "cimetière": "épuisé", "hôpital": "affamé", "ruelle": "malicieux"}
    if form.is_valid():
        lieu.disponibilite = "libre"
        lieu.save()
        form.save(commit=False)
        nouveau_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
        if nouveau_lieu.disponibilite == 'occupé(e)':
            messages.error(request, f"{nouveau_lieu.id_equip.capitalize()} est déjà occupé(e).")
        elif character.etat != lieux[nouveau_lieu.id_equip]:
            messages.error(request, f"{character.id_character} n'est pas {lieux[nouveau_lieu.id_equip]}.")
        else:
            if nouveau_lieu.id_equip != 'cimetière':
                if nouveau_lieu.id_equip == 'église':
                    character.etat = 'épuisé'
                    messages.error(request, f"{character.id_character} a fait le plein d'aura, il est se sent très {character.etat}.")
                    character.save()
                elif nouveau_lieu.id_equip == 'hôpital':
                    character.etat = 'malicieux'
                    messages.error(request, f"{character.id_character} s'est régalé, il est maintenant {character.etat}.")
                    character.save()
                elif nouveau_lieu.id_equip == 'ruelle':
                    character.etat = "en manque d'aura noire"
                    messages.error(request, f"{character.id_character} s'est bien amusé, il est maintenant {character.etat}.")
                    character.save()
                nouveau_lieu.disponibilite = "occupé(e)"
                nouveau_lieu.save()
                form.save()
            else:
                character.etat = 'affamé'
                messages.error(request, f"{character.id_character} s'est bien reposé, il est maintenant {character.etat}.")
                character.save()
                nouveau_lieu.save()
                form.save()

        return redirect('character_detail', id_character=id_character)
    else:
        form = MoveForm()
        return render(request,
                  'blog/character_detail.html',
                  {'character': character, 'lieu': lieu, 'form': form})

