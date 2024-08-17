import typing
import strawberry
import strawberry.django
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from typing import Union,Annotated
from asgiref.sync import sync_to_async
from strawberry.types import Info
from strawberry.permission import BasePermission

from apps.review.models import Review
from apps.book.models import Book,Favorite
from apps.book.types import BookType,BookInput,FavoriteType

       
class IsAuthenticated(BasePermission):
    """
    Permission class to check if the user is authenticated
    """
    message = "User is not authenticated"
    @sync_to_async
    def has_permission(self, source: typing.Any, info: strawberry.Info, **kwargs) -> bool:
        return  info.context.request.user.is_authenticated


class IsOwner(BasePermission):
    """
    Permission class to check if the user is the owner of a book
    """
    message = "You do not have permission to perform this action"
    @sync_to_async
    def has_permission(self, source: typing.Any, info: strawberry.Info, **kwargs) -> bool:
        book_id = kwargs.get('id')
        if not book_id:
                return False
            
        user=info.context.request.user
        book = Book.objects.get(id=book_id)
        return book.created_by == user
      
    

@strawberry.django.type(User)
class UserType:
    username: str | None
    email: str | None

@strawberry.input
class UserInput:
    username: str
    password: str

@strawberry.type
class LoginSuccess:
    user: UserType

@strawberry.type
class LoginError:
    message: str

@strawberry.type
class LogoutSuccess:
    message: str

@strawberry.type
class LogoutError:
    message: str

LoginResult = Annotated[
    Union[LoginSuccess, LoginError], strawberry.union("LoginResult")
]

LogoutResult = Annotated[
    Union[LogoutSuccess, LogoutError], strawberry.union("LogoutResult")
]

@strawberry.type
class Query:
    """
    Query type for retrieving data.
    """
    @strawberry.field
    @sync_to_async
    def current_user(self, info: strawberry.Info) -> UserType:
        """
        Returns the currently authenticated user.
        """
        user =  info.context.request.user
        return UserType(username=user.username, email=user.email)


    @strawberry.field
    @sync_to_async
    def books(self, info: strawberry.Info) -> typing.List[BookType]:
        """
        Returns a list of active books.
        """
        books =list(Book.objects.filter(is_active=True))
        return books

    
    @strawberry.field
    @sync_to_async
    def book(self, info: Info, id: strawberry.ID) -> BookType:
        """
        Returns a single book by it's id with reviews if it is active.
        """
        book = Book.objects.get(id=id)
        if not book.is_active:
            raise Exception("Book is not active")
        reviews = list(Review.objects.filter(book=book))
        return BookType(
            id=book.id,
            title=book.title,
            author=book.author,
            created_by=book.created_by,
            is_active=book.is_active,
            description=book.description,
            reviews=reviews
        )
    
    @strawberry.field(permission_classes=[IsAuthenticated])
    @sync_to_async
    def myfavourite_books(self,info:Info)->typing.List[FavoriteType]:
        """
        Returns a list of favorite books for the currently authenticated user.
        """
        user = info.context.request.user
        favorites= list(Favorite.objects.filter(user=user.id))
        return favorites


@strawberry.type
class Mutation:
    @strawberry.mutation
    @sync_to_async
    def login(self,info, username: str, password: str) -> LoginResult:
        """
        Authenticates a user and logs them in.
        """
        request=info.context.request
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)
            return LoginSuccess(user=User(username=username))
        return LoginError(message="Invalid credentials")

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    @sync_to_async
    def logout(self, info) -> LogoutResult:
        """
        Logs out the currently authenticated user.
        """
        request = info.context.request
        logout(request)
        return LogoutSuccess(message="Logged out successfully")

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    @sync_to_async
    def add_book(self, info, input: BookInput) -> BookType:
        """
        Adds a new book with the provided input.
        """
        user =info.context.request.user
        book = Book.objects.create(created_by=user, **input.__dict__)
        return book


    @strawberry.mutation(permission_classes=[IsAuthenticated,IsOwner])
    @sync_to_async
    def update_book(self,info,id: strawberry.ID,input:BookInput)-> BookType:
        """
        Updates an existing book by its id with the provided input.
        """
        book = Book.objects.get(id=id)
        for attr, value in input.__dict__.items():
            setattr(book, attr, value)
        book.save()
        return book
        
    @strawberry.mutation(permission_classes=[IsAuthenticated,IsOwner])
    @sync_to_async
    def delete_book(self, info, id: strawberry.ID) -> bool:
        """
        Marks a book as inactive by its id.
        """
        book = Book.objects.get(id=id)
        book.is_active = False
        book.save(update_fields=['is_active']) 
        return True   
    
        
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    @sync_to_async
    def add_favourite(self,id: strawberry.ID, info)-> FavoriteType:
        """
        Adds a book to the currently authenticated user's favorites.
        """
        user =info.context.request.user
        book =  Book.objects.get(id=id)
        favourtes = Favorite.objects.create(user=user,book=book)
        return favourtes
        
schema = strawberry.Schema(query=Query, mutation=Mutation)


