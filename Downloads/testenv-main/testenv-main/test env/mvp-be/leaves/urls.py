from django.urls import path
from .views import SubmitLeaveRequestView, ApproveRejectLeaveView, ViewLeavesView

urlpatterns = [
    path("submit/", SubmitLeaveRequestView.as_view(), name="submit_leave_request"),
    path("<int:leave_id>/approve_reject/", ApproveRejectLeaveView.as_view(), name="approve_reject_leave"),
    path("status/", ViewLeavesView.as_view(), name="view_leaves"),
    path("<int:leave_id>/", ViewLeavesView.as_view(), name="leave_detail"),
    path("update/", SubmitLeaveRequestView.as_view(), name="update_leave"),
    path("user/<int:user_id>/", ViewLeavesView.as_view(), name="user_leaves"),
    path("<int:leave_id>/cancel/", SubmitLeaveRequestView.as_view(), name="cancel_leave"),
]
