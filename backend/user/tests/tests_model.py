from django.test import TestCase
from user.tests.factories import CustomUserFactory
from team.tests.factories import TeamFactory
from user.models import CustomUser
from team.models import Team
from team.tests.factories import TeamFactory
from team.constants import DEFAULT_TEAM_NAME
from psycopg.errors import NotNullViolation

class UserModelTests(TestCase):

    def setUp(self):
        self.team = TeamFactory(name=DEFAULT_TEAM_NAME)
    
    def test_create_blogger_user_successfully_in_database(self):
        # Arrange
        current_objects = CustomUser.objects.count()
        # Act
        user = CustomUserFactory()
        db_user = CustomUser.objects.get(email=user.email)
        # Assert
        self.assertEqual(user, db_user)
        self.assertEqual(CustomUser.objects.count(), current_objects + 1)

    def test_raw_password_is_not_stored_in_database(self):
        # Arrange
        team = TeamFactory()
        raw_password = "raw_password"
        # Act
        user = CustomUserFactory(password=raw_password)
        db_password = CustomUser.objects.get(id=user.id).password
        # Arrange
        self.assertNotEqual(db_password, raw_password)

    def test_create_super_user_successfully_in_database(self):
        # Arrange
        example_user = {
            "email": "test@test.com",
            "password": "test_password",
            "first_name": "test",
            "last_name": "test",
        }
        # Act
        user = CustomUser.objects.create_superuser(**example_user)
        # Arrange
        self.assertNotEqual(user.password, example_user['password'])
        self.assertEqual(user.email, example_user['email'])
        self.assertEqual(user.team.name, DEFAULT_TEAM_NAME)
        self.assertIs(user.is_staff, True)
        self.assertIs(user.is_superuser, True)

    def test_create_admin_user_successfully_in_database(self):
        # Arrange
        user = CustomUserFactory()
        db_user = CustomUser.objects.get(email=user.email)
        db_user.is_staff = True
        # Act
        db_user.save()
        # Assert
        db_user_after_update = CustomUser.objects.get(email=user.email)
        self.assertIs(db_user_after_update.is_staff, True)


    def test_parameters_by_default_are_created_successfully(self):
        # Arrange
        user = CustomUserFactory()
        # Act
        db_user = CustomUser.objects.get(email=user.email)
        # Arrange
        self.assertIs(db_user.is_active, True)
        self.assertIs(db_user.is_staff, False)
        self.assertIs(db_user.is_superuser, False)
        
    def test_users_by_team_can_be_listed(self):
        # Arrange
        amount_users_in_team = 5
        CustomUserFactory.create_batch(amount_users_in_team, team=self.team)
        CustomUserFactory.create_batch(5)
        # Act
        users_by_team = CustomUser.objects.filter(team=self.team).count()
        # Assert
        self.assertEqual(users_by_team, 5)

    def test_insert_an_user_without_an_email_should_raise_an_error(self):
            # Arrange
            team = TeamFactory()
            data = {
                "email": "",
                "password": "test_password",
                "first_name": "test",
                "last_name": "test",
            }
            # Act & Assert
            with self.assertRaises(ValueError):
                CustomUser.objects.create_user(**data)

    def test_insert_an_user_without_password_should_raise_an_error(self):
            # Arrange
            team = TeamFactory()
            data = {
                "email": "test@test.com",
                "first_name": "test",
                "last_name": "test",
            }
            # Act & Assert
            with self.assertRaises(ValueError):
                CustomUser.objects.create_user(**data)

    def test_create_super_user_without_email_should_raise_an_error(self):
        # Arrange
        example_user = {
            "email": "",
            "password": "test_password",
            "first_name": "test",
            "last_name": "test",
        }
        # Act & Arrange
        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(**example_user)

    def test_create_super_user_without_password_should_raise_an_error(self):
        # Arrange
        example_user = {
            "email": "test@test.com",
            "first_name": "test",
            "last_name": "test",
        }
        # Act & Arrange
        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(**example_user)


    def test_create_a_user_without_firstname_should_raise_an_error(self):
        # Arrange
        example_user = {
            "email": "example@mail.com",
            "password": "test_password",
            "last_name": "example"
        }
        # Act & Arrange
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(**example_user)

    def test_create_a_super_user_without_first_name_should_raise_an_error(self):
        # Arrange
        example_user = {
            "email": "example@mail.com",
            "password": "test_password",
            "last_name": "example"
        }
        # Act & Arrange
        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(**example_user)

    def test_create_a_user_without_last_name_should_raise_an_error(self):
        # Arrange
        example_user = {
            "email": "example@mail.com",
            "password": "test_password",
            "first_name": "example"
        }
        # Act & Arrange
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(**example_user)

    def test_create_a_super_user_without_last_name_should_raise_an_error(self):
        # Arrange
        example_user = {
            "email": "example@mail.com",
            "password": "test_password",
            "first_name": "example"
        }
        # Act & Arrange
        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(**example_user)


