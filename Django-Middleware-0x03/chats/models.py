import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """Custom User model that extends Django's AbstractUser"""

    user_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name=_("User ID")
    )

    first_name = models.CharField(_("first name"), max_length=150, blank=False)
    last_name = models.CharField(_("last name"), max_length=150, blank=False)

    email = models.EmailField(_("email address"), unique=True, blank=False)

    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Phone Number"))

    ROLE_CHOICES = (
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='guest',
        blank=False,
        verbose_name=_("Role")
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ['-created_at']


class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(
        User,
        related_name='conversations', # Allows `user.conversations.all()`
        verbose_name=_("Participants")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    class Meta:
        verbose_name = _("Conversation")
        verbose_name_plural = _("Conversations")
        ordering = ['-created_at'] # Order by most recent conversation

    def __str__(self):
        participant_emails = ", ".join([user.email for user in self.participants.all()])
        return f"Conversation {self.conversation_id} with: {participant_emails}"
    


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name=_("Sender")
    )

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name=_("Conversation")
    )

    message_body = models.TextField(blank=False, verbose_name=_("Message Body"))
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Sent At"))

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
        ordering = ['sent_at']

    def __str__(self):
        return f"Message from {self.sender.email} in Conversation {self.conversation.conversation_id}"