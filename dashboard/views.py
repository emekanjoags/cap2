from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from rest_framework import permissions, status, generics
from rest_framework.response import Response
from django.urls import reverse
from rest_framework.views import APIView
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.db.models import Sum
from datetime import datetime, timedelta
from authentication.models import Profile, BlockedUser
from .models import Receivers, ReservedReceivers, PayerRemnant, AmountDonated, Timer, Investor
from .dashboardSerializers import *
from django.contrib.auth.models import User
from account.models import Referral, WithrawRefBal, ExchangeRate
import math
from testimony.models import Testimony
from django.contrib import messages
from random import randint
from django.utils.decorators import decorator_from_middleware
from utilities.general_middleware import AdminCheckMiddleware
from utilities.mailing import Mailer




class InvestApi(APIView):
    def post(self, request):
        data = request.data
        amount = int(data.get('amount'))
        print('amount: ', amount)
        profile = Profile.objects.get(user=request.user)
        if not profile.account_name or not profile.account_number or not profile.bank or not profile.phone:
            return Response(data={'stat':'no_account_details'}, status=status.HTTP_200_OK)
        no_testimony = Receivers.objects.filter(user=request.user, has_received=True, has_testified=False)
        if no_testimony:
            return Response(data={'stat':'no_testimony'}, status=status.HTTP_200_OK)
        investors = Investor.objects.filter(received_roi=False, user=request.user)
        if investors:
            return Response(data={'stat':'already_invested'}, status=status.HTTP_200_OK)
        package = 0
        if amount >= 50000:
            package = 2
        elif amount < 50000:
            package = 1
        else:
            return Response(data={'stat':'incorrect_amount'}, status=status.HTTP_200_OK)
        Investor.objects.create(user=request.user, amount=amount, name=request.user.username, transaction_type=1, package=package)
        return Response(data={'stat':'good'}, status=status.HTTP_200_OK)

class InvestApib(APIView):
    def post(self, request):
        data = request.data
        amount = float(data.get('amount'))
        print('amount: ', amount)
        profile = Profile.objects.get(user=request.user)
        if not profile.bitcoin_wallet or not profile.phone:
            return Response(data={'stat':'no_account_details'}, status=status.HTTP_200_OK)
        no_testimony = Receivers.objects.filter(user=request.user, has_received=True, has_testified=False)
        if no_testimony:
            return Response(data={'stat':'no_testimony'}, status=status.HTTP_200_OK)
        investors = Investor.objects.filter(received_roi=False, user=request.user)
        if investors:
            return Response(data={'stat':'already_invested'}, status=status.HTTP_200_OK)
        package = 0
        if amount >= 0.012:
            package = 2
        elif amount < 0.012:
            package = 1
        else:
            return Response(data={'stat':'incorrect_amount'}, status=status.HTTP_200_OK)
        Investor.objects.create(user=request.user, amount=amount, name=request.user.username, transaction_type=2, package=package)
        return Response(data={'stat':'good'}, status=status.HTTP_200_OK)
class GetInvestors(APIView):
    def get(self, request):
        investors = Investor.objects.filter(received_roi=False, user=request.user)
        serializer = InvestorSerializer(investors, many=True)
        print('invest: ', investors)
        if investors:
            return Response(data={'content':serializer.data, 'stat':'good'}, status=status.HTTP_200_OK)
        return Response(data={'content':serializer.data, 'stat':'none'}, status=status.HTTP_200_OK)
