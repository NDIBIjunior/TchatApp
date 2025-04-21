from django.db import models

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat()
        }

class Message(models.Model):
    sender = models.CharField(max_length=255)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} to {self.recipient}: {self.content[:20]}..."  # Display first 20 characters of content
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def to_dict(self):
        return {
            'username': self.sender,
            'content': self.content,
            'timestamp': self.timestamp.isoformat()
        }


    def get_sender(self):
        # Return the sender of the message
        return self.sender
    def get_recipient(self):
        # Return the recipient of the message
        return self.recipient
    def get_content(self):
        # Return the content of the message
        return self.content
    def get_timestamp(self):
        # Return the timestamp of the message
        return self.timestamp