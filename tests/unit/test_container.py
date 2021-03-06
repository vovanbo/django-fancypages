import mock

from django.test import TestCase
from django.template import RequestContext
from django.contrib.auth.models import User

from fancypages.test import factories
from fancypages.models import Container
from fancypages.renderers import ContainerRenderer


class TestAContainer(TestCase):

    def setUp(self):
        super(TestAContainer, self).setUp()
        self.request = mock.Mock()
        self.request.META = {}
        self.request_context = RequestContext(self.request, {})

    def test_can_be_retrieved_by_name(self):
        container = Container.objects.create(name='some-container')
        retrieved_container = Container.get_container_by_name(container.name)
        self.assertEquals(container.id, retrieved_container.id)

    def test_renders_block_selection_correctly(self):
        self.request.fp_edit_mode = True

        ctn_id = 15
        container = factories.ContainerFactory.build(id=ctn_id)
        html = ContainerRenderer(container, self.request_context).render()
        self.assertIn(
            'data-target="#block_selection_modal"'.format(container.uuid),
            html)
        self.assertIn('data-container-id="{}"'.format(container.uuid), html)


class TestAnObjectContainer(TestCase):

    def test_can_be_retrieved_by_name(self):
        user = User.objects.create(username='testuser')
        container = Container.objects.create(
            name='some-container', page_object=user)

        retrieved_container = Container.get_container_by_name(
            container.name, user)
        self.assertEquals(container.id, retrieved_container.id)
