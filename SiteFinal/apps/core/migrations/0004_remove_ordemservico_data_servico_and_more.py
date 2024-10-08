# Generated by Django 5.0.7 on 2024-08-28 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_produto_descricao'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordemservico',
            name='data_servico',
        ),
        migrations.RemoveField(
            model_name='servico',
            name='produto',
        ),
        migrations.AddField(
            model_name='ordemservico',
            name='data_finalizacao',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='ordemservico',
            name='data_inicio',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='ordemservico',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
