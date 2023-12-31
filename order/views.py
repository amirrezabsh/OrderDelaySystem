from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import DelayService, AssignmentService
delay_service = DelayService()
assignment_service = AssignmentService()


# API call to report delay by the user
@api_view(['GET'])
def report_delay(request, order_id):
    message, status_code, new_estimated_time = delay_service.report_delay(order_id)

    response_data = {'message': message}
    if new_estimated_time is not None:
        response_data['data'] = {'new_estimated_time':new_estimated_time}

    return Response(response_data, status=status_code)

# API call to assign a reported delay to an agent
@api_view(['GET'])
def assign_report(request, agent_id):
    message, status_code = assignment_service.assign_report(agent_id)
    return Response({'message': message}, status=status_code)