class MatchApib(APIView):
    def get(self, request):
        investors = Investor.objects.filter(enter_list=True, transaction_type=2, completed=False)
        serializer = InvestorSerializer(investors, many=True)
        return Response(data={'content':serializer.data, 'stat':'good'}, status=status.HTTP_200_OK)
    def post(self, request):
        data = request.data
        receiver_remnant = data.get('receiver_remnant')
        payer_remnant = data.get('payer_remnant')
        user_will_pay = data.get('user_pay')
        receiver = data.get('receiver')
        investor = data.get('investor')

        investor = User.objects.get(username=investor)
        receiver = User.objects.get(username=receiver)
        investor_prof = Profile.objects.get(user=investor)
        receiver_prof = Profile.objects.get(user=receiver)
        expiry_date = timezone.localtime() + timedelta(days=1)
        investor_obj = Investor.objects.filter(user=investor, completed=False, matched=False).first()
        investor_obj.matched = True
        investor_obj.save()
        receiver_obj = Receivers.objects.filter(user=receiver, has_received=False, blocked=False).first()
        if receiver_remnant:
            receiver_obj.amount = receiver_remnant
            receiver_obj.save()
            print('recev: ', receiver_obj.amount)
        else:
            receiver_obj.enter_list = False
            receiver_obj.save()
        investor_obj = Investor.objects.filter(user=investor, completed=False, matched=True).first()
        if payer_remnant:
            investor_obj.invested_amt = investor_obj.amount - float(payer_remnant)
            investor_obj.amount = payer_remnant
            investor_obj.save()
        else:
            investor_obj.invested_amt = investor_obj.amount
            investor_obj.amount = 0
            investor_obj.enter_list = False
            investor_obj.save()
        ReservedReceivers.objects.create(receiving_amount=user_will_pay, user=investor, receiving_user= receiver,
        transaction_type=2, phone=receiver_prof.phone, givers_phone=investor_prof.phone, receivers_name=receiver.username, 
        givers_name=investor.username, bitcoin_wallet=receiver_prof.bitcoin_wallet, expiry_date=expiry_date)
        AmountDonated.objects.create(user=investor, amount=user_will_pay)
        Mailer().matched_mail(investor.username, receiver.username, investor.email)
        return Response(data={'stat':'good'}, status=status.HTTP_200_OK)

class MatchApi(APIView):
    def get(self, request):
        investors = Investor.objects.filter(enter_list=True, transaction_type=1, completed=False)
        serializer = InvestorSerializer(investors, many=True)
        return Response(data={'content':serializer.data, 'stat':'good'}, status=status.HTTP_200_OK)
    def post(self, request):
        data = request.data
        receiver_remnant = data.get('receiver_remnant')
        payer_remnant = data.get('payer_remnant')
        user_will_pay = data.get('user_pay')
        receiver = data.get('receiver')
        investor = data.get('investor')

        investor = User.objects.get(username=investor)
        receiver = User.objects.get(username=receiver)
        investor_prof = Profile.objects.get(user=investor)
        receiver_prof = Profile.objects.get(user=receiver)
        expiry_date = timezone.localtime() + timedelta(days=1)
        investor_obj = Investor.objects.filter(user=investor, completed=False, matched=False).first()
        if investor_obj:
            investor_obj.matched = True
            investor_obj.save()
        receiver_obj = Receivers.objects.filter(user=receiver, has_received=False, blocked=False).first()
        if receiver_remnant:
            receiver_obj.amount = receiver_remnant
            receiver_obj.save()
        else:
            receiver_obj.enter_list = False
            receiver_obj.save()
        investor_obj = Investor.objects.filter(user=investor, completed=False, matched=True).first()
        if payer_remnant:
            new_invested_amt = investor_obj.amount - float(payer_remnant)
            investor_obj.invested_amt += new_invested_amt
            investor_obj.amount = payer_remnant
            investor_obj.save()
        else:
            investor_obj.invested_amt += investor_obj.amount
            investor_obj.amount = 0
            investor_obj.enter_list = False
            investor_obj.save()
        ReservedReceivers.objects.create(receiving_amount=user_will_pay, user=investor, receiving_user= receiver,
        transaction_type=1, phone=receiver_prof.phone, givers_phone=investor_prof.phone, receivers_name=receiver.username, 
        givers_name=investor.username, bank=receiver_prof.bank, account_name=receiver_prof.account_name, account_number=receiver_prof.account_number, expiry_date=expiry_date)
        AmountDonated.objects.create(user=investor, amount=user_will_pay)
        Mailer().matched_mail(investor.username, receiver.username, investor.email)
        return Response(data={'stat':'good'}, status=status.HTTP_200_OK)

class TimerDisplay(APIView):
    def get(self, request):
        timer = Timer.objects.get(id=1)
        serializer = TimerSerializer(timer)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class MakeDonation(APIView):
    def get(self, request):
        remnant = 'False'
        receivers_list = Receivers.objects.filter(enter_list=True, has_received=False, receiving_type=1)
        serializer =  MakeDonationSerializer(receivers_list, many=True)
        payer_remnant = PayerRemnant.objects.filter(user=request.user, has_remnant=True)
        if payer_remnant:
            remnant = 'True'
        if not receivers_list.first():
            return Response(data={'content':serializer.data, 'remnant':remnant, 'stat':'empty'}, status=status.HTTP_200_OK)
        return Response(data={'content':serializer.data, 'remnant':remnant, 'stat':'good'}, status=status.HTTP_200_OK)

        
