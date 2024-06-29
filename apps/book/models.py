from django.db import models
from django.contrib.auth.models import User

#Book Model
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Method to perform a soft delete by marking the book as inactive
    def soft_delete(self):
        self.is_active = False
        self.save()
        
    def __str__(self):
        return self.title

# Model representing a user's favorite book
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    # Ensure a user can not favorite the same book more than once
    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.username}'s favorite: {self.book.title}"

