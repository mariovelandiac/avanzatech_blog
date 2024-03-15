import os
from permission.tests.factories import PermissionFactory
from category.tests.factories import CategoryFactory
from team.tests.factories import TeamFactory
from team.constants import DEFAULT_TEAM_NAME
from user.models import CustomUser
from user.tests.factories import CustomUserFactory
from post.tests.factories import PostFactory, PostCategoryPermissionFactory
from common.utils import create_custom_category_permissions_handler
from common.constants import AccessCategory, AccessPermission

def check_and_create_superuser():
    # Get superuser credentials from environment variables
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@admin.com')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'adminpassword')

    # Check if superuser already exists
    if not CustomUser.objects.filter(is_superuser=True).exists():
        # Create superuser
        print("Creating superuser...")
        CustomUser.objects.create_superuser(
            email=email,
            password=password,
            first_name="Admin",
            last_name="Admin"
        )

def create_post_permissions(posts):
    # Create just read public posts
    print("-- Creating just read public posts...")
    public_just_read_posts = posts[:8]
    category_permission = {
        AccessCategory.PUBLIC: AccessPermission.READ,
        AccessCategory.AUTHENTICATED: AccessPermission.NO_PERMISSION,
        AccessCategory.TEAM: AccessPermission.NO_PERMISSION,
        AccessCategory.AUTHOR: AccessPermission.NO_PERMISSION
    }
    PostCategoryPermissionFactory.create_batch(public_just_read_posts, category_permission=category_permission)
    # Create edit public posts
    print("-- Creating edit public posts...")
    public_read_write_posts = posts[8:16]
    category_permission = {
        AccessCategory.PUBLIC: AccessPermission.EDIT,
        AccessCategory.AUTHENTICATED: AccessPermission.NO_PERMISSION,
        AccessCategory.TEAM: AccessPermission.NO_PERMISSION,
        AccessCategory.AUTHOR: AccessPermission.NO_PERMISSION
    }
    PostCategoryPermissionFactory.create_batch(public_read_write_posts, category_permission=category_permission)
    # Create just read authenticated posts
    print("-- Creating just read authenticated posts...")
    authenticated_just_read_posts = posts[16:24]
    category_permission = {
        AccessCategory.PUBLIC: AccessPermission.NO_PERMISSION,
        AccessCategory.AUTHENTICATED: AccessPermission.READ,
        AccessCategory.TEAM: AccessPermission.NO_PERMISSION,
        AccessCategory.AUTHOR: AccessPermission.NO_PERMISSION
    }
    PostCategoryPermissionFactory.create_batch(authenticated_just_read_posts, category_permission=category_permission)
    # Create edit authenticated posts
    print("-- Creating edit authenticated posts...")
    authenticated_read_write_posts = posts[24:32]
    category_permission = {
        AccessCategory.PUBLIC: AccessPermission.NO_PERMISSION,
        AccessCategory.AUTHENTICATED: AccessPermission.EDIT,
        AccessCategory.TEAM: AccessPermission.NO_PERMISSION,
        AccessCategory.AUTHOR: AccessPermission.NO_PERMISSION
    }
    PostCategoryPermissionFactory.create_batch(authenticated_read_write_posts, category_permission=category_permission)
    # Create just read team posts
    print("-- Creating just read team posts...")
    team_just_read_posts = posts[32:40]
    category_permission = {
        AccessCategory.PUBLIC: AccessPermission.NO_PERMISSION,
        AccessCategory.AUTHENTICATED: AccessPermission.NO_PERMISSION,
        AccessCategory.TEAM: AccessPermission.READ,
        AccessCategory.AUTHOR: AccessPermission.NO_PERMISSION
    }
    PostCategoryPermissionFactory.create_batch(team_just_read_posts, category_permission=category_permission)
    # Create edit team posts
    print("-- Creating edit team posts...")
    team_read_write_posts = posts[40:48]
    category_permission = {
        AccessCategory.PUBLIC: AccessPermission.NO_PERMISSION,
        AccessCategory.AUTHENTICATED: AccessPermission.NO_PERMISSION,
        AccessCategory.TEAM: AccessPermission.EDIT,
        AccessCategory.AUTHOR: AccessPermission.NO_PERMISSION
    }
    PostCategoryPermissionFactory.create_batch(team_read_write_posts, category_permission=category_permission)
    # Create just read author posts
    print("-- Creating just read author posts...")
    author_just_read_posts = posts[48:56]
    category_permission = {
        AccessCategory.PUBLIC: AccessPermission.NO_PERMISSION,
        AccessCategory.AUTHENTICATED: AccessPermission.NO_PERMISSION,
        AccessCategory.TEAM: AccessPermission.NO_PERMISSION,
        AccessCategory.AUTHOR: AccessPermission.READ
    }
    PostCategoryPermissionFactory.create_batch(author_just_read_posts, category_permission=category_permission)
    # Create edit author posts
    print("-- Creating edit author posts...")
    author_read_write_posts = posts[56:]
    category_permission = {
        AccessCategory.PUBLIC: AccessPermission.NO_PERMISSION,
        AccessCategory.AUTHENTICATED: AccessPermission.NO_PERMISSION,
        AccessCategory.TEAM: AccessPermission.NO_PERMISSION,
        AccessCategory.AUTHOR: AccessPermission.EDIT
    }
    PostCategoryPermissionFactory.create_batch(author_read_write_posts, category_permission=category_permission)


def create_posts(users, team_a, team_b, default_team):
    posts = []
    for i in range(64):
        if i < 8:
            author = users[0]
        elif i < 16:
            author = users[1]
        elif i < 24:
            author = users[2]
        elif i < 32:
            author = users[3]
        elif i < 40:
            author = users[4]
        elif i < 48:
            author = users[5]
        elif i < 56:
            author = users[6]
        else:
            author = users[7]
        post = PostFactory(user=author)
        posts.append(post)
    return posts

def create_users(team_a, team_b, default_team):
    users = []
    for i in range(8):
        if i < 2:
            team = default_team
        elif i < 4:
            team = team_a
        elif i < 6:
            team = team_b
        else:
            team = default_team
        user = CustomUserFactory(team=team)
        users.append(user)
    return users

def fill_database():
    # Create permissions
    print("Creating permissions...")
    permissions = PermissionFactory.create_batch()
    # Create Categories
    print("Creating categories...")
    categories = CategoryFactory.create_batch()
    # Create Teams
    print("Creating teams...")
    default_team=TeamFactory(name=DEFAULT_TEAM_NAME)
    team_a = TeamFactory(name="Alpha Team")
    team_b = TeamFactory(name="Beta Team")
    # Create Users
    print("Creating users...")
    users = create_users(team_a, team_b, default_team)
    # Create Posts
    print("Creating posts...")
    posts = create_posts(users, team_a, team_b, default_team)
    # Create Post Permissions
    print("Creating post permissions...")
    create_post_permissions(posts)
    print("Database filled.")


fill_database()
check_and_create_superuser()