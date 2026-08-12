# notification_views.py
from rest_framework import viewsets, permissions, decorators, response, status
from maintenance.models import Notification
from maintenance.serializers import NotificationSerializer
from maintenance.base.pagination import NotificationPagination

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = NotificationPagination  # ✅ ajout pagination

    def get_queryset(self):
        # ✅ chaque utilisateur ne voit que ses notifications
        return Notification.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        # ✅ marquer comme lu
        serializer.save(user=self.request.user)
    
    @decorators.action(detail=False, methods=["post"])
    def mark_all_read(self, request):
        # ✅ marquer toutes les notifications comme lues
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        count = notifications.update(is_read=True)
        return response.Response(
            {"message": f"{count} notifications marquées comme lues."},
            status=status.HTTP_200_OK
        )
        
