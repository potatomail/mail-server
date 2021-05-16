from django.contrib.auth.models import User
from django.db import models


class SecondaryPw(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    secondary = models.CharField(max_length=254)

# class pomail_user(models.Model):
#     user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="emails")
#     sender = models.ForeignKey("User", on_delete=models.PROTECT, related_name="emails_sent")
#     recipients = models.ManyToManyField("User", related_name="emails_received")
#     subject = models.CharField(max_length=254)
#     body = models.TextField(blank=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     read = models.BooleanField(default=False)
#     archived = models.BooleanField(default=False) 

#     def serialize(self):
#         return {
#             "id": self.id,
#             "sender": self.sender.email,
#             "recipients": [user.email for user in self.recipients.all()],
#             "subject": self.subject,
#             "body": self.body,
#             "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
#             "read": self.read,
#             "archived": self.archived
#         }

