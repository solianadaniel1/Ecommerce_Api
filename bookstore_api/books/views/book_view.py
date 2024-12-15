from rest_framework import generics
from books.models.book import Book
from books.serializers import BookSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

# List and Create Books
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

# Retrieve, Update, and Delete a Book
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
er_class = BookSerializer
