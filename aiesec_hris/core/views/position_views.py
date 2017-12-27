from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from ..models import LC


def positions_json(request, pk):
    lc = get_object_or_404(LC, pk=pk)
    positions = list(lc.position.values('pk', 'title'))
    return JsonResponse({'details': positions})
