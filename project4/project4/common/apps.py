from django.apps import AppConfig


#让settings中的app里面加入common
class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'common'
