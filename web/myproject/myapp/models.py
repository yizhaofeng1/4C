# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

#如要启用数据库功能请将下面注释删除掉
# class Shj(models.Model):
#     name = models.CharField(primary_key=True, max_length=100)
#     appearance = models.CharField(max_length=500, blank=True, null=True)
#     original_habitat = models.CharField(max_length=1000, blank=True, null=True)
#     modern_location = models.CharField(max_length=1000, blank=True, null=True)
#     source_excerpt = models.CharField(max_length=1000, blank=True, null=True)
#     source_translation = models.CharField(max_length=1000, blank=True, null=True)
#     abilities = models.CharField(max_length=500, blank=True, null=True)
#     symbolism = models.CharField(max_length=1000, blank=True, null=True)
#     category = models.CharField(max_length=30, blank=True, null=True)
#     mountain_location = models.CharField(max_length=10, blank=True, null=True)
#     chapter = models.CharField(max_length=20, blank=True, null=True)
#     def __str__(self):
#         return self.name
