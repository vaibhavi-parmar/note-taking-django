from django.db import models
from django.utils.timezone import now
import uuid

# Create your models here.

class NotesUser(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name")
    username = models.CharField(max_length=100, unique=True, verbose_name="Username")
    email = models.EmailField(unique=True, verbose_name="Email")
    contact_no = models.CharField(max_length=15, unique=True, verbose_name="Contact No")
    password = models.CharField(max_length=100, verbose_name="Password")

    def __str__(self):
        return f'{self.username}'
    
    class Meta:
        verbose_name = "Notes User"
        verbose_name_plural = "Notes Users"

class Notes(models.Model):
    user = models.ForeignKey(NotesUser, on_delete=models.CASCADE, verbose_name="Username")
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name="Title")
    content = models.TextField(verbose_name="Content")
    created_at = models.DateTimeField(default=now)
    is_pinned = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    in_bin = models.BooleanField(default=False)
    share_uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, null=False)

    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"

    def __str__(self):
        return f'{self.username} - {self.title}'
