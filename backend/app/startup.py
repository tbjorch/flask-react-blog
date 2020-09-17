# Standard library
from typing import List

# Internal modules
from app.models import Role, User, Blogpost
from app.controllers.AuthController import AuthController


auth = AuthController.get_instance()


def create_user(username: str, password, roles: List[Role]) -> None:
    user: User = User(username, auth.create_pw_hash(password))
    if roles:
        for role in roles:
            user.roles.append(role)
    user.save()


def create_blogpost(title: str, body: str, uid: int) -> None:
    blogpost: Blogpost = Blogpost(title, body, uid)
    blogpost.save()


# Create base roles
admin_role: Role = Role("ADMIN", "Global administrator of site")
admin_role.save()
user_role: Role = Role("USER", "Regular blog user")
user_role.save()


# Create dummy users
create_user("admin", "password", [admin_role, user_role])
create_user("John Doe", "password", [user_role])
create_user("Reggie67", "password", [user_role])
create_user("Jane Dane", "password", [admin_role, user_role])
create_user("ArnoldStronk", "password", [user_role])
create_user("Jessica", "password", [user_role])


# Create dummy blogposts
welcome_post = "I just want to start off by welcoming you to this most awesome page. This is just a little hobby project to allow me to build an object oriented MVC style backend application, and a react frontend application. This is just a demo site to show a little bit of what i can do."
lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
lorem2 = "Accumsan sit amet nulla facilisi morbi tempus iaculis. Dolor sit amet consectetur adipiscing elit pellentesque habitant. A erat nam at lectus urna duis. Purus non enim praesent elementum facilisis leo. Eu tincidunt tortor aliquam nulla facilisi cras fermentum odio eu. Amet justo donec enim diam vulputate ut pharetra. Duis at tellus at urna condimentum. Arcu cursus vitae congue mauris rhoncus aenean vel elit. Tortor pretium viverra suspendisse potenti nullam ac tortor vitae. Lacus sed turpis tincidunt id. Tellus id interdum velit laoreet id donec ultrices tincidunt arcu. Tortor dignissim convallis aenean et tortor at. Mauris commodo quis imperdiet massa. Duis tristique sollicitudin nibh sit amet commodo nulla facilisi nullam. Turpis massa sed elementum tempus egestas sed sed. Et netus et malesuada fames ac turpis egestas integer eget. Quam viverra orci sagittis eu. Risus nullam eget felis eget nunc lobortis. Aliquam id diam maecenas ultricies mi eget mauris pharetra. Viverra aliquet eget sit amet tellus cras adipiscing."
create_blogpost("Welcome to the Blog of all blogs!", welcome_post, 1)
create_blogpost("Sooo, what have we been up to?", lorem, 2)
create_blogpost("You really never thought that this would happen", lorem2, 3)
