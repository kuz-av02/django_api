import decimal
from datetime import datetime

from django.template.backends import django
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Q, Count

from .serializers import *


# # Create your views here.

@api_view(['GET'])
def users_options_view_all(request):
    if request.method == 'GET':
        user_option = LfUsersOptions.objects.all()
        serializer = UsersOptionsSerializer(user_option, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def users_options_create(request):
    if request.method == 'POST':
        user_id = request.data.get('user_id')
        try:
            user = LfUsersOptions.objects.get(user_id=user_id)
            return Response({'error': f'User with user_id={user_id} do exist'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            serializer = UsersOptionsSerializerPost(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
def users_options_view_one(request, pk):
    try:
        user_option = LfUsersOptions.objects.get(user_id=pk)
    except LfUsersOptions.DoesNotExist:
        return Response({'message': 'User option not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UsersOptionsSerializer(user_option)
        return Response(serializer.data)

    if request.method == 'PATCH':
        serializer = UsersOptionsSerializerPatch(data=request.data, instance=user_option, partial=True)
        if serializer.is_valid():
            if request.data.get('workmode') == 0:
                # Получаем все group_id для данного user_id
                group_ids = LfGroups.objects.filter(user_id=pk).values_list('id', flat=True)
                credits_sum = sum([LfGroups.objects.get(id=group).credits for group in group_ids])
                user_option.credits = credits_sum
                user_option.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        try:
            users_options = LfUsersOptions.objects.get(id=pk)
        except LfUsersOptions.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        users_options.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def group_view_all(request):
    if request.method == 'GET':
        groups = LfGroups.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def group_create(request):
    user_id = request.data.get('user_id')
    try:
        user = LfUsersOptions.objects.get(user_id=user_id)
    except LfUsersOptions.DoesNotExist:
        return Response({'error': f'User with user_id={user_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = GroupSerializerPost(data=request.data)
    if serializer.is_valid():
        try:
            interval = request.data.get('interval')
            mass = interval[1:len(interval) - 1].split(',')
            if mass[0].isdigit() and mass[1].isdigit():
                if int(mass[0]) > int(mass[1]) or (int(mass[0]) == 0 and int(mass[1]) != 0) or (
                        int(mass[1]) > 10800) or len(mass) > 2:
                    return Response({'error': f'invalid interval value'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': f'invalid interval value'}, status=status.HTTP_400_BAD_REQUEST)
        except LfGroups.DoesNotExist:
            return Response({'error': f'invalid interval value'}, status=status.HTTP_400_BAD_REQUEST)

        credits_user = decimal.Decimal(request.data.get('credits'))
        if credits_user > user.credits:
            return Response({'error': f'The value of the credits field is too large'},
                            status=status.HTTP_400_BAD_REQUEST)
        user.credits -= credits_user
        user.save()
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def groups_by_user_id(request, user_id):
    try:
        user = LfUsersOptions.objects.get(user_id=user_id)
    except LfUsersOptions.DoesNotExist:
        return Response({'error': f'User with user_id={user_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        group = LfGroups.objects.filter(user_id=user_id)
        serializer = GroupSerializer(group, many=True)
        return Response(serializer.data)


@api_view(['PATCH', 'DELETE'])
def group_edit(request, group_id):
    try:
        group = LfGroups.objects.get(id=group_id)
    except LfGroups.DoesNotExist:
        return Response({'error': f'Group with id={group_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PATCH':
        serializer = GroupSerializerPatch(data=request.data, instance=group, partial=True)
        if serializer.is_valid():
            interval = request.data.get('interval')
            if interval is not None:
                try:
                    mass = interval[1:len(interval) - 1].split(',')
                    if mass[0].isdigit() and mass[1].isdigit():
                        if int(mass[0]) > int(mass[1]) or (int(mass[0]) == 0 and int(mass[1]) != 0) or (
                                int(mass[1]) > 10800) or len(mass) > 2:
                            return Response({'error': f'invalid interval value'}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'error': f'invalid interval value'}, status=status.HTTP_400_BAD_REQUEST)
                except LfGroups.DoesNotExist:
                    return Response({'error': f'invalid interval value'}, status=status.HTTP_400_BAD_REQUEST)

            user_id = request.data.get('user_id')
            user = LfUsersOptions.objects.get(user_id=user_id)
            credits_user = decimal.Decimal(request.data.get('credits'))
            if credits_user > user.credits:
                return Response({'error': f'The value of the credits field is too large'},
                                status=status.HTTP_400_BAD_REQUEST)
            user.credits -= credits_user
            user.save()

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def list_countries_view(request):
    queryset = LfListCountries.objects.filter(~Q(name=None))
    serializer = ListCountriesSerializer(queryset, many=True)
    data = serializer.data

    for item in data:
        if not item['region']:
            del item['region']
        if not item['city']:
            del item['city']

    return Response(data)


@api_view(['GET'])
def list_countries_detail(request, pk):
    queryset = LfListCountries.objects.filter(id=pk)
    serializer = ListCountriesSerializer(queryset, many=True)
    data = serializer.data
    if pk == 99:
        return Response(status=status.HTTP_404_BAD_REQUEST)

    return Response(data)


@api_view(['GET'])
def show_geo_view_all(request):
    if request.method == 'GET':
        groups = LfShowingGeo.objects.all()
        serializer = ShowGeoSerializer(groups, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def show_geo_by_group(request, group_id):
    try:
        group = LfGroups.objects.get(id=group_id)
    except LfGroups.DoesNotExist:
        return Response({'error': f'Group with id={group_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    group = LfShowingGeo.objects.filter(group_id=group_id)
    serializer = ShowGeoSerializer(group, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def geo_create(request):
    group_id = request.data.get('group_id')
    try:
        group = LfGroups.objects.get(id=group_id)
    except LfGroups.DoesNotExist:
        return Response({'error': f'Group with group_id={group_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    country_id = request.data.get('country')
    try:
        country = LfListCountries.objects.get(id=country_id)
    except LfListCountries.DoesNotExist:
        return Response({'error': f'Country with id={country_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ShowGeoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH', 'DELETE'])
def geo_edit(request, geo_id):
    try:
        show_time = LfShowingGeo.objects.get(id=geo_id)
    except LfShowingGeo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        country_id = request.data.get('country')
        try:
            country = LfListCountries.objects.get(id=country_id)
        except LfListCountries.DoesNotExist:
            return Response({'error': f'Country with id={country_id} does not exist'},
                            status=status.HTTP_400_BAD_REQUEST)
        group_id = request.data.get('group_id')
        try:
            group = LfGroups.objects.get(id=group_id)
        except LfGroups.DoesNotExist:
            return Response({'error': f'Group with group_id={group_id} does not exist'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = ShowGeoSerializer(data=request.data, instance=show_time, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        show_time.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def show_times_view_all(request):
    groups = LfShowingTimes.objects.all()
    serializer = ShowTimesSerializer(groups, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def show_times_create(request):
    group_id = request.data.get('group_id')
    try:
        group = LfGroups.objects.get(id=group_id)
    except LfGroups.DoesNotExist:
        return Response({'error': f'Group with group_id={group_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ShowTimesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def show_times_view_one(request, group_id):
    try:
        group = LfGroups.objects.get(id=group_id)
    except LfGroups.DoesNotExist:
        return Response({'error': f'Group with group_id={group_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        group = LfShowingTimes.objects.filter(group_id=group_id)
        serializer = ShowTimesSerializer(group, many=True)
        return Response(serializer.data)


@api_view(['PATCH', 'DELETE'])
def show_times_edit(request, pk):
    try:
        show_time = LfShowingTimes.objects.get(id=pk)
    except LfShowingTimes.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        serializer = ShowTimesSerializer(data=request.data, instance=show_time, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        show_time.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def show_all_pages_view(request):
    queryset = LfPages.objects.all()
    serializer = ShowPagesSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def page_create(request):
    group_id = request.data.get('group_id')
    try:
        group = LfGroups.objects.get(id=group_id)
    except LfGroups.DoesNotExist:
        return Response({'error': f'Group with group_id={group_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    user_id = group.user_id
    # Получаем все group_id для данного user_id
    group_ids = LfGroups.objects.filter(user_id=user_id).values_list('id', flat=True)
    # Получаем количество страниц для каждого group_id
    page_counts = LfPages.objects.filter(group_id__in=group_ids).values('group_id').annotate(total=Count('id'))
    # Считаем суммарное количество страниц
    total_pages = sum([page_count['total'] for page_count in page_counts if page_count['group_id'] in group_ids])
    # Если суммарное количество страниц больше или равно 100, то не разрешаем создавать новую страницу
    if total_pages >= 100:
        return Response({'error': f'You cannot create more than 100 pages for this user={user_id}'})

    serializer = PostPageSerializer(data=request.data)
    if serializer.is_valid():
        try:
            showtime = request.data.get('showtime')
            mass = showtime[1:len(showtime) - 1].split(',')
            if mass[0].isdigit() and mass[1].isdigit():
                # изменить значение 10800 на app_meta.types_settings[user.type].max_showtime
                if int(mass[0]) > int(mass[1]) or (int(mass[1]) > 10800) or len(mass) > 2 or (int(mass[0]) < 15):
                    return Response({'error': f'invalid showtime value'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': f'invalid showtime value'}, status=status.HTTP_400_BAD_REQUEST)
        except LfGroups.DoesNotExist:
            return Response({'error': f'invalid showtime value'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
def show_page_detail(request, page_id):
    try:
        page = LfPages.objects.get(id=page_id)
    except LfPages.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        queryset = LfPages.objects.filter(id=page_id)
        serializer = ShowPagesSerializer(queryset, many=True)
        return Response(serializer.data)

    if request.method == 'PATCH':
        serializer = PatchPageSerializer(data=request.data, instance=page, partial=True)
        if serializer.is_valid():
            showtime = request.data.get('showtime')
            if showtime is not None:
                try:
                    mass = showtime[1:len(showtime) - 1].split(',')
                    if mass[0].isdigit() and mass[1].isdigit():
                        # изменить значение 10800 на app_meta.types_settings[user.type].max_showtime
                        if int(mass[0]) > int(mass[1]) or (int(mass[1]) > 10800) or len(mass) > 2 or (int(mass[0]) < 15):
                            return Response({'error': f'invalid showtime value'}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'error': f'invalid showtime value'}, status=status.HTTP_400_BAD_REQUEST)
                except LfGroups.DoesNotExist:
                    return Response({'error': f'invalid showtime value'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        group_id = page.group_id
        # Получаем количество страниц для group_id
        page_counts = LfPages.objects.filter(group_id=group_id).values_list('id', flat=True).count()
        # Удаляем группу, если у нее нет страниц
        if page_counts == 1:
            group = LfGroups.objects.get(id=group_id)
            group.delete()
        page.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def show_all_pages_options(request):
    queryset = LfPagesOptions.objects.all().order_by('page_id')
    serializer = ShowPagesOptionsSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def page_options_create(request):
    page_id = request.data.get('page_id')
    try:
        page = LfPages.objects.get(id=page_id)
    except LfGroups.DoesNotExist:
        return Response({'error': f'Page with page_id={page_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = PostPageOptionsSerializer(page, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def show_page_options_detail(request, page_id):
    queryset = LfPagesOptions.objects.filter(page_id=page_id)
    serializer = ShowPagesOptionsSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['PATCH', 'DELETE'])
def page_options_edit(request, pk):
    if request.method == 'PATCH':
        try:
            pageOptions = LfPagesOptions.objects.get(id=pk)
        except LfPagesOptions.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PatchPageOptionsSerializer(data=request.data, instance=pageOptions, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        try:
            pageOptions = LfPagesOptions.objects.get(id=pk)
        except LfPagesOptions.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        pageOptions.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def show_all_pages_compiled_stats(request):
    twenty_minutes_ago = django.utils.timezone.now() + datetime.timedelta(minutes=-20)
    queryset = LfPagesCompiledStats.objects.filter(date__gte=twenty_minutes_ago).order_by('page_id')
    serializer = ShowPagesCompiledStatsSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def show_page_compiled_stats_detail(request, page_id):
    queryset = LfPagesCompiledStats.objects.filter(page_id=page_id).order_by('date')
    serializer = ShowPagesCompiledStatsSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def show_all_pages_stats(request):
    queryset = LfPagesStats.objects.order_by('date', 'page_id')[:500]
    serializer = ShowPagesStatsSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def show_page_stats_detail(request, page_id):
    queryset = LfPagesStats.objects.filter(page_id=page_id).order_by('page_id')
    serializer = ShowPagesStatsSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def show_all_groups_options(request):
    queryset = LfGroupsOptions.objects.all().order_by('group_id')
    serializer = ShowGroupsOptionsSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def show_group_options(request, group_id):
    queryset = LfGroupsOptions.objects.filter(group_id=group_id)
    serializer = ShowGroupsOptionsSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def group_options_create(request):
    group_id = request.data.get('group_id')
    try:
        group = LfGroups.objects.get(id=group_id)
        serializer = PostGroupsOptionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except LfGroupsOptions.DoesNotExist:
        return Response({'error': f'Group options for group with id={group_id} already exist'},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH', 'DELETE'])
def group_options_edit(request, pk):
    try:
        groupOptions = LfGroupsOptions.objects.get(id=pk)
    except LfGroupsOptions.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        serializer = PatchGroupsOptionsSerializer(data=request.data, instance=groupOptions, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        groupOptions.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Возвращает возможные языки
def possible_language():
    # return "possible languages: 0 - русский, 1 - английский, 2 - другой"
    return [0, 1, 2]

# Возвращает возможные категории
# def possible_categories():
#     return  list(LfWebsitesCategory.objects.values_list('id', flat=True))
