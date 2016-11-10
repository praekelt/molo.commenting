# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-23 12:29
from __future__ import unicode_literals

from django.db import migrations
from django.core.management.sql import emit_post_migrate_signal


class Migration(migrations.Migration):
    def add_commenting_permissions_to_groups(apps, schema_editor):
        db_alias = schema_editor.connection.alias
        try:
            # Django 1.9
            emit_post_migrate_signal(2, False, db_alias)
        except TypeError:
            # Django < 1.9
            try:
                # Django 1.8
                emit_post_migrate_signal(2, False, 'default', db_alias)
            except TypeError:  # Django < 1.8
                emit_post_migrate_signal([], 2, False, 'default', db_alias)

        Group = apps.get_model('auth.Group')
        Permission = apps.get_model('auth.Permission')
        GroupPagePermission = apps.get_model('wagtailcore.GroupPagePermission')


        # Create groups

        access_admin = Permission.objects.get(codename='access_admin')

        # <- Moderator ->
        moderator_group = Group.objects.get(name='Moderators')

        add_cannedresponse = Permission.objects.get(
            codename='add_cannedresponse')
        change_cannedresponse = Permission.objects.get(
            codename='change_cannedresponse')
        delete_cannedresponse = Permission.objects.get(
            codename='delete_cannedresponse')
        add_molocomment = Permission.objects.get(
            codename='add_molocomment')
        delete_molocomment = Permission.objects.get(
            codename='delete_molocomment')
        moderator_group.permissions.add(
            add_cannedresponse, delete_cannedresponse,
            change_cannedresponse, add_molocomment, delete_molocomment)

        # <- Comment Moderator ->
        comment_moderator_group, _created = Group.objects.get_or_create(name='Comment Moderator')
        comment_moderator_group.permissions.all().delete()
        comment_moderator_group.permissions.add(access_admin)
        change_user = Permission.objects.get(
            codename='change_user')
        add_cannedresponse = Permission.objects.get(
            codename='add_cannedresponse')
        add_molocomment = Permission.objects.get(
            codename='add_molocomment')
        delete_molocomment = Permission.objects.get(
            codename='delete_molocomment')
        comment_moderator_group.permissions.add(change_user,
            add_cannedresponse, add_molocomment, delete_molocomment)

        # <- Expert ->
        expert_group, _created = Group.objects.get_or_create(name='Expert')
        expert_group.permissions.all().delete()
        expert_group.permissions.add(access_admin)
        add_molocomment = Permission.objects.get(codename='add_molocomment')
        expert_group.permissions.add(add_molocomment)

    dependencies = [
        ('commenting', '0004_auto_20160713_0221'),
        ('core', '0047_add_core_permissions_to_groups'),
        ('contenttypes', '__latest__'),
        ('sites', '__latest__'),
    ]

    operations = [
        migrations.RunPython(add_commenting_permissions_to_groups),
    ]