from django.contrib import admin
from User.models import *

# Register your models here.

admin.site.register(Separator)
admin.site.register(StringCharacter)
admin.site.register(SchemaColumn)
admin.site.register(Schema)
admin.site.register(InputType)
admin.site.register(Generated_csv)