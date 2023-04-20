from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Friend_Request)
admin.site.register(Photo)
admin.site.register(Chat_History)
admin.site.register(Message)