from django.test import TestCase
from team.models import Team
from team.tests.factories import TeamFactory
from user.tests.factories import CustomUserFactory

class TeamModelTests(TestCase):

    def test_create_a_team_successfully_in_database(self):
        # Arrange
        current_objects = Team.objects.count()
        # Act
        team = TeamFactory()
        db_team = Team.objects.get(id=team.id)
        # Assert
        self.assertEqual(team, db_team)
        self.assertEqual(team.name, db_team.name)
        self.assertEqual(Team.objects.count(), current_objects + 1)


    def test_update_a_team_successfully_in_database(self):
        # Arrange
        team = TeamFactory()
        team_db = Team.objects.get(id=team.id)
        new_name = 'another name'
        # Act
        team_db.name = 'another name'
        team_db.save()
        # Arrange
        team_after_update = Team.objects.get(id=team.id)
        self.assertEqual(team_after_update.name, new_name)



