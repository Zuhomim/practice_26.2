from django.db import models

from config import settings

NULLABLE = {'null': True, 'blank': True}


class Course(models.Model):
    name = models.CharField(max_length=60, verbose_name='Название')
    preview = models.ImageField(upload_to='materials/courses/', verbose_name='Превью', **NULLABLE)
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    price = models.PositiveIntegerField(verbose_name="Цена", **NULLABLE)

    def __str__(self):
        return f'{self.name} ({self.description[:30]})'

    def get_subscribed_users(self):
        subscription_user = [subscription.user for subscription in self.subscriptions.all() if
                             subscription.user is not None]
        return subscription_user


class Lesson(models.Model):
    name = models.CharField(max_length=60, verbose_name='Название')
    description = models.CharField(max_length=100, verbose_name='Описание', **NULLABLE)
    preview = models.ImageField(upload_to='materials/lessons/', verbose_name='Превью', **NULLABLE)
    video_link = models.URLField(verbose_name='Ссылка на видео', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.name} ({self.course.name})'


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="subscriptions", verbose_name="Курс")
    is_active = models.BooleanField(default=True, verbose_name="Активность подписки")

    def __str__(self):
        return f'{self.user} ({self.course.name})'


class CoursePayment(models.Model):
    name = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Продукт")
    price = models.PositiveIntegerField(verbose_name="Цена", **NULLABLE)
    link = models.URLField(max_length=200, verbose_name="Ссылка оплаты", **NULLABLE)
    session_id = models.CharField(max_length=255, verbose_name="Идентификатор", **NULLABLE)

    def __str__(self):
        return f'{self.session_id}'
