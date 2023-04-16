from django.db import models

# Create your models here.


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class LfApplicationIdentifiers(models.Model):
    id = models.CharField(primary_key=True, max_length=256)
    user_id = models.IntegerField(blank=True, null=True)
    date = models.BigIntegerField(blank=True, null=True)
    last_date = models.BigIntegerField(blank=True, null=True)
    uuid = models.CharField(max_length=256, blank=True, null=True)
    ip_addr = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lf_application_identifiers'


class LfApplicationOptions(models.Model):
    uuid = models.CharField(primary_key=True, max_length=128)
    options = models.JSONField(blank=True, null=True)
    date = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lf_application_options'


class LfGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.IntegerField()
    hour_limit = models.SmallIntegerField()
    hour_limit_current = models.SmallIntegerField(null=True) 
    geo = models.SmallIntegerField()
    uniq_ip = models.SmallIntegerField()
    credits = models.DecimalField(max_digits=16, decimal_places=5)
    interval = models.TextField()  # This field type is a guess.
    name = models.CharField(max_length=255)
    moby = models.SmallIntegerField(null=True)  
    moby_ratio = models.SmallIntegerField()
    date_add = models.BigIntegerField(null=True)  
    date_edit = models.BigIntegerField(null=True) 
    options = models.JSONField(blank=True, null=True)
    priority = models.SmallIntegerField()
    day_limit = models.SmallIntegerField()
    day_limit_current = models.SmallIntegerField(null=True)  
    version = models.SmallIntegerField()

    class Meta:
        managed = True
        db_table = 'lf_groups'


class LfGroupsOptions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group_id = models.BigIntegerField()
    option = models.CharField(max_length=12, blank=True, null=True)
    value = models.CharField(max_length=255, blank=True, null=True)
    date = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lf_groups_options'


class LfListCountries(models.Model):
    id = models.SmallAutoField(primary_key=True)
    country = models.CharField(max_length=255)
    region = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    accept_language = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lf_list_countries'


class LfPages(models.Model):
    id = models.BigAutoField(primary_key=True)
    group_id = models.BigIntegerField()
    position = models.SmallIntegerField()
    state = models.SmallIntegerField()
    day_limit = models.SmallIntegerField()
    day_limit_current = models.SmallIntegerField()
    day_limit_up = models.SmallIntegerField()
    showtime = models.TextField()  # This field type is a guess.
    referrers = models.JSONField(blank=True, null=True)
    keywords = models.JSONField(blank=True, null=True)
    url = models.JSONField(blank=True, null=True)
    search_engines = models.JSONField(blank=True, null=True)
    behavior = models.BooleanField()
    referrer_type = models.SmallIntegerField()
    clicks = models.BooleanField(blank=True, null=True)
    elements = models.JSONField(blank=True, null=True)
    options = models.JSONField(blank=True, null=True)
    date_add = models.BigIntegerField()
    date_edit = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'lf_pages'


class LfPagesCompiledStats(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.IntegerField()
    group_id = models.BigIntegerField()
    page_id = models.BigIntegerField()
    visits = models.IntegerField()
    credits = models.DecimalField(max_digits=16, decimal_places=5)
    data = models.JSONField(blank=True, null=True)
    date = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'lf_pages_compiled_stats'


class LfPagesOptions(models.Model):
    id = models.BigAutoField(primary_key=True)
    page_id = models.BigIntegerField()
    option = models.CharField(max_length=12, blank=True, null=True)
    value = models.CharField(max_length=255, blank=True, null=True)
    date = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lf_pages_options'


class LfPagesStats(models.Model):
    id = models.BigAutoField(primary_key=True)
    page_id = models.BigIntegerField()
    date = models.BigIntegerField(blank=True, null=True)
    data = models.JSONField(blank=True, null=True)
    group_id = models.BigIntegerField(blank=True, null=True)
    user_id = models.BigIntegerField(blank=True, null=True)
    client_user_id = models.BigIntegerField(blank=True, null=True)
    server = models.CharField(max_length=32, blank=True, null=True)
    ip_addr = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lf_pages_stats'


class LfPerfomance(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.BigIntegerField(blank=True, null=True)
    data = models.JSONField(blank=True, null=True)
    env = models.CharField(max_length=12, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lf_perfomance'


class LfProxyProfiles(models.Model):
    id = models.BigAutoField(primary_key=True)
    tag = models.CharField(max_length=255, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    proxy = models.CharField(max_length=255, blank=True, null=True)
    link_uuid = models.CharField(max_length=255, blank=True, null=True)
    date_create = models.BigIntegerField(blank=True, null=True)
    date_last_use = models.BigIntegerField(blank=True, null=True)
    date_last_check = models.BigIntegerField(blank=True, null=True)
    is_active = models.SmallIntegerField(blank=True, null=True)
    countryiso = models.CharField(db_column='countryISO', max_length=255, blank=True, null=True)  
    fail_checks = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lf_proxy_profiles'


class LfShowingGeo(models.Model):
    id = models.BigAutoField(primary_key=True)
    group_id = models.BigIntegerField()
    country = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'lf_showing_geo'


class LfShowingTimes(models.Model):
    id = models.BigAutoField(primary_key=True)
    group_id = models.BigIntegerField()
    hour = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'lf_showing_times'


class LfUsersOptions(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    credits = models.DecimalField(max_digits=16, decimal_places=5)
    workmode = models.SmallIntegerField()
    type = models.SmallIntegerField()
    experience = models.BigIntegerField() 
    env = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lf_users_options'


class LfUsersStats(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    visits = models.IntegerField()
    credits = models.DecimalField(max_digits=16, decimal_places=5)
    experience = models.IntegerField()
    date = models.BigIntegerField()
    data = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lf_users_stats'