from django.db import models






class PublishStateOptions(models.TextChoices):
        # CONSTANT = DB_VALUE, USER_DISPLAY
        PUBLISH = 'PU','Publish' 
        DRAFT = 'DR','Draft'
        # UNLISTED  = 'UN','Unlisted'
        # PRIVATE = 'PR','Private'