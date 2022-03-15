# Generated by Django 4.0.2 on 2022-03-15 03:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('NameOnCard', models.CharField(blank=True, max_length=200, null=True)),
                ('Address', models.CharField(blank=True, max_length=500, null=True)),
                ('creditcardnumber', models.CharField(blank=True, max_length=500, null=True)),
                ('city', models.CharField(blank=True, max_length=300, null=True)),
                ('cardExpdate', models.CharField(blank=True, max_length=300, null=True)),
                ('state', models.CharField(blank=True, max_length=300, null=True)),
                ('zip', models.CharField(blank=True, max_length=300, null=True)),
                ('cvv', models.CharField(blank=True, max_length=300, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customer')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('image', models.ImageField(upload_to='images/')),
                ('description', models.CharField(blank=True, max_length=3000, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.seller')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, null=True)),
                ('price', models.CharField(blank=True, max_length=100, null=True)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='ecomApp.checkout')),
            ],
        ),
        migrations.CreateModel(
            name='MyRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], default=0, max_length=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomApp.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customer')),
            ],
        ),
    ]
