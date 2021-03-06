from django.urls import path
from django.utils.decorators import decorator_from_middleware
from utilities.general_middleware import AuthCheckMiddleware, AuthCheckLoginMiddleware
from .views import (MakeDonation, DashBoard, transactions, donationPage, MakeDonationB, PendingCashDonations,
PendingCashWithdraw, BlockMemberView, ConfirmUser, DisplayMsg, PendingBitcoinDonations, PendingBitcoinWithdraw,
CompletedTransactions, InvestApi, InvestApib, GetInvestors, CompletedTransactionsW, testify, TimerDisplay, adminConfirmUser, MatchApi)

user_auth_decorator = decorator_from_middleware(AuthCheckLoginMiddleware)

app_name = 'dashboard'
urlpatterns = [
    path('api/money', user_auth_decorator(MakeDonation.as_view())),
    path('api/bitcoin', user_auth_decorator(MakeDonationB.as_view())),
    path('donate', donationPage, name="donate" ),
    path('', user_auth_decorator(DashBoard.as_view()), name='dashboard'),
    path('transactions', transactions, name='transactions'),
    # path('transactions', transac, name='transactions'),
    path('api/money-donate', user_auth_decorator(PendingCashDonations.as_view())),
    path('api/money-receive', user_auth_decorator(PendingCashWithdraw.as_view())),
    path('api/block', user_auth_decorator(BlockMemberView.as_view())),
    path('api/confirm', user_auth_decorator(ConfirmUser.as_view())),
    path('api/display_msg', user_auth_decorator(DisplayMsg.as_view())),
    path('api/bitcoin-donate', user_auth_decorator(PendingBitcoinDonations.as_view())),
    path('api/bitcoin-withdraw', user_auth_decorator(PendingBitcoinWithdraw.as_view())),
    path('api/transact', user_auth_decorator(CompletedTransactions.as_view())),
    path('api/transactw', user_auth_decorator(CompletedTransactionsW.as_view())),
    path('api/timer', user_auth_decorator(TimerDisplay.as_view())),
    path('i-wizard', adminConfirmUser, name='admin-confirm'),
    path('testify', testify, name="testify"),
    path('api/get-investors', user_auth_decorator(GetInvestors.as_view())),
    path('api/invest', user_auth_decorator(InvestApi.as_view())),
    path('api/investb', user_auth_decorator(InvestApib.as_view()))
]