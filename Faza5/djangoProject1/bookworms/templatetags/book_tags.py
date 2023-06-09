from django import template

register = template.Library()

@register.filter
def chunk_books(books, chunk_size):
    chunked_books = [books[i:i+chunk_size] for i in range(0, len(books), chunk_size)]
    return chunked_books