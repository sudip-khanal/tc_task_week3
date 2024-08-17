from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from PyPDF2 import PdfReader  # Use PyPDF2 to read PDF content

from apps.book.models import Book,Favorite
from apps.review.models import Review
from apps.review.serializer import ReviewSerializer
from apps.book.cache import top_book_cache
from apps.book.filters import BookFilter
from apps.book.serializers import (
    BookSerializer,
    FavoriteSerializer,
    FavoriteBookSerializer,
    BookPdfSerializer
    )
from ollamaservice.summery_service import summarizer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.filter(is_active=True)
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        reviews = Review.objects.filter(book=instance)
        review_serializer = ReviewSerializer(reviews, many=True)
        # Calculate the average rating for the book
        average_rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
        
        response_data = serializer.data
        response_data['average_rating'] = average_rating
        response_data['reviews'] = review_serializer.data
        return Response(response_data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.created_by != request.user:

            return Response({"msg": "You dont have premission to delete this book."},
                    status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_destroy(instance)
        return Response({ "msg": "book deleted."},
                    status=status.HTTP_200_OK)
    
    def perform_destroy(self, instance):
        instance.is_active=False
        instance.save(update_fields=['is_active'])

    @action(
            detail=True, 
            methods=['post'], 
            permission_classes=[IsAuthenticated]
            )
    def favorite(self, request, pk=None):
        book = self.get_object()
        data = {'book': book.id, 'user': request.user.id}
        serializer = FavoriteSerializer(
                data=data,
                context={'request': request
                })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(
            detail=True, 
            methods=['delete'], 
            permission_classes=[IsAuthenticated]
            )
    def unfavorite(self, request, pk=None):
        book = self.get_object()
        user = request.user
        favorite = Favorite.objects.filter(book=book, user=user)
        if favorite.exists():
            favorite.delete()
            return Response({
                'msg': 'Book removed from favorites successfully.'}, 
                status=status.HTTP_200_OK)
        return Response({
            'msg': 'You have not favorited this book.'}, 
            status=status.HTTP_400_BAD_REQUEST)
    
    
    @action(
            detail=False, 
            methods=['get'],
            permission_classes=[IsAuthenticated]
            )
    def my_favorites(self, request):  
        favorites = Favorite.objects.filter(user=request.user)  
        serializer = FavoriteBookSerializer(favorites, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    


    # @action(detail=True,methods=['get'],serializer_class = BookPdfSerializer)
    # def get_pdf(self, request, pk=None):
    #     book=BookPdfSerializer()
    #     pdf_reader = PdfReader(book.pdf_file)
    #     text_content = ""
    #     for page in pdf_reader.pages:
    #         text_content += page.extract_text()

    #     # Return the response with the extracted text and PDF URL
    #     return Response({
    #         'book_title': book.title,
    #         'pdf_url': book.pdf_file.url,
    #         'extracted_text': text_content,
    #     })

    @action(detail=True, methods=['get'], serializer_class=BookPdfSerializer)
    def get_pdf(self, request, pk=None):
        # Fetch the correct book instance
        book = self.get_object()

        # Initialize PdfReader with the actual book's PDF file
        pdf_reader = PdfReader(book.pdf_file)

        # Extract text content from the PDF
        text_content = ""
        for page in pdf_reader.pages:
            text_content += page.extract_text()

        summary = summarizer(text_content)

        # Return the response with the extracted text and PDF URL
        return Response({
            'book_title': book.title,
            'pdf_url': book.pdf_file.url,
            'extracted_text': text_content,
            'summary':summary
        })

    @action(detail=False)
    def get_summery(self, request, pk=None):
        # try:
        #     book = self.get_object()  # Fetch the book instance
        # except Book.DoesNotExist:
        #     return Response({"error": "Book not found"}, status=404)
        # book=BookPdfSerializer()
        # # Extract text from the PDF file
        # pdf_reader = PdfReader(book.pdf_file)
        text_content = """      We have configured our templates and added the first page to our project, a static homepage.
                                We also added tests which should always be included with new code changes. Some developers
                                prefer a method called Test-Driven Development where they write the tests first and then the
                                code. Personally I prefer to write the tests immediately after which is what we’ll do here.
                                Both approaches work, the key thing is to be rigorous with your testing. Django projects quickly
                                grow in size where it’s impossible to remember all the working pieces in your head. And if you
                                are working on a team, it is a nightmare to work on an untested codebase. Who knows what will
                                break?
                                In the next chapter we’ll add user registration to our project: log in, log out, and sign up.
                                
                                """
        # for page in pdf_reader.pages:
        #     text_content += page.extract_text()

        # Generate the summary using the `invoke` function
        summary = summarizer(text_content)

        # Return the response with the extracted text, summary, and PDF URL
        return Response({
            # 'book_title': book.title,
            # 'pdf_url': book.pdf_file.url,
            'extracted_text': text_content,
            'summary': summary
        })

  # Here you would pass the text_content to the Ollama model
        # book_summary= summazier(text_content)
        # For now, we'll simulate this by returning the text.

        # Return the response with the text content and the PDF URL

    @action(detail=True, methods=['get'], serializer_class=BookPdfSerializer)
    def pdfs(self, request, pk=None):
        try:
            # Retrieve the actual book instance
            book = self.get_object()
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=404)

        # Extract text from the PDF file
        pdf_path = book.pdf_file.path  # This gives you the absolute path to the file
        text_content = ""

        try:
            # Open the PDF file
            with open(pdf_path, 'rb') as pdf_file:
                pdf_reader = PdfReader(pdf_file)
                for page in pdf_reader.pages:
                    text_content += page.extract_text()

        except FileNotFoundError:
            return Response({"error": "File not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

        # Generate a summary (This is a placeholder for now)
        summary = "This is where the Ollama-generated summary will be."

        # Return the response with the extracted text and PDF URL
        return Response({
            'book_title': book.title,
            'pdf_url': book.pdf_file.url,  # This gives you the URL to access the file
            'extracted_text': text_content,
            'summary': summary
        })


    # Get the books with the highest average rating, limiting to top 10
    def get_top_rated_books(self):
        return Review.objects.values('book').annotate(avg_rating=Avg('rating')).order_by('-avg_rating')[:10]
    
    @action(
            detail=False,
            methods=['get'],
            url_path='top-10-rated'
            )
    def top_rated(self, request):
        cache_key = 'top_10_rated_books'
        top_rated_books = top_book_cache(cache_key, self.get_top_rated_books)

        if top_rated_books:
            top_rated_books_list = []
            for book_info in top_rated_books:
                book_id = book_info['book']
                average_rating = book_info['avg_rating']
                book = Book.objects.get(id=book_id)

                serializer = self.get_serializer(book)
                reviews = Review.objects.filter(book=book)
                review_serializer = ReviewSerializer(reviews, many=True)

                book_data = serializer.data
                book_data['average_rating'] = average_rating
                book_data['reviews'] = review_serializer.data

                top_rated_books_list.append(book_data)
            return Response(top_rated_books_list)
        return Response({"detail": "No reviews found."}, status=status.HTTP_404_NOT_FOUND)





    # def get(self, request, pk, format=None):
    #     try:
    #         # Fetch the book by ID
    #         book = Book.objects.get(pk=pk)
    #     except Book.DoesNotExist:
    #         raise NotFound("Book not found.")

    #     # Extract text from the PDF file
    #     pdf_reader = PdfReader(book.pdf_file)
    #     text_content = ""
    #     for page in pdf_reader.pages:
    #         text_content += page.extract_text()

    #     # Here you would pass the text_content to the Ollama model

    #     # For now, we'll simulate this by returning the text.

    #     # Return the response with the text content and the PDF URL
    #     return Response({
    #         'book_title': book.title,
    #         'pdf_url': book.pdf_file.url,
    #         'extracted_text': text_content,
    #         # Placeholder for the Ollama summary (to be implemented later)
    #         'summary': "This is where the Ollama-generated summary will be."
    #     })
