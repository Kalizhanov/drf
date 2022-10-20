# Generated by Django 4.1.1 on 2022-10-18 05:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basket',
            name='products',
        ),
        migrations.CreateModel(
            name='BasketItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('basket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.basket')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.item')),
            ],
        ),
    ]
