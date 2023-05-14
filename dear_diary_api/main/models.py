from django.db import models
from django.utils import timezone

# Create your models here.
class userLogin(models.Model):
    name=models.CharField(max_length=200)
    userid=models.TextField(primary_key=True)
    pswd=models.CharField(max_length=30)
    def __str__(self):
        return self.userid
    
class MasterTable(models.Model):
    userid = models.ForeignKey(userLogin,on_delete=models.CASCADE,default=0)
    page = models.CharField('Page',max_length=50)
    data = models.TextField() 
    def __str__(self):
        return self.userid.userid
    
class Session(models.Model):
    user=models.ForeignKey(userLogin, on_delete=models.CASCADE)
    session_key=models.CharField(max_length=50)
    last_activity=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}({self.session_key})"
    
    @classmethod
    def create(cls, user, session_key):
        active_sessions=Session.objects.filter(user=user)
        for session in active_sessions:
            if (timezone.now()-session.last_activity).total_seconds()<3600:
                return None
        new_session=cls(user=user, session_key=session_key)
        new_session.save()
        return new_session
    
    

    