#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase
from django.conf import settings
from tweet.models import Status
from datetime import datetime
class TestTwitterDeserializer(TestCase):
    def setUp(self):
        self.xml = open(settings.LOCAL_FILE('tweet/dilmabr.xml')).read()

    def test_can_deserialize_status(self):
        StatusSet = Status.Set()
        statuses = StatusSet.deserialize(self.xml, 'twitter')

        status = statuses[0]

        self.assertEquals(
            status.text,
            u'Dia do Agricultor. Um grande abraço a todos aqueles que retiram da terra seu sustento e os alimentos que chegam à mesa dos brasileiros.'
        )
        self.assertEquals(
            status.created_at,
            datetime(2010, 7, 28, 14, 10, 35)
        )

    def test_can_deserialize_status_with_user(self):
        StatusSet = Status.Set()
        statuses = StatusSet.deserialize(self.xml, 'twitter')

        status = statuses[1]

        self.assertEquals(
            status.text,
            u'@ibere40 @Vilma400 @juliaarruda vamos nos ver aí amanhã, amigos!'
        )
        self.assertEquals(
            status.created_at,
            datetime(2010, 7, 27, 17, 57, 50)
        )

        self.assertEquals(
            status.user.name,
            'Dilma Rousseff'
        )
        self.assertEquals(
            status.user.screen_name,
            'dilmabr'
        )
        self.assertEquals(
            status.user.profile_image_url,
            'http://a3.twimg.com/profile_images/1075356403/dilma-twitter_normal.jpg'
        )
