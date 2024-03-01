# from django.db import models
# from database.models import User
# from django.contrib.auth.models import AbstractUser
# from django.db import models
# # Create your models here.


# # get user by id
# def get_user_by_id(user_id: int):
#     try:
#         user = User.objects.get(user_id=user_id)
#         return user
#     except User.DoesNotExist:
#         return None


# # get user by intra name
# def get_user_by_intra_name(intra_name: str):
#     try:
#         user = User.objects.get(intra_name=intra_name)
#         return user
#     except User.DoesNotExist:
#         return None


# # get all games played by user
# def get_all_games_played_by_user(user_id: int):
#     try:
#         user = User.objects.get(user_id=user_id)
#         games = user.game_set.all()
#         return games
#     except User.DoesNotExist:
#         return None


# # set new user
# # def set_new_user(intra_name: str, name: str, surname: str, email: str, password_hash: str, wallet_id: str):
# def set_new_user(intra_name: str, name: str, surname: str, email: str, password_hash: str):
#     try:
#         # user = User.objects.create(intra_name=intra_name, name=name, surname=surname, email=email, password_hash=password_hash, wallet_id=wallet_id)
#         user = User.objects.create(intra_name=intra_name, name=name, surname=surname, email=email, password_hash=password_hash)
#         return user
#     except Exception:
#         return None


# # update user
# def update_user(user_id: int, intra_name: str, name: str, surname: str, email: str, password_hash: str):
#     try:
#         user = User.objects.get(user_id=user_id)
#         user.intra_name = intra_name
#         user.name = name
#         user.surname = surname
#         user.email = email
#         user.password_hash = password_hash
#         # user.birthdate = birthdate
#         user.save()
#         return user
#     except User.DoesNotExist:
#         return None
