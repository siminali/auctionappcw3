from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import datetime
from datetime import date






class QandA(models.Model):
    item_id = models.IntegerField()
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    
    def to_dict(self):
        return{
            'id': self.id,
            'item_id':self.item_id,
            'question': self.question,
            'answer': self.answer,

        }


class Item(models.Model):
    
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    start_price = models.DecimalField(max_digits = 5,decimal_places = 2)
    bid_time_end = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    highest_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    highest_bidder = models.CharField(max_length=255, default="")
    owner_name = models.TextField(blank=True)
    owner = models.ForeignKey("User", related_name='owns', on_delete=models.CASCADE, null=True)
    question = models.ForeignKey("QandA", related_name='belongs_to', on_delete=models.CASCADE, null=True)

    def to_dict(self):
        return{
            'id': self.id,
            'title': self.title,
            'start_price': self.start_price,
            'bid_time_end': self.bid_time_end,
            'highest_bid': self.highest_bid,
            'highest_bidder': self.highest_bidder,
            'owner_name': self.owner_name,
            'image': self.image.url if self.image else None,
            #'question': self.question.item_id,
        }




class User(AbstractUser):
    '''
    Our User models is a sub-class of Django's AbstractUser
    So we can make use of Django's authentication system
    '''

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=254)
    dob = models.DateField(default=timezone.now)
    profile_pic = models.ImageField(upload_to='images', default='paulo.jpg', blank=True, null=True)
    bids = models.ManyToManyField(Item)

    profile = models.OneToOneField(
        to='Profile',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    following = models.ManyToManyField(
        to='self',
        blank=True,
        symmetrical=False,
        related_name='followers',
    )
    messages = models.ManyToManyField(
        to='self',
        blank=True,
        symmetrical=False,
        through='Message',
        related_name='related_to'
    )

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def to_dict(self):
        return {
            'username': self.username,
            'email':self.email,
            #'dob': self.dob,

            'profile': self.profile.to_dict() if self.profile else None,
            'messages': [message.to_dict() for message in self.messages]
        }

    @property
    def messages(self):
        '''Messages sent and received by this user'''

        return (self.sent.all() | self.received.all()).order_by("-time")

    def messages_with(self, view_user):
        '''Messages visible between two users'''

        # public messages that 'view_user' has received
        m1 = Message.objects.filter(recip=view_user, public=True)
        # public messages that 'view_user' has sent
        m2 = Message.objects.filter(sender=view_user, public=True)
        # messages 'user' sent 'view_user'
        m3 = Message.objects.filter(sender=self, recip=view_user)
        # messages 'view_user' sent 'user'
        m4 = Message.objects.filter(sender=view_user, recip=self)
        # union of the four query sets
        return m1.union(m2, m3, m4).order_by('-time')

    @property
    def following_count(self):
        '''Count of following'''

        return self.following.count()

    @property
    def follower_count(self):
        '''Count of followers'''

        return User.objects.filter(following__id=self.id).count()


class Profile(models.Model):
    '''
    A Profile is simply a bit of text and/or image
    that a Member might or might not have, hence the
    OneToOne relationship in Member with null=True
    '''

    text = models.CharField(max_length=4096)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return f"{self.text} ({self.member_check})"

    def to_dict(self):
        return {
            'text': self.text,
            'image': self.image.url if self.image else None,
        }

    @property
    def has_member(self):
        '''True if this profile belongs to a Member'''

        return hasattr(self, 'member') and self.member is not None

    @property
    def member_check(self):
        '''Either the username of the Member, or NONE'''

        return str(self.member) if self.has_member else 'NONE'


class Message(models.Model):
    '''
    The Message models is the 'through' model for
    the 'message' ManyToMany relationship between Members
    '''

    sender = models.ForeignKey(
        to=User,
        related_name='sent',
        on_delete=models.CASCADE
    )
    recip = models.ForeignKey(
        to=User,
        related_name='received',
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=4096)
    public = models.BooleanField(default=True)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"From {self.sender} to {self.recip}"

    def to_dict(self):
        return {
            'id': self.id,
            'sender': self.sender.username,
            'recip': self.recip.username,
            'text': self.text,
            'public': self.public,
            'time': self.time.strftime("%Y-%d-%mT%H:%M"),
        }




    