class MakeDonationB(APIView):
    def get(self, request):
        remnant = False
        receivers_list = Receivers.objects.filter(enter_list=True, has_received=False, receiving_type=2)
        serializer =  MakeDonationBSerializer(receivers_list, many=True)
        payer_remnant = PayerRemnant.objects.filter(user=request.user, has_remnant=True)
        if payer_remnant:
            remnant = 'True'
        if not receivers_list.first():
            return Response(data={'content':serializer.data, 'remnant':remnant, 'stat':'empty'}, status=status.HTTP_200_OK)
        return Response(data={'content':serializer.data, 'remnant':remnant, 'stat':'good'}, status=status.HTTP_200_OK)
    
    

@login_required(login_url='login-page')
def donationPage(request):
    return render(request, 'donation/make-donation.html')

class DashBoard(View):
    def get(self, request):
        not_testified = 0
        not_testimony_user = Receivers.objects.filter(user=request.user, has_received=True, has_testified=False)
        if not_testimony_user.first():
            not_testified = 1
        
        context = {
            'not_testified':not_testified
        }
        return render(request, 'donation/dashboard.html', context)
@login_required(login_url='login-page')
def testify(request):
    if request.method == "POST":
        profile = Profile.objects.get(user=request.user)
        text = request.POST.get('text')
        if len(text) < 10:
            messages.warning(request, 'Text too short')
            return render(request, 'donation/testify.html')
            #return HttpResponseRedirect(reverse('dashboard:testify'))
        time = timezone.now()
        Testimony.objects.create(user=request.user, profile=profile, content=text, name=request.user.username, time=time)
        receiver = Receivers.objects.filter(user=request.user, has_received=True, has_testified=False)
        if receiver:
            for obj in receiver:
                obj.has_testified = True
                obj.save()
            messages.success(request, 'Thank you for sharing your testimony, you can now make new investments')
            return HttpResponseRedirect(reverse('dashboard:dashboard'))
    return render(request, 'donation/testify.html')

class DisplayMsg(APIView):
    def get(self, request):

        receiver_msg = Receivers.objects.filter(enter_list=True, user=request.user, has_received=False,)
        if receiver_msg.count() < 1:
            return Response(data={'stat':'not_receiver'}, status=status.HTTP_200_OK)
        serializer = MakeDonationSerializer(receiver_msg, many=True)
        return Response(data={'stat':'receiver', 'content': serializer.data}, status=status.HTTP_200_OK)

