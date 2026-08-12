from rest_framework.response import Response


class SuccessResponseMixin:

    def success_response(self, data=None, message="success"):

        return Response({
            "status": "success",
            "message": message,
            "data": data
        })