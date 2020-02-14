# Generated by Django 3.0.2 on 2020-02-11 10:34

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('fname', models.CharField(max_length=150)),
                ('lname', models.CharField(max_length=150)),
                ('dob', models.DateField(null=True)),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Prefer not say')], max_length=2)),
                ('password', models.CharField(max_length=150, validators=[django.core.validators.MinLengthValidator(5)])),
                ('email', models.EmailField(max_length=150, unique=True)),
                ('phone', models.CharField(max_length=15, unique=True)),
                ('pfp', models.ImageField(upload_to='')),
                ('date_joined', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('brand_name', models.CharField(max_length=150)),
                ('brand_url', models.URLField()),
                ('brand_logo', models.ImageField(upload_to='')),
                ('org_name', models.CharField(max_length=150)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'customers',
            },
        ),
        migrations.CreateModel(
            name='CPRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('S', 'Owner'), ('A', 'Admin'), ('O', 'Operator'), ('R', 'Restricted')], max_length=2)),
                ('is_active', models.BooleanField(default=True)),
                ('cust', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'cprelationship',
            },
        ),
        migrations.CreateModel(
            name='PropertyTokens',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.CharField(max_length=16)),
                ('psecret', models.CharField(max_length=150)),
                ('generated_by', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
            ],
            options={
                'db_table': 'property_tokens',
            },
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.CharField(max_length=16, unique=True)),
                ('ptype', models.CharField(choices=[('A', 'APP'), ('W', 'Website')], max_length=5)),
                ('domain', models.CharField(max_length=200)),
                ('verified', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('properties', models.ManyToManyField(through='customer.CPRelationship', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'property',
            },
        ),
        migrations.AddField(
            model_name='cprelationship',
            name='prop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.Property'),
        ),
    ]
