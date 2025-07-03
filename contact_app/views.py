from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.middleware.csrf import get_token
from .models import ContactMessage
from .serializers import ContactMessageSerializer
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        logger.info(f"Received request: method={request.method}, path={request.path}")
        logger.info(f"Request headers: {dict(request.META)}")
        logger.info(f"Request data: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            logger.info(f"Serializer valid, validated data: {serializer.validated_data}")
            try:
                instance = serializer.save()
                logger.info(f"Data saved successfully: {serializer.data}, instance ID: {instance.id}")
            except Exception as e:
                logger.error(f"Database save failed: {str(e)}")
                return Response(
                    {"error": f"Database save failed: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            subject = f"New Freelancing Form Submission: {serializer.data['name']}"
            message = (
                f"New message from {serializer.data['name']} ({serializer.data['email']}):\n\n"
                f"Phone Number: {serializer.data['phone_number']}\n"
                f"Subject: {serializer.data['subject']}\n"
                f"Message: {serializer.data['message']}\n"
                f"Budget: {serializer.data['budget'] or 'Not specified'}"
            )
            logger.info(f"Sending email to {settings.ADMIN_EMAIL} from {settings.DEFAULT_FROM_EMAIL}")
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.ADMIN_EMAIL],
                    fail_silently=False,
                )
                logger.info("Email sent successfully")
            except Exception as e:
                logger.error(f"Email sending failed: {str(e)}")
                return Response(
                    {"error": f"Email sending failed: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            return Response(
                {"message": "Thank you for your message! I'll get back to you soon."},
                status=status.HTTP_201_CREATED
            )
        logger.error(f"Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def list(self, request, *args, **kwargs):
        return Response({"detail": "Use POST to submit a contact message."})

@api_view(['GET'])
def get_csrf_token(request):
    return Response({'csrfToken': get_token(request)})