# Generated by Django 4.2 on 2023-04-24 15:17

import app.custom_field
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="District",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name="Municipality",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=30)),
                (
                    "district",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.district"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Province",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=255, null=True)),
                ("status", models.CharField(blank=True, max_length=30, null=True)),
                ("donor", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "executing_agency",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("implementing_partner", models.TextField(blank=True, null=True)),
                (
                    "counterpart_ministry",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "type_of_assistance",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "budget_type",
                    models.CharField(
                        choices=[
                            ("Off Budget", "Off Budget"),
                            ("On Budget", "On Budget"),
                        ],
                        default="Off Budget",
                        max_length=15,
                    ),
                ),
                ("is_humanitarian", app.custom_field.YesNoBooleanField()),
                ("sector", models.CharField(max_length=200)),
                (
                    "commitments",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("agreement_date", models.DateField(blank=True, null=True)),
                (
                    "disbursement",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("disbursement_date", models.DateField(blank=True, null=True)),
                (
                    "municipality",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.municipality",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="district",
            name="province",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="app.province"
            ),
        ),
    ]
