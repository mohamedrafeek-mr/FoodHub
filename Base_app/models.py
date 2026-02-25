from django.db import models

class ContactMessage(models.Model):
    """Contact form submissions"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message from {self.name} - {self.subject}"


class RestaurantInfo(models.Model):
    """Restaurant information and settings"""
    name = models.CharField(max_length=100, default='Restaurant Name')
    description = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    
    # Razorpay settings
    razorpay_key_id = models.CharField(max_length=100, blank=True)
    razorpay_key_secret = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Restaurant Info"
    
    def __str__(self):
        return self.name
