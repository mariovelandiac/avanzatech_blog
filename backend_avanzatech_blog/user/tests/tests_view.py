from rest_framework.test import APITestCase
from user.tests.factories import CustomUserFactory
from rest_framework.reverse import reverse
from rest_framework import status
from django.contrib.sessions.backends.db import SessionStore

class UserLogInViewTests(APITestCase):

    def test_an_existing_user_is_authenticated_and_log_in_successfully(self):
        # Arrange
        raw_password = "test_password"
        user_db = CustomUserFactory(password=raw_password)
        credentials = {
            "username": user_db.email,
            "password": raw_password
        }
        url = reverse('login')  
        # Act
        response = self.client.post(url, credentials)
        user_id_in_request = self.client.session.get('_auth_user_id')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(user_db.id, int(user_id_in_request))
        self.assertIsNotNone(response.cookies)
        self.assertIsNotNone(response.cookies['sessionid'])
        self.assertIsNotNone(response.cookies['csrftoken'])
        self.assertIsInstance(self.client.session, SessionStore)
        self.assertRedirects(response, reverse('success_page'))

    def test_an_non_existing_user_can_not_log_in(self):
        # Arrange
        raw_password = "test_password"
        user = CustomUserFactory.build()
        credentials = {
            "username": user.email,
            "password": raw_password
        }
        url = reverse('login')
        # Act
        response = self.client.post(url, credentials)
        user_id_in_request = self.client.session.get('_auth_user_id')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(user_id_in_request)


    def test_get_request_returns_status_code_200_if_user_is_unauthenticated(self):
        # Arrange
        url = reverse('login')
        # Act
        response = self.client.get(url)
        csrf = response.cookies.get('csrftoken')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(csrf)

    def test_put_request_returns_status_code_200_if_user_is_unauthenticated(self):
        # Arrange
        url = reverse('login')
        data = {
            "username": "user@username.com",
            "password": "raw_password"
        }
        # Act
        response = self.client.put(url, data)
        csrf = response.cookies.get('csrftoken')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(csrf)

    def test_patch_request_returns_status_code_200_if_user_is_unauthenticated(self):
        # Arrange
        url = reverse('login')
        data = {
            "password": "raw_password"
        }
        # Act
        response = self.client.patch(url, data)
        csrf = response.cookies.get('csrftoken')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(csrf)

    def test_delete_request_returns_status_code_200_if_user_is_unauthenticated(self):
        # Arrange
        url = reverse('login')
        # Act
        response = self.client.delete(url)
        csrf = response.cookies.get('csrftoken')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(csrf)


    def test_a_logged_in_user_can_log_in_again_and_its_session_id_is_the_same(self):
        # Arrange
        raw_password = "test_password"
        user_db = CustomUserFactory(password=raw_password)
        credentials = {
            "username": user_db.email,
            "password": raw_password
        }
        url = reverse('login')
        # Act
        response_1 = self.client.post(url, credentials)
        sessionid_1 = response_1.cookies.get('sessionid').value
        response_2 = self.client.post(url, credentials)
        sessionid_2  = response_2.cookies.get('sessionid').value
        # Assert
        self.assertEqual(sessionid_1, sessionid_2)
        self.assertIsNotNone(sessionid_1)
        self.assertIsNotNone(sessionid_2)
        self.assertEqual(response_1.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response_2.status_code, status.HTTP_302_FOUND)
        
    def test_a_logged_in_user_try_to_login_with_other_valid_credentials_and_session_id_is_updated(self):
        # Arrange
        raw_password = "test_password"
        user_db_1 = CustomUserFactory(password=raw_password)
        credentials_1 = {
            "username": user_db_1.email,
            "password": raw_password
        }
        user_db_2 = CustomUserFactory(password=raw_password)
        credentials_2 = {
            "username": user_db_2.email,
            "password": raw_password
        }
        url = reverse('login')
        # Act
        response_1 = self.client.post(url, credentials_1)
        sessionid_1 = response_1.cookies.get('sessionid')
        response_2 = self.client.post(url, credentials_2)
        sessionid_2  = response_2.cookies.get('sessionid')
        # Assert
        self.assertNotEqual(sessionid_1, sessionid_2)
        self.assertIsNotNone(sessionid_1)
        self.assertIsNotNone(sessionid_2)
        self.assertEqual(response_1.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response_2.status_code, status.HTTP_302_FOUND)


class UserLogOutViewTests(APITestCase):

    def setUp(self):
        user_db = CustomUserFactory()
        self.client.force_login(user_db)
        self.user_id = self.client.session.get("_auth_user_id")

    def test_an_unauthorized_user_access_log_out_an_then_is_redirected(self):
        # Arrange
        self.client.logout()
        # Act
        url = reverse('logout')
        response = self.client.post(url)
        session_id = response.cookies.get('sessionid')
        user_id_after_logout = self.client.session.get("_auth_user_id")
        # Assert
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertIsNone(session_id)
        self.assertIsNone(user_id_after_logout) 
        
    
    def test_an_existing_user_is_authenticated_and_then_log_out_successfully_with_post_method(self):
        # Arrange
        url = reverse('logout')
        # Act
        response = self.client.post(url)
        session_id = response.cookies.get('sessionid').value
        user_id_after_logout = self.client.session.get("_auth_user_id")
        # Assert
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(session_id, "")
        self.assertIsNone(user_id_after_logout)
        
    def test_an_existing_user_is_authenticated_and_then_log_out_successfully_with_get_method(self):
        # Arrange
        url = reverse('logout')
        # Act
        response = self.client.get(url)
        session_id = response.cookies.get('sessionid').value
        user_id_after_logout = self.client.session.get("_auth_user_id")
        # Assert
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(session_id, "")
        self.assertIsNone(user_id_after_logout)    
        

    def test_an_existing_user_is_authenticated_and_then_log_out_successfully_with_put_method(self):
        # Arrange
        url = reverse('logout')
        # Act
        response = self.client.put(url)
        session_id = response.cookies.get('sessionid').value
        user_id_after_logout = self.client.session.get("_auth_user_id")
        # Assert
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(session_id, "")
        self.assertIsNone(user_id_after_logout) 


    def test_an_existing_user_is_authenticated_and_then_log_out_successfully_with_patch_method(self):
        # Arrange
        url = reverse('logout')
        # Act
        response = self.client.patch(url)
        session_id = response.cookies.get('sessionid').value
        user_id_after_logout = self.client.session.get("_auth_user_id")
        # Assert
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(session_id, "")
        self.assertIsNone(user_id_after_logout) 


    def test_an_existing_user_is_authenticated_and_then_log_out_successfully_with_delete_method(self):
        # Arrange
        url = reverse('logout')
        # Act
        response = self.client.delete(url)
        session_id = response.cookies.get('sessionid').value
        user_id_after_logout = self.client.session.get("_auth_user_id")
        # Assert
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(session_id, "")
        self.assertIsNone(user_id_after_logout) 
        
