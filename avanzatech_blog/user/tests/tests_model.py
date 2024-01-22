from django.test import TestCase
from user.tests.factories import CustomUserFactory
from team.tests.factories import TeamFactory
from user.models import CustomUser
from team.models import Team
from user.constants import SUPER_USER_TEAM_NAME

class UserModelTests(TestCase):

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
        team = Team.objects.create(name='team_test')
        example_user = {
            "email": "test@test.com",
            "password": "test_password",
            "team": team
        }
        # Act
        user = CustomUser.objects.create_user(**example_user)
        # Arrange
        self.assertNotEqual(user.password, example_user['password'])

    def test_create_super_user_successfully_in_database(self):
        # Arrange
        example_user = {
            "email": "test@test.com",
            "password": "test_password",
        }
        # Act
        user = CustomUser.objects.create_superuser(**example_user)
        # Arrange
        self.assertNotEqual(user.password, example_user['password'])
        self.assertEqual(user.email, example_user['email'])
        self.assertEqual(user.team.name, SUPER_USER_TEAM_NAME)
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
        amount_users_in_team = 10
        team_instance = TeamFactory()
        CustomUserFactory.create_batch(amount_users_in_team, team=team_instance)
        CustomUserFactory.create_batch(5)
        # Act
        users_by_team = CustomUser.objects.filter(team_id=team_instance.id).count()
        # Assert
        self.assertEqual(users_by_team, amount_users_in_team)

    
