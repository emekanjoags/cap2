from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from rest_framework import permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.db.models import Sum
from datetime import datetime, timedelta
from authentication.models import Profile, BlockedUser
from .models import Receivers, ReservedReceivers, PayerRemnant, AmountDonated
from .dashboardSerializers import *
from django.contrib.auth.models import User
from account.models import Referral, WithrawRefBal, ExchangeRate
import math

class MakeDonation(APIView):
    def get(self, request):
        remnant = 'False'
        receivers_list = Receivers.objects.filter(enter_list=True, has_received=False, receiving_type=1)
        print('receivers: ', receivers_list)
        serializer =  MakeDonationSerializer(receivers_list, many=True)
        print('serializer: ', serializer.data)
        payer_remnant = PayerRemnant.objects.filter(user=request.user, has_remnant=True)
        if payer_remnant:
            remnant = 'True'
        return Response(data={'content':serializer.data, 'remnant':remnant}, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        receiver_remnat = data.get('r_remnant')
        payer_remnant = data.get('p_remnant')
        user_will_pay = data.get('user_pay')
        receiver = data.get('receiver')
        print('type: ', type(receiver))
        print('receiver: ', receiver)

        current_user_still_on_list = False
        profile = Profile.objects.get(user=request.user)
        if not profile.account_name or not profile.account_number or not profile.bank or not profile.phone:
            return Response(data={'stat':'no_account_details'}, status=status.HTTP_200_OK)

        reserved_in_bit = ReservedReceivers.objects.filter(user=request.user, have_received=False, transaction_type=2).first()
        if reserved_in_bit:
            return Response(data={'stat':'reserved_in_bit'}, status=status.HTTP_200_OK)
        try:
            active_receiver = Receivers.objects.get(enter_list=True, has_received=False, name=receiver)
        except Receivers.DoesNotExist:
            return Response(data={'stat':'taken'}, status=status.HTTP_200_OK)
        
        try:
            current_user_still_on_list = Receivers.objects.get(has_received=False, user=request.user)
        except Receivers.DoesNotExist:
            current_user_still_on_list = False
        if current_user_still_on_list:
            return Response(data={'stat':'still_on_list'}, status=status.HTTP_200_OK)

        if receiver_remnat:
            active_receiver.amount = receiver_remnat
        else:
            active_receiver.enter_list = False
        print('receiver:', active_receiver)
        active_receiver.save()
        receiving_profile = Profile.objects.get(user=active_receiver.user)
        print('prof:', receiving_profile)
        print('acct: ', receiving_profile.account_name)
        expiry_date = datetime.now() + timedelta(1)
        ReservedReceivers.objects.create(user=request.user, receiving_amount=user_will_pay, receivers_name=active_receiver.name,
            receiving_user=active_receiver.user, transaction_type=1, phone=receiving_profile.phone,
             account_name=receiving_profile.account_name, account_number=receiving_profile.account_number, bank=receiving_profile.bank,
             givers_phone=profile.phone, givers_name=request.user.username, expiry_date=expiry_date)
        AmountDonated.objects.create(user=request.user, amount=user_will_pay)
        
        if payer_remnant:
            PayerRemnant.objects.create(user=request.user, has_remnant=True)
        return Response(data={'stat':'good'}, status=status.HTTP_200_OK)

class MakeDonationB(APIView):
    def get(self, request):
        remnant = False
        receivers_list = Receivers.objects.filter(enter_list=True, has_received=False, receiving_type=2)
        print('receivers: ', receivers_list)
        serializer =  MakeDonationBSerializer(receivers_list, many=True)
        print('serializer: ', serializer)
        payer_remnant = PayerRemnant.objects.filter(user=request.user, has_remnant=True)
        if payer_remnant:
            remnant = 'True'
        return Response(data={'content':serializer.data, 'remnant':remnant}, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        receiver_remnat = data.get('r_remnant')
        payer_remnant = data.get('p_remnant')
        user_will_pay = data.get('user_pay')
        receiver = data.get('receiver')
        print('type: ', type(receiver))
        print('receiver: ', receiver)

        current_user_still_on_list = False
        profile = Profile.objects.get(user=request.user)

        if not profile.bitcoin_wallet or not profile.phone:
            return Response(data={'stat':'no_account_details'}, status=status.HTTP_200_OK)
        reserved_in_naira = ReservedReceivers.objects.filter(user=request.user, have_received=False, transaction_type=1).first()
        if reserved_in_naira:
            return Response(data={'stat':'reserved_in_naira'}, status=status.HTTP_200_OK)
        try:
            active_receiver = Receivers.objects.get(enter_list=True, has_received=False, name=receiver)
        except Receivers.DoesNotExist:
            return Response(data={'stat':'taken'}, status=status.HTTP_200_OK)
        try:
            current_user_still_on_list = Receivers.objects.get(has_received=False, user=request.user)
        except Receivers.DoesNotExist:
            current_user_still_on_list = False
        if current_user_still_on_list:
            return Response(data={'stat':'still_on_list'}, status=status.HTTP_200_OK)
        if receiver_remnat:
            active_receiver.amount = receiver_remnat
        else:
            active_receiver.enter_list = False
        print('receiver:', active_receiver)
        active_receiver.save()
        receiving_profile = Profile.objects.get(user=active_receiver.user)
        print('prof:', receiving_profile)
        print('acct: ', receiving_profile.account_name)
        expiry_date = datetime.now() + timedelta(1)
        ReservedReceivers.objects.create(user=request.user, receiving_amount=user_will_pay, receivers_name=active_receiver.name,
            receiving_user=active_receiver.user, transaction_type=2, phone=receiving_profile.phone,
             bitcoin_wallet=receiving_profile.bitcoin_wallet,
             givers_phone=profile.phone, givers_name=request.user.username, expiry_date=expiry_date)
        AmountDonated.objects.create(user=request.user, amount=user_will_pay)
        if payer_remnant:
            PayerRemnant.objects.create(user=request.user, has_remnant=True)
        return Response(data={'stat':'good'}, status=status.HTTP_200_OK)

@login_required(login_url='login-page')
def donationPage(request):
    return render(request, 'donation/make-donation.html')

class DashBoard(View):
    def get(self, request):
        context = {}
        return render(request, 'donation/dashboard.html')

class DisplayMsg(APIView):
    def get(self, request):

        receiver_msg = Receivers.objects.filter(enter_list=False, user=request.user, has_received=False, display_msg=True)
        if receiver_msg.count() < 1:
            on_list_msg = Receivers.objects.filter(enter_list=True, user=request.user)
            if on_list_msg:
                return Response(data={'stat':'on_list'}, status=status.HTTP_200_OK)
            else:
                return Response(data={'stat':'not_receiver'}, status=status.HTTP_200_OK)
        serializer = MakeDonationSerializer(receiver_msg, many=True)
        return Response(data={'stat':'receiver', 'content': serializer.data}, status=status.HTTP_200_OK)

class PendingCashDonations(APIView):
    def get(self, request):
        reservedreceivers = ReservedReceivers.objects.filter(user=request.user, transaction_type=1, have_paid=False, blocked=False)
        print('reseved: ', reservedreceivers)
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
        print('pic: ', picture)
        print('acct_name: ', acct_name)
        reservedreceivers = ReservedReceivers.objects.filter(user=request.user, transaction_type=1, 
        phone=phone, receiving_amount=receiving_amount, have_paid=False).first()
        reservedreceivers.pop = picture
        reservedreceivers.have_paid = True
        reservedreceivers.save()
        return Response(data={'status':'alright'}, status=status.HTTP_200_OK)

class PendingBitcoinDonations(APIView):
    def get(self, request):
        reservedreceivers = ReservedReceivers.objects.filter(user=request.user, transaction_type=2, have_paid=False, blocked=False)
        print('reseved: ', reservedreceivers)
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
        print('pic: ', picture)
        print('wallet: ', wallet)
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

        reserved_receivers = ReservedReceivers.objects.filter(user=blocked_user, receiving_user=request.user,
        have_paid=False).first()
        if reserved_receivers:
            if timezone.now() > reserved_receivers.expiry_date:
                print('user: ', blocked_user)
                user = User.objects.get(id=int(blocked_user))
                user.is_active = False
                user.save()
                BlockedUser.objects.create(user=user, blocker=request.user)
                reserved_receivers.blocked = True
                reserved_receivers.save()
                check_active_receivers = Receivers.objects.filter(enter_list=True, has_received=False, user=request.user, receiving_type=int(transaction_type)).first()
                if not check_active_receivers:
                    Receivers.objects.create(user=request.user, name=request.user.username, amount=unpaid_amount, enter_list=True, receiving_type=int(transaction_type))
                if check_active_receivers:
                    check_active_receivers.amount += unpaid_amount
                    check_active_receivers.save()
                return Response(data={'stat':'user_blocked'}, status=status.HTTP_200_OK)

            else:
               return Response(data={'stat':'still_time'}, status=status.HTTP_200_OK)


 

class ConfirmUser(APIView):
    def post(self, request):
        data = request.data
        paying_user = data.get('payer')
        amount = data.get('amount')
        print('type: ', data.get('type'))
        trans_type = int(data.get('type'))
        payer = User.objects.get(id=int(paying_user))
        profile = Profile.objects.get(user=payer)
        receiver = ReservedReceivers.objects.filter(user=payer, receiving_user=request.user, receiving_amount=amount, have_paid=True, have_received=False).first()
        if not receiver:
            return Response(data={'stat':'already_confirmed'}, status=status.HTTP_200_OK)
        receiver.have_received = True
        receiver.save()
        donated_amount = AmountDonated.objects.filter(user=payer, amount=amount, completed=False).first()
        if donated_amount:
            donated_amount.completed = True
            donated_amount.save()
        is_referred = 0
        try:
            is_referred = Referral.objects.get(user=payer, is_settled=False)
        except Referral.DoesNotExist:
            pass
        if is_referred:
            is_referred.is_settled = True
            is_referred.save()
            referrer = is_referred.referrer
            referrer_wallet = Profile.objects.get(user=referrer.pk)
            referrer_wallet.referral_balance += 2000
            referrer_wallet.referred_active += 1
            referrer_wallet.save()

        check_receiver_stat = ReservedReceivers.objects.filter(receiving_user=request.user, have_received=False, blocked=False)
        if not check_receiver_stat:
            is_receiver_on_list = Receivers.objects.filter(user=request.user, enter_list=True)
            if not is_receiver_on_list:
                receivers = Receivers.objects.filter(user=request.user, has_received=False)
                for i in receivers:
                    i.has_received = True
                    i.save()
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
                    print('amt: ', total_amt)
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
                        rate_qs = ExchangeRate.objects.filter().first()
                        rate = rate_qs.rate
                        if trans_type == 1 and mode == 2:
                            conv_amt = total_amt * rate
                        elif trans_type == 2 and mode == 1:
                            conv_amt = math.floor(total_amt / rate)
                    if mode == 2:
                        ref_bal = ref_bal * rate
                    roi = conv_amt * 1.5
                    roi += ref_bal
                    date_start = datetime.now() + timedelta(days=1)
                    date_end = datetime.now() + timedelta(days=8)
                    Receivers.objects.create(user=payer, name=payer.username, date_end=date_end, date_start=date_start, receiving_type=mode, amount=roi)
        return Response(data={'stat':'success'}, status=status.HTTP_200_OK)



@login_required(login_url='login-page')
def transactions(request):
    return render(request, 'donation/transactions.html')

class CompletedTransactions(APIView):
    def get(self, request):
        transactions = ReservedReceivers.objects.filter(user=request.user, have_paid=True)
        if transactions.count() < 1:
            return Response(data={'stat':"emtpy"}, status=status.HTTP_200_OK)
        serializer = ReservedReceiversSerializer(transactions, many=True)
        return Response(data={'stat':"good", 'content':serializer.data}, status=status.HTTP_200_OK)
class CompletedTransactionsW(APIView):
    def get(self, request):
        transactions = ReservedReceivers.objects.filter(receiving_user=request.user, have_received=True)
        if transactions.count() < 1:
            return Response(data={'stat':"emtpy"}, status=status.HTTP_200_OK)
        serializer = ReservedReceiversSerializer(transactions, many=True)
        return Response(data={'stat':"good", 'content':serializer.data}, status=status.HTTP_200_OK)