import json

from django.urls import reverse
from django.test import TestCase
from django.conf import settings

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Todo

from channels.testing import ChannelsLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

class TodoConsumerTestCase(ChannelsLiveServerTestCase):
    serve_static = True

    def _open_new_window(self):
        self.driver.execute_script('window.open("about:blank", "_blank");')
        self.driver.switch_to_window(self.driver.window_handles[-1])

    def _close_all_new_windows(self):
        while len(self.driver.window_handles) > 1:
            self.driver.switch_to_window(self.driver.window_handles[-1])
            self.driver.execute_script('window.close();')
        if len(self.driver.window_handles) == 1:
            self.driver.switch_to_window(self.driver.window_handles[0])

    def _switch_to_window(self, window_index):
        self.driver.switch_to_window(self.driver.window_handles[window_index])

    def _post_message(self, message):
        ActionChains(self.driver).send_keys(message + '\n').perform()

    def _enter_todo_service(self):
        self.driver.get(self.live_server_url + '/ws/todos/')
        WebDriverWait(self.driver,2).until(self.driver.current_url)

    def _open_new_window(self):
        self.driver.execute_script('window.open("about:blank", "_blank");')
        self.driver.switch_to_window(self.driver.window_handles[-1])

    def _post_message(self, message):
        ActionChains(self.driver).send_keys(message + '\n').perform()


