from typing import List
import strawberry
import strawberry.django
# from django.contrib.auth.models import User

from apps.book.models import Book,Favorite
from apps.review.models import Review

@strawberry.django.type(Review)
class ReviewType:
    rating:int
    review_text:str
    user:str

@strawberry.django.type(Book)
class BookType:
    id:int 
    title: str
    author: str
    description: str
    created_by : str
    is_active: bool
    reviews:List[ReviewType] 
    
    # @strawberry.field
    # @sync_to_async
    # def created_by(self) -> str:
    #     return self.created_by.username

@strawberry.django.input(Book)
class BookInput:
    title:str
    author:str
    description:str
    is_active : bool


@strawberry.django.type(Favorite)
class FavoriteType:
    book:str


@strawberry.django.input(Favorite)
class FavoriteInput:
    book:str
