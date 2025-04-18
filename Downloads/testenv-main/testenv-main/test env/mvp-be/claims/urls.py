from django.urls import path
from .views import SubmitClaimView, ApproveRejectClaimView, ViewClaimsView, ClaimStatisticsView

urlpatterns = [
    path("new/", SubmitClaimView.as_view(), name="submit_claim"),
    path("<int:claim_id>/approve_reject/", ApproveRejectClaimView.as_view(), name="approve_reject_claim"),
    path("list/", ViewClaimsView.as_view(), name="view_claims"),
    path("<int:claim_id>/", ViewClaimsView.as_view(), name="claim_detail"),
    path("update/", SubmitClaimView.as_view(), name="update_claim"),
    path("user/<int:user_id>/", ViewClaimsView.as_view(), name="user_claims"),
    path("statistics/", ClaimStatisticsView.as_view(), name="claim_statistics"),
]
