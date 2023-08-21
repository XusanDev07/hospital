from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager
from django.db import models


class CusManeger(UserManager):
    def create_user(self, phone, email=None, password=None, is_staff=False, is_active=True, is_superuser=False,
                    **extra_fields):
        user = self.model(
            phone=phone,
            email=email,
            password=password,
            is_staff=is_staff,
            is_active=is_active,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, email=None,
                         password=None, **extra_fields):
        return self.create_user(phone, email, password=password, is_staff=True, is_superuser=True, **extra_fields)


class Professions(models.Model):
    name = models.CharField(max_length=123)

    class Meta:
        verbose_name_plural = '5. Kasblar'
        verbose_name = "Kasb"

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=123)

    class Meta:
        verbose_name_plural = '6. Lavozimlar'
        verbose_name = "Lavozim"

    def __str__(self):
        return self.name


class UserDoctor(AbstractBaseUser, PermissionsMixin):
    name = models.CharField('Ismi', max_length=125)
    surname = models.CharField('Familyasi', max_length=125)
    phone = models.CharField('Telefon raqami', max_length=125, unique=True)
    img = models.ImageField('Rasm', upload_to='docs', null=True)
    prof = models.ForeignKey(Professions, on_delete=models.CASCADE, related_name="profession")
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="position")
    info = models.TextField("Shifokor haqida ma'lumot", null=True)
    email = models.EmailField('Elektron pochtasi', null=True)
    gender = models.BooleanField("Jinsi", default=True)
    user_type = models.SmallIntegerField('Foydalanuvchi statusi', choices=[
        (1, 'Owner'),
        (2, 'Adminastirator'),
        (3, 'Doktor'),
        (4, 'Mijozlar'),
    ], default=4)
    new = models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CusManeger()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email', 'user_type']

    class Meta:
        verbose_name_plural = '1. Doktorlar'
        verbose_name = "Doktor"

    def save(self, *args, **kwargs):
        if self.user_type == 4:
            self.position_id = 2

        return super(UserDoctor, self).save(*args, **kwargs)


class DocTime(models.Model):
    date = models.DateField()
    time = models.TimeField()
    doc = models.ForeignKey(UserDoctor, on_delete=models.CASCADE, related_name='doc_time',
                            limit_choices_to={'user_type': 3})
    free = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = '4. Vaqt sarrhisobi'
        verbose_name = "Vaqt"

# class DocRating(models.Model):
# user=models.ForeignKey(User,on_delete=models.SET_NULL)
# doc=models.ForeignKey(Doctor,on_delete=models.CASCADE)
# star=models.SmallIntegerField(choices=[
#   (1, "★"),
#  (2, "★★"),
# (3, "★★★"),
# (4, "★★★★"),
# (5, "★★★★★"),

# ]