class PendingCashDonations(APIView):
    def get(self, request):
        reservedreceivers = ReservedReceivers.objects.filter(user=request.user, transaction_type=1, have_paid=False, blocked=False)
        if reservedreceivers.count() < 1:
            return Response(data={'stat':'no_pay_money'}, status=status.HTTP_200_OK)
        serializer =  ReservedReceiversSerializer(reservedreceivers, many=True)
        return Response(data={'stat':'good', 'content':serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        picture = data.get('picture')
        acct_name = data.get('acct_name')
        phone = data.get('phone')
        receiving_amount = data.get('amount')
        reservedreceivers = ReservedReceivers.objects.filter(user=request.user, transaction_type=1, 
        phone=phone, receiving_amount=receiving_amount, have_paid=False).first()
        reservedreceivers.pop = picture
        reservedreceivers.have_paid = True
        reservedreceivers.save()
        return Response(data={'status':'alright'}, status=status.HTTP_200_OK)

class PendingBitcoinDonations(APIView):
    def get(self, request):
        reservedreceivers = ReservedReceivers.objects.filter(user=request.user, transaction_type=2, have_paid=False, blocked=False)
        if reservedreceivers.count() < 1:
            return Response(data={'stat':'no_pay_money'}, status=status.HTTP_200_OK)
        serializer =  ReservedReceiversSerializer(reservedreceivers, many=True)
        return Response(data={'stat':'good', 'content':serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        picture = data.get('picture')
        wallet = data.get('wallet')
        phone = data.get('phone')
        receiving_amount = data.get('amount')
        reservedreceivers = ReservedReceivers.objects.filter(user=request.user, transaction_type=2, 
        phone=phone, receiving_amount=receiving_amount, have_paid=False).first()
        reservedreceivers.pop = picture
        reservedreceivers.have_paid = True
        reservedreceivers.save()
        return Response(data={'status':'alright'}, status=status.HTTP_200_OK)

class PendingCashWithdraw(APIView):
    def get(self, request):
        reservedreceivers = ReservedReceivers.objects.filter(receiving_user=request.user, transaction_type=1, have_received=False, blocked=False)
        if reservedreceivers.count() < 1:
            return Response(data={'stat':'no_receive_money'}, status=status.HTTP_200_OK)
        serializer =  ReservedReceiversSerializer(reservedreceivers, many=True)
        return Response(data={'stat':'good', 'content':serializer.data}, status=status.HTTP_200_OK)

class PendingBitcoinWithdraw(APIView):
    def get(self, request):
        reservedreceivers = ReservedReceivers.objects.filter(receiving_user=request.user, transaction_type=2, have_received=False, blocked=False)
        if reservedreceivers.count() < 1:
            return Response(data={'stat':'no_receive_money'}, status=status.HTTP_200_OK)
        serializer =  ReservedReceiversSerializer(reservedreceivers, many=True)
        return Response(data={'stat':'good', 'content':serializer.data}, status=status.HTTP_200_OK)

class BlockMemberView(APIView):
    def post(self, request):
        data = request.data
        blocked_user = data.get('blocked_user')
        expiry_date = data.get('expiry_date')
        unpaid_amount = data.get('unpaid_amount')
        transaction_type = data.get('transaction_type')

        check_active_receivers = 0

        reserved_receivers = ReservedReceivers.objects.filter(user=blocked_user, receiving_amount=unpaid_amount, receiving_user=request.user,
        have_paid=False).first()
        if reserved_receivers:
            if timezone.now() > reserved_receivers.expiry_date and not reserved_receivers.pop:
                user = User.objects.get(id=int(blocked_user))
                user.is_active = False
                user.save()
                BlockedUser.objects.create(user=user, blocker=request.user)
                reserved_receivers.blocked = True
                reserved_receivers.save()
                check_active_receivers = Receivers.objects.filter(enter_list=True, has_received=False, user=request.user, receiving_type=int(transaction_type)).first()
                if not check_active_receivers:
                    date_start = timezone.localtime() + timedelta(days=1)
                    date_end = timezone.localtime() + timedelta(days=1)
                    Receivers.objects.create(user=request.user, is_priority=True, date_end=date_end, date_start=date_start, name=request.user.username, amount=unpaid_amount, has_entered_list=True, enter_list=True, receiving_type=int(transaction_type))
                if check_active_receivers:
                    check_active_receivers.amount += unpaid_amount
                    check_active_receivers.is_priority = True
                    check_active_receivers.save()
                return Response(data={'stat':'user_blocked'}, status=status.HTTP_200_OK)

            else:
               return Response(data={'stat':'still_time'}, status=status.HTTP_200_OK)


 

class ConfirmUser(APIView):
    def post(self, request):
        data = request.data
        paying_user = data.get('payer')
        amount = data.get('amount')
        trans_type = int(data.get('type'))
        payer = User.objects.get(id=int(paying_user))
        profile = Profile.objects.get(user=payer)
        rate_qs = ExchangeRate.objects.filter().first()
        rate = rate_qs.rate
        receiver = ReservedReceivers.objects.filter(user=payer, receiving_user=request.user, receiving_amount=amount, have_paid=True, have_received=False).first()
        if not receiver:
            return Response(data={'stat':'already_confirmed'}, status=status.HTTP_200_OK)
        receiver.have_received = True
        receiver.save()
        donated_amount = AmountDonated.objects.filter(user=payer, amount=amount, completed=False).first()
        if donated_amount:
            donated_amount.completed = True
            donated_amount.save()
        check_receiver_stat = ReservedReceivers.objects.filter(receiving_user=request.user, have_received=False, blocked=False)
        if not check_receiver_stat:
            is_receiver_on_list = Receivers.objects.filter(user=request.user, enter_list=True)
            if not is_receiver_on_list:
                receivers = Receivers.objects.filter(user=request.user, has_received=False)
                for i in receivers:
                    i.has_received = True
                    i.save()
                receiver_investor = Investor.objects.filter(user=request.user, received_roi=False).first()
                if receiver_investor:
                    receiver_investor.received_roi = True
                    receiver_investor.save()
        check_if_payer = AmountDonated.objects.filter(user=payer)
        if check_if_payer:
            check_payer_stat = AmountDonated.objects.filter(user=payer, completed=False)
            if not check_payer_stat:
                total_donated_amount = AmountDonated.objects.filter(user=payer, completed=True, receiver_created=False)
                if total_donated_amount:
                    total_amt = 0
                    for i in total_donated_amount:
                        total_amt += i.amount
                        i.receiver_created = True
                        i.save()
                    package = 0
                    investor_obj = Investor.objects.filter(user=payer, completed=False, matched=True).first()
                    if investor_obj:
                        investor_obj.completed = True
                        package = investor_obj.package
                        investor_obj.save()
                    process_ref = 1
                    ref_amt = 0
                    if trans_type == 1:
                        ref_amt = math.floor(total_amt * 0.1)
                    if trans_type == 2:
                        naira_amt = total_amt/rate
                        ref_amt = math.floor(naira_amt * 0.1)
                    if process_ref:
                        is_referred = 0
                        try:
                            is_referred = Referral.objects.get(user=payer, is_settled=False)
                        except Referral.DoesNotExist:
                            pass
                        if is_referred:
                            is_referred.is_settled = True
                            is_referred.amount = ref_amt
                            is_referred.save()
                            referrer = is_referred.referrer
                            referrer_wallet = Profile.objects.get(user=referrer.pk)
                            referrer_wallet.referral_balance += ref_amt
                            referrer_wallet.referred_active += 1
                            referrer_wallet.save()
                    mode = profile.mode_of_receiving
                    ref_bal = 0
                    ref_bal_obj = 0
                    ref_bal_qs = WithrawRefBal.objects.filter(user=payer, collected=False)
                    if ref_bal_qs:
                        ref_bal_obj = ref_bal_qs.first()
                        ref_bal = ref_bal_obj.balance
                        ref_bal_obj.collected = True
                        ref_bal_obj.save() 
                    conv_amt = 0
                    if trans_type == mode:
                        conv_amt = total_amt
                    elif trans_type != mode:
                        if trans_type == 1 and mode == 2:
                            conv_amt = total_amt * rate
                        elif trans_type == 2 and mode == 1:
                            conv_amt = math.floor(total_amt / rate)
                            print('conv: ', conv_amt)
                    if mode == 2:
                        ref_bal = ref_bal * rate
                    if package:
                        percent = 1.5
                        if package == 2:
                            percent = 1.3
                        roi = conv_amt * percent
                        roi += ref_bal
                        date_start = timezone.localtime() + timedelta(days=1)
                        date_end = timezone.localtime() + timedelta(days=8)
                        Receivers.objects.create(user=payer, name=payer.username, enter_list=True, date_end=date_end, date_start=date_start, receiving_type=mode, amount=roi)
        return Response(data={'stat':'success'}, status=status.HTTP_200_OK)



@login_required(login_url='login-page')
def transactions(request):
    return render(request, 'donation/transactions.html')

class CompletedTransactions(APIView):
    def get(self, request):
        transactions = ReservedReceivers.objects.filter(user=request.user, have_paid=True).order_by('-id')
        if transactions.count() < 1:
            return Response(data={'stat':"emtpy"}, status=status.HTTP_200_OK)
        serializer = ReservedReceiversSerializer(transactions, many=True)
        return Response(data={'stat':"good", 'content':serializer.data}, status=status.HTTP_200_OK)
class CompletedTransactionsW(APIView):
    def get(self, request):
        transactions = ReservedReceivers.objects.filter(receiving_user=request.user, have_received=True).order_by('-id')
        if transactions.count() < 1:
            return Response(data={'stat':"emtpy"}, status=status.HTTP_200_OK)
        serializer = ReservedReceiversSerializer(transactions, many=True)
        return Response(data={'stat':"good", 'content':serializer.data}, status=status.HTTP_200_OK)

@decorator_from_middleware(AdminCheckMiddleware)
def adminConfirmUser(request):
    if request.method == 'POST':
        data = request.POST
        paying_user = data.get('payer')
        amount = data.get('amount')
        trans_type = int(data.get('type'))
        receiver_p = data.get('receiver')
        rate_qs = ExchangeRate.objects.filter().first()
        rate = rate_qs.rate
        try:
            payer = User.objects.get(username=paying_user)
        except User.DoesNotExist:
            messages.warning(request, 'No user like this')
            return HttpResponseRedirect(reverse('dashboard:admin-confirm'))
        try:
            receiving_user = User.objects.get(username=receiver_p)
        except User.DoesNotExist:
            messages.warning(request, 'No receiver like this')
            return HttpResponseRedirect(reverse('dashboard:admin-confirm'))
        profile = Profile.objects.get(user=payer)
        receiver = ReservedReceivers.objects.filter(user=payer, receiving_user=receiving_user, receiving_amount=amount, have_paid=True, have_received=False).first()
        if not receiver:
            messages.warning(request, 'this receiver does not exist or already confirmed')
            return HttpResponseRedirect(reverse('dashboard:admin-confirm'))
        receiver.have_received = True
        receiver.save()
        donated_amount = AmountDonated.objects.filter(user=payer, amount=amount, completed=False).first()
        if donated_amount:
            donated_amount.completed = True
            donated_amount.save()
        check_receiver_stat = ReservedReceivers.objects.filter(receiving_user=receiving_user, have_received=False, blocked=False)
        if not check_receiver_stat:
            is_receiver_on_list = Receivers.objects.filter(user=receiving_user, enter_list=True)
            if not is_receiver_on_list:
                receivers = Receivers.objects.filter(user=receiving_user, has_received=False)
                for i in receivers:
                    i.has_received = True
                    i.save()
                receiver_investor = Investor.objects.filter(user=receiving_user, received_roi=False).first()
                if receiver_investor:
                    receiver_investor.received_roi = True
                    receiver_investor.save()
        check_if_payer = AmountDonated.objects.filter(user=payer)
        if check_if_payer:
            check_payer_stat = AmountDonated.objects.filter(user=payer, completed=False)
            if not check_payer_stat:
                total_donated_amount = AmountDonated.objects.filter(user=payer, completed=True, receiver_created=False)
                if total_donated_amount:
                    total_amt = 0
                    for i in total_donated_amount:
                        total_amt += i.amount
                        i.receiver_created = True
                        i.save()
                    package = 0
                    investor_obj = Investor.objects.filter(user=payer, completed=False, matched=True).first()
                    if investor_obj:
                        investor_obj.completed = True
                        package = investor_obj.package
                        investor_obj.save()
                    process_ref = 1
                    ref_amt = 0
                    if trans_type == 1:
                        ref_amt = math.floor(total_amt * 0.1)
                    if trans_type == 2:
                        naira_amt = total_amt/rate
                        ref_amt = math.floor(naira_amt * 0.1)
                    if process_ref:
                        is_referred = 0
                        try:
                            is_referred = Referral.objects.get(user=payer, is_settled=False)
                        except Referral.DoesNotExist:
                            pass
                        if is_referred:
                            is_referred.is_settled = True
                            is_referred.amount = ref_amt
                            is_referred.save()
                            referrer = is_referred.referrer
                            referrer_wallet = Profile.objects.get(user=referrer.pk)
                            referrer_wallet.referral_balance += ref_amt
                            referrer_wallet.referred_active += 1
                            referrer_wallet.save()
                    mode = profile.mode_of_receiving
                    ref_bal = 0
                    ref_bal_obj = 0
                    ref_bal_qs = WithrawRefBal.objects.filter(user=payer, collected=False)
                    if ref_bal_qs:
                        ref_bal_obj = ref_bal_qs.first()
                        ref_bal = ref_bal_obj.balance
                        ref_bal_obj.collected = True
                        ref_bal_obj.save() 
                    conv_amt = 0
                    if trans_type == mode:
                        conv_amt = total_amt
                    elif trans_type != mode:
                        if trans_type == 1 and mode == 2:
                            conv_amt = total_amt * rate
                        elif trans_type == 2 and mode == 1:
                            conv_amt = math.floor(total_amt / rate)
                    if mode == 2:
                        ref_bal = ref_bal * rate
                    if package:
                        percent = 1.5
                        if package == 2:
                            percent = 1.3
                        roi = conv_amt * percent
                        roi += ref_bal
                        date_start = timezone.localtime() + timedelta(days=1)
                        date_end = timezone.localtime() + timedelta(days=8)
                        Receivers.objects.create(user=payer, name=payer.username, date_end=date_end, date_start=date_start, receiving_type=mode, amount=roi, enter_list=True)
                        messages.success(request, 'User confirmed successfully!')
                        return HttpResponseRedirect(reverse('dashboard:admin-confirm'))
    return render(request, 'account/admin-confirm.html')

