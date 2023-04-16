from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import *
import pytz


class UsersOptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = LfUsersOptions
        exclude = ("env",)


class UsersOptionsSerializerPost(serializers.ModelSerializer):
    workmode = serializers.ChoiceField(choices=[0, 1])
    type = serializers.ChoiceField(choices=[0, 1, 2])

    class Meta:
        model = LfUsersOptions
        exclude = ("env", 'experience',)

    def create(self, validated_data):
        validated_data['experience'] = 0
        validated_data['id'] = validated_data['user_id']
        return super().create(validated_data)


class UsersOptionsSerializerPatch(serializers.ModelSerializer):
    workmode = serializers.ChoiceField(choices=[0, 1])
    type = serializers.ChoiceField(choices=[0, 1, 2])

    class Meta:
        model = LfUsersOptions
        exclude = ("id", "user_id", "env", "experience",)


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = LfGroups
        exclude = ("moby", "version",)


class GroupSerializerPost(serializers.ModelSerializer):
    uniq_ip = serializers.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(168)])
    geo = serializers.ChoiceField(choices=[0, 1, 2, 3])
    moby_ratio = serializers.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    priority = serializers.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        model = LfGroups
        exclude = ("id", "moby", "version", "hour_limit_current", "day_limit_current", "date_add", "date_edit")

    def create(self, validated_data):
        validated_data['moby'] = 2
        validated_data['version'] = 2
        if validated_data['geo'] == 3:
            validated_data['geo'] = 99
        return super().create(validated_data)


class GroupSerializerPatch(serializers.ModelSerializer):
    uniq_ip = serializers.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(168)])
    geo = serializers.ChoiceField(choices=[0, 1, 2, 3])
    moby_ratio = serializers.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    priority = serializers.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        model = LfGroups
        exclude = ("id", "user_id", "moby", "version", "hour_limit_current", "day_limit_current", "date_add", "date_edit")

    def validate(self, data):
        geo = data.get('geo')
        if geo == 3:
            data['geo'] = 99
        return data


class ListCountriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = LfListCountries
        exclude = ("accept_language",)


class ShowGeoSerializer(serializers.ModelSerializer):

    class Meta:
        model = LfShowingGeo
        fields = '__all__'


class ShowTimesSerializer(serializers.ModelSerializer):
    hour = serializers.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(168)])

    class Meta:
        model = LfShowingTimes
        fields = '__all__'


class PatchShowTimesSerializer(serializers.ModelSerializer):
    hour = serializers.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(168)])

    class Meta:
        model = LfShowingTimes
        exclude = ("id", "group_id")


class ShowPagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = LfPages
        exclude = ('day_limit', 'day_limit_current', 'day_limit_up', 
            'referrers', 'keywords', "search_engines", "referrer_type",
        )


class PostPageSerializer(serializers.ModelSerializer):
    state = serializers.ChoiceField(choices=[0, 1])
    position = serializers.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)])

    class Meta:
        model = LfPages
        fields = ['id', 'group_id', 'position', 'state', 'url', 'showtime', 'behavior', 'elements', 'clicks', 'options']

    def create(self, validated_data):
        return super().create(validated_data)


class PatchPageSerializer(serializers.ModelSerializer):
    state = serializers.ChoiceField(choices=[0, 1])
    position = serializers.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)])

    class Meta:
        model = LfPages
        fields = ['position', 'state', 'url', 'showtime', 'behavior', 'elements', 'clicks', 'options']

    def create(self, validated_data):
        return super().create(validated_data)


class ShowPagesOptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = LfPagesOptions
        fields = '__all__'


class PostPageOptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = LfPagesOptions
        fields = ['page_id', 'option', 'value']

    def create(self, validated_data):
        return super().create(validated_data)


class PatchPageOptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = LfPagesOptions
        fields = ['option', 'value']

    def create(self, validated_data):
        return super().create(validated_data)


class ShowPagesCompiledStatsSerializer(serializers.ModelSerializer):

    class Meta:
        model = LfPagesCompiledStats
        fields = '__all__'


class ShowPagesStatsSerializer(serializers.ModelSerializer):

    class Meta:
        model = LfPagesStats
        fields = '__all__'


class ShowGroupsOptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = LfGroupsOptions
        fields = '__all__'


class PostGroupsOptionsSerializer(serializers.ModelSerializer):
    option = serializers.ChoiceField(choices=["retention", "autoimp", "mtz", "lm_from", "lm_to",
                                              "bm_from", "bm_to", "category", "language"])

    class Meta:
        model = LfGroupsOptions
        fields = ['group_id', 'option', 'value']

    def create(self, validated_data):
        return super().create(validated_data)

    def validate(self, data):
        option = data.get('option')
        value = data.get('value')
        if option == "retention" or option == "autoimp":
            if value.lower() in ['true', 'false']:
                if value.lower() == 'false':
                    value = None
            else:
                raise serializers.ValidationError("Value error")
        elif option == "mtz":
            if value in pytz.all_timezones:
                pass
            else:
                raise serializers.ValidationError("Value error")
        elif option == "lm_from" or option == "lm_to":
            try:
                if -500 <= int(value) <= 500:
                    pass
                else:
                    raise serializers.ValidationError("Value should be between -500 and 500")
            except:
                raise serializers.ValidationError("Invalid value")
        elif option == "bm_from" or option == "bm_to":
            try:
                if 0 <= int(value) <= 100:
                    pass
                else:
                    raise serializers.ValidationError("Value should be between -500 and 500")
            except:
                raise serializers.ValidationError("Invalid value")
        elif option == "category":
            try:
                int(value)
            except:
                raise serializers.ValidationError("Invalid value")
        elif option == "language":
            try:
                if int(value) in [0, 1, 2]:
                    if int(value) == 0:
                        value = None
                else:
                    raise serializers.ValidationError("Value error")
            except:
                raise serializers.ValidationError("Invalid value")

        data['value'] = value
        return data


class PatchGroupsOptionsSerializer(serializers.ModelSerializer):
    option = serializers.ChoiceField(choices=["retention", "autoimp", "mtz", "lm_from", "lm_to",
                                              "bm_from", "bm_to", "category", "language"])

    class Meta:
        model = LfGroupsOptions
        fields = ['option', 'value']

    def validate(self, data):
        option = data.get('option')
        value = data.get('value')
        print(value)
        if option == "retention" or option == "autoimp":
            if value.lower() in ['true', 'false']:
                if value.lower() == 'false':
                    value = None
            else:
                raise serializers.ValidationError("Value error")
        elif option == "mtz":
            if value in pytz.all_timezones:
                pass
            else:
                raise serializers.ValidationError("Value error")
        elif option == "lm_from" or option == "lm_to":
            try:
                if -500 <= int(value) <= 500:
                    pass
                else:
                    raise serializers.ValidationError("Value should be between -500 and 500")
            except:
                raise serializers.ValidationError("Invalid value")
        elif option == "bm_from" or option == "bm_to":
            try:
                if 0 <= int(value) <= 100:
                    pass
                else:
                    raise serializers.ValidationError("Value should be between -500 and 500")
            except:
                raise serializers.ValidationError("Invalid value")
        elif option == "category":
            try:
                int(value)
            except:
                raise serializers.ValidationError("Invalid value")
        elif option == "language":
            try:
                if int(value) in [0, 1, 2]:
                    if int(value) == 0:
                        value = None
                else:
                    raise serializers.ValidationError("Value error")
            except:
                raise serializers.ValidationError("Invalid value")

        data['value'] = value
        return data


