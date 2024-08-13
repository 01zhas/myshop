from django.db import models
from django.contrib.auth.models import User, Group

class Category(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey('self', null=True, blank=True, related_name="children", on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"Корзина {self.user.username}"
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Товары в корзине"
        verbose_name_plural = "Товары в корзинах"

    def __str__(self):
        return f"{self.quantity}: {self.product.name}"
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('ordered', 'Заказан'),
        ('shipped', 'Отправлен'),
        ('received', 'Получен'),
        ('canceled', 'Отменен'),
        ('returned', 'Возращен'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='order')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ordered')
    payment_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f'Заказ номер {self.id} пользователя {self.user.username}'
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Запись заказов"
        verbose_name_plural = "Записи заказов"

    def __str__(self):
        return f"{self.quantity}: {self.product.name}"
    
class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    valid_until = models.DateTimeField()

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"

    def __str__(self):
        return self.code
    
class GroupDiscount(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Группа клиента"
        verbose_name_plural = "Группа клиентов"

    def __str__ (self):
        return self.group.name