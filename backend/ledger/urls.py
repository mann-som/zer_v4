from django.urls import path
from . import views

urlpatterns = [
    path("get_wallet/", views.WalletView.as_view(), name="get-wallet"),
    path("get_ledger_entry/", views.LedgerListView.as_view(), name="ledger-entry"),
    path("deposit/", views.DepositView.as_view(), name="maunal-depost"),
]