from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.middleware.csrf import get_token
from .models import ContactMessage
from .serializers import ContactMessageSerializer
from django.core.mail import send_mail
from django.conf import settings

class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    http_method_names = ['get', 'post','head','options']  # Allow GET and POST

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Send email notification
            subject = f"New Freelancing Form Submission: {serializer.data['name']}"
            message = (
                f"New message from {serializer.data['name']} ({serializer.data['email']}):\n\n"
                f"Phone Number: {serializer.data['phone_number']}\n"
                f"Subject: {serializer.data['subject']}\n"
                f"Message: {serializer.data['message']}\n"
                f"Budget: {serializer.data['budget'] or 'Not specified'}"
            )
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            return Response(
                {"message": "Thank you for your message! I'll get back to you soon."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        return Response({"detail": "Use POST to submit a contact message."})

@api_view(['GET'])
def get_csrf_token(request):
    return Response({'csrfToken': get_token(request)})