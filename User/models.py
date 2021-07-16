from django.db import models

#Types of inputes
class InputType(models.Model):
    name = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return self.name
#Saparetor model
class Separator(models.Model):
    name = models.CharField(max_length=50)
    prefix = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return self.name

#String Character model
class StringCharacter(models.Model):
    name = models.CharField(max_length=50)
    prefix = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return self.name

#Columns for Schema model
class SchemaColumn(models.Model):
    columnName = models.CharField(max_length = 150)
    type = models.ForeignKey(InputType, on_delete=models.CASCADE)
    from_int = models.IntegerField(blank=True, null=True)
    to_int = models.IntegerField(blank=True, null=True)
    sentence = models.IntegerField(blank=True, null=True)
    order = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return self.columnName

#Schema model
class Schema(models.Model):
    schemaTitle = models.CharField(max_length = 150)
    separator = models.ForeignKey(Separator, on_delete=models.CASCADE)
    stringCharacter = models.ForeignKey(StringCharacter,on_delete=models.CASCADE)
    schemaColumns = models.ManyToManyField(SchemaColumn, blank=True)
    user_id = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return self.schemaTitle

class Generated_csv(models.Model):
    schema_id = models.ForeignKey(Schema, to_field='id',  on_delete=models.CASCADE)
    row = models.IntegerField()
    status = models.CharField(max_length=50)
    path = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.schema_id)