class DetailTodoAPIViewTestCase(APITestCase):
    def setUp(self):
        self.sample_todo = Todo.objects.create(title="t1", content="c1")
        self.url = reverse('todos:detail', kwargs={'pk' : self.sample_todo.id})
        self.url_with_invalid_id = reverse('todos:detail', kwargs={'pk' : 99})

    def test_can_get_todo_return_correct_id(self):
        """GET /api/todos/{pk} returns a todo with detail"""
        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue('id' in json.loads(response.content))

    def test_cannot_access_todo_if_invalid_id(self):
        """GET, DELETE, /api/todos/{pk} returns 404 NOT_FOUND for invalid id"""
        test_methods = [ self.client.get, self.client.delete ]
        for test_method in test_methods:
            response = test_method(self.url_with_invalid_id)
            self.assertTrue(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_can_delete_todo_return_deleted_id(self):
        """DELETE /api/todos/{pk} returns a 204 NO_CONTENT, deleted todo detail"""
        response = self.client.delete(self.url)
        self.assertTrue(status.HTTP_204_NO_CONTENT, response.content)

    def test_can_todo_object_update(self):
        """PUT /api/todos/{pk} returns a 200 OK, update todo detail"""
        update_data = {'title' : 'updated title', 'content' : 'updated content'}
        response = self.client.put(self.url, update_data)
        response_data = json.loads(response.content)
        todo = Todo.objects.get(id=self.sample_todo.id)
        self.assertTrue(response_data.get('title'), todo.title)

    def test_can_todo_object_partial_update(self):
        """PATCH /api/todos/{pk} returns a 200 OK, partial update todo detail"""
        response = self.client.patch(self.url, {'is_done' : True})
        response_data = json.loads(response.content)
        todo = Todo.objects.get(id=self.sample_todo.id)
        self.assertTrue(response_data.get('is_done'), todo.is_done)

    def test_cannot_update_todo_if_title_is_null(self):
        """PATCH /api/todos/{pk} return a 400 BAD_REQUES, title's can not be updated to null"""
        response = self.client.patch(self.url, {'title' : ''})
        self.assertTrue(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertTrue('title' in json.loads(response.content))

    # Do test position
    def test_can_update_index(self):
        """PATCH /api/todos/{pk} returns a 200 OK, index update"""
        to_change_index = 2
        Todo.objects.create(title='t2', content='c2') # This Object index is 1
        Todo.objects.create(title='t3', content='c3') # This Object index is 2
        response = self.client.patch(self.url, {'index' : to_change_index})
        response_data = json.loads(response.content)
        expected_id = Todo.objects.get(index=to_change_index).id
        self.assertEqual(response_data['id'], expected_id)


class ListTodoAPIViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('todos:list')
        self.sample_data = {\
                'title' : 'sample title', \
                'content' : 'sample content' \
            }

    def test_can_get_todo_list(self):
        """GET /api/todos/ returns list of todos"""
        Todo.objects.create(title='t1', content='c1')
        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(len(json.loads(response.content)))

    def test_can_get_todo_list_without_todo_objects(self):
        """GET /api/todos/ returns a empty list"""
        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertFalse(len(json.loads(response.content)))

    def test_request_todo_list_with_wrong_method(self):
        """NOT GET(other method) /api/todos/ returns 405 METHOD_NOT_ALLOWED for wrong method"""
        response = self.client.delete(self.url)
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)

    def test_can_create_todo(self):
        """POST /api/todos returns 201 CREATED for a valid todo data"""
        response = self.client.post(self.url, data=self.sample_data)
        created_todo = json.loads(response.content)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(Todo.objects.filter(id=created_todo['id']).exists())

    def test_cannot_create_todo_if_todo_count_is_over_limit(self):
        """POST /api/todos return 406 NOT_ACCEPTABLE If len(todos.all()) of a has reached the limit"""
        limit_count = settings.LIMITED_TODO_COUNT
        [Todo.objects.create(title="t"+str(i)) \
                for i in range(limit_count)]
        response = self.client.post(self.url, data=self.sample_data)
        self.assertEqual(status.HTTP_406_NOT_ACCEPTABLE, response.status_code)

    def test_cannot_create_todo_if_title_field_null(self):
        """POST /api/todos return 400 BAD_REQUEST for title field is null"""
        sample_data_without_title = self.sample_data.copy()
        del sample_data_without_title['title']
        response = self.client.post(self.url, data=sample_data_without_title)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_can_increase_index_when_create_new_todo(self):
        """POST /api/todos returns a 200 OK, create a new todo with index parameter"""
        data = self.sample_data.copy()
        data['index'] = 1
        response = self.client.post(self.url, data=data)
        self.new_todo = Todo.objects.create(title="t1", content="c1")
        todo_count = Todo.objects.count()
        self.assertEqual(todo_count, self.new_todo.index+1)

    def test_can_insert_first_index_with_change_other_todo_index(self):
        """POST /api/todos returns a 200 OK, create a new todo with index is 0"""
        Todo.objects.create(title="hello", content="okay", index=0)
        data = self.sample_data.copy()
        data['index'] = 0
        response = self.client.post(self.url, data=data)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['index'], Todo.objects.get(id=response_data['id']).index)

    def test_can_create_todo_if_index_that_existing_range(self):
        """POST /api/todos/ returns a 200 OK, create a new todo with index within existing range"""
        Todo.objects.create(title='t1', content='c1') # This Object index is 0
        Todo.objects.create(title='t2', content='c2') # This Object index is 1
        Todo.objects.create(title='t3', content='c3') # This Object index is 2
        to_change_index = 1
        data = self.sample_data.copy()
        data['index'] = to_change_index
        response = self.client.post(self.url, data=data)
        new_todo_created_by_user = Todo.objects.get(id=json.loads(response.content)['id'])
        expected_id = Todo.objects.get(index=to_change_index).id
        self.assertEqual(new_todo_created_by_user.id, expected_id)

    def test_can_create_todo_if_index_that_exceeds_existing_range(self):
        """POST /api/todos/ returns a 200 OK, create a new todo with index that exceeds the existing range"""
        data = self.sample_data.copy()
        data['index'] = 300
        response = self.client.post(self.url, data=data)
        response_data = json.loads(response.content)
        self.assertTrue('index' in response_data)
        self.assertEqual(response_data['index'], Todo.objects.get(id=response_data['id']).index)
