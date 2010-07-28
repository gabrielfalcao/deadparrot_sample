#!/usr/bin/env python
# -*- coding: utf-8 -*-
import bolacha
from lxml import etree
from deadparrot import models
from deadparrot.serialization.plugins.base import Serializer
from deadparrot.models.managers import ObjectsManager
from deadparrot.models.managers import ModelManager

url = 'http://twitter.com/status/user_timeline/%s.xml'

class TwitterObjectsManager(ObjectsManager):
    def from_user(self, username):
        http = bolacha.Bolacha()
        headers, xml = http.get(url % username)

        StatusSet = self.model.Set()
        return StatusSet.deserialize(xml, 'twitter')

class TwitterManager(ModelManager):
    manager = TwitterObjectsManager

class TwitterApiSerializer(Serializer):
    format = 'twitter'

    @classmethod
    def deserialize(cls, xml):
        if isinstance(xml, basestring):
            is_list = True
            try:
                tree = etree.fromstring(xml)
            except Exception, e:
                print xml
                raise e
        else:
            is_list = False
            tree = xml

        if is_list:
            items = tree.iterchildren()
            ret = {
                tree.tag: [cls.deserialize(item) for item in items]
            }
        else:
            d2 = {}
            d1 = {
                tree.tag: d2
            }
            for tag in tree.iterchildren():
                text = tag.text
                if isinstance(text, basestring) and text.strip():
                    d2[tag.tag] = text.strip()
                else:
                    d2[tag.tag] = cls.deserialize(tag)

            ret = d1

        return ret

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    screen_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    profile_image_url = models.URLField(verify_exists=False)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

class Status(models.Model):
    created_at = models.DateTimeField(format="%a %b %d %H:%M:%S +0000 %Y")
    id = models.IntegerField(primary_key=True)
    text = models.TextField()
    user = models.ForeignKey(User)
    objects = TwitterManager()


    class Meta:
        verbose_name = 'status'
        verbose_name_plural = 'statuses'
