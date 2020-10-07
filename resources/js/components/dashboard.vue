<template>
    <div>
    <div v-if="is_loading" id="loader"></div>
        <div v-else>
            <div class='col-12' v-if="receiver_msg" v-for="(msg, index) in receiver_msg">
            <div style="background:green;color:#ffffff;padding:10px 14px;margin-bottom:20px;box-shadow: 5px 5px 5px gray;">
                <p style="color:white" v-if='is_priority[index] == "true"'> You will be matched with another member on {{msg.end}} so that you can be paid your remaining ROI which is <span v-if="msg_type[index] == 1">&#8358;</span><span v-else>BTC </span>{{msg.r_amount}}.</p>
                <p style="color:white" v-else>You have completed your payment and your Return on Investment is <span v-if="msg_type[index] == 1">&#8358;</span><span v-else>BTC </span>{{msg.r_amount}}. You will be matched on {{msg.end}}</p>
            </div>
           </div>
           <!-- <div class="col-12">
                <div class="alert alert-success" v-show='on_list_msg'>
                    <p>{{on_list_msg}}</p>
                 </div>
            </div> -->
         <div class="col-12">
            <div v-show="success_msg" class="alert alert-success">
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    &times;
                </button>
                <span>
                    <p><span style="color:green;">Success <i class="fa fa-check"></i></span>&nbsp;{{success_msg}}</p>
                </span>
            </div>
            <div v-show="error_msg" class="alert alert-warning">
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    &times;
                </button>
                <span>
                    <p><b>Failed!</b>&nbsp; {{error_msg}}</p>
                </span>
            </div>
            
            <div class="toggle">
                <button v-if="donation_view" class="btn btn-danger" @click="toggle_view">Donations</button><button v-else class="btn btn-outline-danger" @click="toggle_view">Donations</button>
                 &nbsp;<button v-if="donation_view" class="btn btn-outline-danger"  @click="toggle_view">Withdrawals</button><button v-else class="btn btn-danger"  @click="toggle_view">Withdrawals</button>
            </div>
            
           </div>
           <!-- CASH DONATIONS -->
        <div v-if="donation_view">
           <div class="col-lg-12">
               <p v-if="pending_payment || pending_payment_b" class="info-area">Please make payment before the countdown runs out to avoid getting blocked. As soon as you make payment and get confirmed you will receive your Return On Investment in 7 days</p>
               <p v-else class="info-area">You have no pending payments, to see your completed transactions go to  <a style="color:#ff4f2e;" href="/dashboard/transactions">Completed Transactions</a> section</p>
               <div class="col-md-4 list" v-if="money_pending_payments" v-for="(pending, index) in money_pending_payments">
                    <ul><span v-show="!pending.pop"><li v-if='expired' style="color:#000000;">{{expired}}</li><li v-else style="width:5px:height:5px;"><flip-countdown v-bind:deadline="timer_list[index].converted_time"></flip-countdown></li></span>
                        <li>Account Name: {{pending.account_name}}</li>
                        <li>Bank Name: {{pending.bank}}</li>
                        <li>Account Number: {{pending.account_number}}</li>
                        <li>Amount: &#8358;{{pending.receiving_amount}}</li>
                        <li>Phone: {{pending.phone}}</li>
                    </ul><br>
                    <div class="apply_btn"  v-show="!expired">
                        <input v-if="pop[index].popbtn" accept="image/*" type="file" ref="files" @change="fileUpload($event, index)">
                        <button v-else class="boxed-btn3 btn-block" id=index type="submit" @click="displayPop(index)">Upload proof of payment</button><br>
                        <button v-show="selected_files[index].selected_file" class="boxed-btn3 btn-block" type="submit" @click="havePaid(index)">Submit</button>
                    </div>
               </div>
           <!-- END OF DONATIONS -->

           <!-- BITCOIN DONATIONS -->
                <div class="col-md-4 list" v-if="bitcoin_pending_payments" v-for="(pending, index) in bitcoin_pending_payments">
                    <ul>
                        <li v-if='expired' style="color:#000000;">{{expired}}</li><li v-else style="width:5px:height:5px;"><flip-countdown v-bind:deadline="timer_listb[index].converted_time"></flip-countdown></li>
                        <li>Username: {{pending.receivers_name}}</li>
                        <li>Wallet ID: {{pending.bitcoin_wallet}}</li>
                        <li>Amount: {{pending.receiving_amount}}BTC</li>
                        <li>Phone: {{pending.phone}}</li>
                    </ul><br>
                    <div class="apply_btn" v-show="!expired">
                        <input v-if="popb[index].popbtn" accept="image/*" type="file" ref="files" @change="fileUploadb($event, index)">
                        <button v-else class="boxed-btn3 btn-block" id=index type="submit" @click="displayPopb(index)">Upload proof of payment</button><br>
                        <button v-show="selected_filesb[index].selected_file" class="boxed-btn3 btn-block" type="submit" @click="havePaidb(index)">Submit</button>
                    </div>
                 </div>
          <!-- END OF CASH DONATIONS -->
           </div>
        </div>

        <div v-else>
           <!-- WITHDRAWALS -->
           <div class="col-lg-12">
                <p v-if="pending_withdrawal || pending_withdrawal_b" class="info-area">You have been matched with this member, payment will be made to you shortly</p>
                <p v-else class="info-area">You have no pending withdrawal, to see your completed transactions go to  <a style="color:#ff4f2e;" href="/dashboard/transactions"> Completed Transactions</a> section</p>
                <div class="col-md-4 list" v-if="money_pending_receiving" v-for="(pending, index) in money_pending_receiving">
                     <ul><span v-if="pending.pop" style="text-align:center;color:#000000;">Member has made payment</span>
                     <span v-else><li v-if='block[index].block_btn' style="color:#000000;">This member's time has expired, please block this member so that you can be matched with another member</li><li v-else style="width:5px:height:5px;"><flip-countdown v-bind:deadline="r_timer_list[index].converted_time"></flip-countdown></li></span>
                         <li>Username: {{pending.givers_name}}</li>
                         <li>Amount: &#8358;{{pending.receiving_amount}}</li>
                         <li>Phone: {{pending.givers_phone}}</li>
                         <button class="btn btn-warning btn-block" type="button" v-if="pending.pop" @click='viewPop(index)'>View Proof of payment</button>
                        <div class="proofm" style="display:none;">
                            <div>
                                <img :src="pending.pop" height='300px' width='100%' />
                            </div>
                        </div>
                     </ul><br>
                     <div v-if="block[index].block_btn && !pending.pop" class="apply_btn">
                         <button class="boxed-btn3 btn-block" type="submit" @click="blockUser(index)">Block member</button>
                     </div>
                     <div v-if="pending.pop" class="apply_btn">
                         <button class="boxed-btn3 btn-block" type="submit" @click="confirmUser(index)">Confirm this Member</button>
                     </div>
                </div>
            <!-- END OF CASH WITHDRAWAL -->

            <!-- BITCOIN WITHDRAWAL -->
                <div class="col-md-4 list" v-if="bitcoin_pending_receiving" v-for="(pending, index) in bitcoin_pending_receiving">
                    <ul><span v-if="pending.pop" style="text-align:center;color:#000000;">Member has made payment</span>
                        <span v-else><li v-if='blockb[index].block_btn' style="color:#000000;">This member's time has expired, please block this member so that you can be matched with another member</li><li v-else style="width:5px:height:5px;"><flip-countdown v-bind:deadline="r_timer_listb[index].converted_time"></flip-countdown></li></span>
                        <li>Username: {{pending.givers_name}}</li>
                        <li>Amount: {{pending.receiving_amount}}BTC</li>
                        <li>Phone: {{pending.givers_phone}}</li>
                        <button class="btn btn-warning btn-block" type="button" v-if="pending.pop" @click='viewPopb(index)'>View Proof of payment</button>
                        <div class="proof" style="display:none;">
                            <div>
                                <img :src="pending.pop" height='300px' width='100%' />
                            </div>
                        </div>
                    </ul><br>
                    <div v-if="blockb[index].block_btn" class="apply_btn">
                         <button class="boxed-btn3 btn-block" type="submit" @click="blockUserb(index)">Block member</button>
                     </div>
                     <div v-if="pending.pop" class="apply_btn">
                         <button class="boxed-btn3 btn-block" type="submit" @click="confirmUserb(index)">Confirm this Member</button>
                     </div>
                </div>
            <!-- END OF BITCOIN WITHDRAWAL -->

            <!-- END OF RECEIVING MONEY -->
            </div>
        </div>
    </div>
    <!--main div tag below-->
    </div>
</template>
<script>
import FlipCountdown from 'vue2-flip-countdown'
export default {
    components:{FlipCountdown},
    data(){
        return{
            is_loading:false,
            success_msg:'',
            error_msg:'',
            donation_view:true,
            pending_payment:true,
            pending_payment_b:true,
            pending_withdrawal:true,
            pending_withdrawal_b:true,
            money_pending_payments:[],
            bitcoin_pending_payments:[],
            money_pending_receiving:[],
            bitcoin_pending_receiving:[],
            endtime:'2020-09-13 19:00:00',
            expired:'',
            pop:[],
            paid:false,
            selected_files:[],
            timer_list:[],
            timer_listb:[],
            r_timer_list:[],
            r_timer_listb:[],
            block:[],
            blockb:[],
            receiver_msg:[],
            on_list_msg:'',
            popb:[],
            selected_filesb:[],
            close:false,
            msg_type:[],
            is_priority:[],
            closem:false
            
        }
    },
    methods:{
        toggle_view(){
            this.donation_view = !this.donation_view
        },
        BuildTransact(){
        this.is_loading = true
        axios.get('/dashboard/api/money-donate')
        .then(response=>{
            if(response.data.stat == 'no_pay_money'){
                this.pending_payment = false
                
            }
            else if(response.data.stat == 'good'){
                this.money_pending_payments = response.data.content
                for(var i = 0; i < this.money_pending_payments.length;i++){
                    this.pop.push({popbtn:false})
                }
                for(var i = 0; i < this.money_pending_payments.length;i++){
                    this.selected_files.push({selected_file:null})
                }
                
                
                for(var i = 0; i < this.money_pending_payments.length;i++){
                    var py_time = this.money_pending_payments[i].expiry_date
                    var ymd = py_time.slice(0,10)
                    var tt = py_time.slice(11, 19)
                    var time = ymd + ' ' + tt
                    this.timer_list.push({converted_time:time})
                    var date = new Date()
                    var adjusted_date = date.setHours(date.getHours() + 1)
                    var current_time = new Date(adjusted_date);
                    if( current_time > new Date(this.money_pending_payments[i].expiry_date)){
                        this.expired= "Time expired your account will be blocked"
                    }
                }
        
            }
            this.is_loading = false
        })
        .catch(err=>{
            this.is_loading = false
        })
    },
    BuildTransactB(){
        this.is_loading = true;
        axios.get('/dashboard/api/bitcoin-donate')
        .then(response=>{
            if(response.data.stat == 'no_pay_money'){
                this.pending_payment_b = false
                
            }
            else if(response.data.stat == 'good'){
                this.bitcoin_pending_payments = response.data.content
                for(var i = 0; i < this.bitcoin_pending_payments.length;i++){
                    this.popb.push({popbtn:false})
                }
                for(var i = 0; i < this.bitcoin_pending_payments.length;i++){
                    this.selected_filesb.push({selected_file:null})
                }
                
                for(var i = 0; i < this.bitcoin_pending_payments.length;i++){
                    var py_time = this.bitcoin_pending_payments[i].expiry_date
                    var ymd = py_time.slice(0,10)
                    var tt = py_time.slice(11, 19)
                    var time = ymd + ' ' + tt
                    this.timer_listb.push({converted_time:time})
                    
                    var date = new Date()
                    var adjusted_date = date.setHours(date.getHours() + 1)
                    
                    
                    var current_time = new Date(adjusted_date);
                    if( current_time > new Date(this.bitcoin_pending_payments[i].expiry_date)){
                        this.expired= "Time expired your account will be blocked"
                        
                    }
                }
        
            }
            this.is_loading = false
        })
        .catch(err=>{
            this.is_loading = false
        })
    },
    BuildReceivers(){
        this.is_loading = true
        axios.get('/dashboard/api/money-receive')
        .then(response=>{
            if(response.data.stat == 'no_receive_money'){
                this.pending_withdrawal = false
                
            }
            else if(response.data.stat == 'good'){
                
                this.money_pending_receiving = response.data.content
            }
            
            for(var i = 0; i < this.money_pending_receiving.length;i++){
                    this.block.push({block_btn:false})
                }
            for(var i = 0; i < this.money_pending_receiving.length;i++){
                    var py_time = this.money_pending_receiving[i].expiry_date
                    var ymd = py_time.slice(0,10)
                    var tt = py_time.slice(11, 19)
                    var time = ymd + ' ' + tt
                    this.r_timer_list.push({converted_time:time})
                    var date = new Date()
                    var adjusted_date = date.setHours(date.getHours() + 1)
                    var current_time = new Date(adjusted_date);
                    if( current_time > new Date(this.money_pending_receiving[i].expiry_date)){
                        this.block[i].block_btn = true
                        
                    }
                }
            this.check_stat()
            this.is_loading = false
        })
        .catch(err=>{
            this.is_loading = false
        })
    },
    BuildReceiversB(){
        this.is_loading = true
    
        axios.get('/dashboard/api/bitcoin-withdraw')
        .then(response=>{
            if(response.data.stat == 'no_receive_money'){
                this.pending_withdrawal_b = false
                
                
            }
            else if(response.data.stat == 'good'){
                
                
                this.bitcoin_pending_receiving = response.data.content
            }
            
            for(var i = 0; i < this.bitcoin_pending_receiving.length;i++){
                    this.blockb.push({block_btn:false})
                }
            for(var i = 0; i < this.bitcoin_pending_receiving.length;i++){
                    var py_time = this.bitcoin_pending_receiving[i].expiry_date
                    var ymd = py_time.slice(0,10)
                    var tt = py_time.slice(11, 19)
                    var time = ymd + ' ' + tt
                    this.r_timer_listb.push({converted_time:time})
                    
                    var date = new Date()
                    var adjusted_date = date.setHours(date.getHours() + 1)


                    var current_time = new Date(adjusted_date);
                    if( current_time > new Date(this.bitcoin_pending_receiving[i].expiry_date)){
                        this.blockb[i].block_btn = true
                        
                    }
                }
            this.is_loading = false
            
        })
        .catch(err=>{
            this.is_loading = false
            console.log('error:')
        })
    },
    check_stat(){
        if(!this.pending_payment && !this.pending_payment_b){
            if(this.pending_withdrawal || this.pending_withdrawal_b){
                this.donation_view = false
            }
            
        }
    },
    viewPop(index){
        this.closem = !this.closem
        var el = document.getElementsByClassName('proofm')[index]
        el.style.display = this.closem ? 'block': 'none';
        
    
    },
    viewPopb(index){
        this.close = !this.close
        var el = document.getElementsByClassName('proof')[index]
        el.style.display = this.close ? 'block': 'none';
        
        
    
    },
    displayMsg(){
        this.is_loading = true
        axios.get('/dashboard/api/display_msg')
        .then(response=>{
            if(response.data.stat == 'not_receiver'){
                this.receiver_msg = []
            }
            // else if(response.data.stat == 'on_list'){
            //     this.on_list_msg = 'Your name is currently on the receivers list'
            // }
            else if(response.data.stat == 'receiver'){
                var content;
                content = response.data.content
                
                
                for(var obj = 0; obj < content.length;obj++){
                
                    var r_amount = content[obj].amount
                    // var ld_amount = content[obj].amount / 1.5
                    // var d_amount = String(ld_amount).slice(0, 8)
                    
                    
                    this.msg_type.push(content[obj].receiving_type)
                    if(content[obj].is_priority){
                        this.is_priority.push('true')
                    }
                    var py_time = content[obj].date_start
                    var py_time2 = content[obj].date_end
                    var sd = py_time.slice(0,10)
                    var ed = py_time2.slice(0, 10)
                    this.receiver_msg.push({
                    r_amount:r_amount, start:sd, end:ed})
                }


            }
            this.is_loading = false
        })
        .catch(err=>{
            this.is_loading = false
            
        })
    },
    displayPop(index){
        this.pop[index].popbtn = true
    },
    displayPopb(index){
        this.popb[index].popbtn = true
    },
    fileUpload(event, index){
        this.selected_files[index].selected_file = event.target.files[0]
    },
    fileUploadb(event, index){
        this.selected_filesb[index].selected_file = event.target.files[0]
    },
    havePaid(index){
        let data = new FormData()
        data.append('picture', this.selected_files[index].selected_file)
        data.append('acct_name', this.money_pending_payments[index].account_name)
        data.append('phone', this.money_pending_payments[index].phone)
        data.append('amount', this.money_pending_payments[index].receiving_amount)
        this.is_loading = true
        axios.post('/dashboard/api/money-donate', data, {
            headers:{
                'Content-Type':'multipart/form-data'
            }
        })
        .then(response=>{
            this.is_loading = false
            if(response.data.status = 'alright'){
                this.success_msg = "Your investment process will be complete as soon as your are confirmed"
                setTimeout(() => {
                            window.location.reload()
                        }, 2000)
            }
            
        })
        .catch(err=>{
            this.is_loading = false
        })
    },
    havePaidb(index){
        let data = new FormData()
        data.append('picture', this.selected_filesb[index].selected_file)
        data.append('wallet', this.bitcoin_pending_payments[index].bitcoin_wallet)
        data.append('phone', this.bitcoin_pending_payments[index].phone)
        data.append('amount', this.bitcoin_pending_payments[index].receiving_amount)
        this.is_loading = true
        axios.post('/dashboard/api/bitcoin-donate', data, {
            headers:{
                'Content-Type':'multipart/form-data'
            }
        })
        .then(response=>{
            this.is_loading = false
            if(response.data.status = 'alright'){
                this.success_msg = "Your investment process will be complete as soon as your are confirmed"
                setTimeout(() => {
                            window.location.reload()
                        }, 2000)
            }
            
        })
        .catch(err=>{
            this.is_loading = false
        })
    },
    blockUser(index){
        this.is_loading = true
        axios.post('/dashboard/api/block', {
            blocked_user:this.money_pending_receiving[index].user,
            expiry_date:this.money_pending_receiving[index].expiry_date,
            unpaid_amount:this.money_pending_receiving[index].receiving_amount,
            transaction_type:this.money_pending_receiving[index].transaction_type
        })
        .then(response=>{
            this.is_loading = false
            if(response.data.stat == 'user_blocked'){
                this.success_msg = 'you will be matched to another member shortly'
                setTimeout(() => {
                            window.location.reload()
                        }, 2000)
            }
            else if(response.data.stat == "still_time"){
                this.error_msg = 'Cannot block user because the time has not expired'
            }
            
            
        })
        .catch(err=>{
            this.is_loading = false
            this.error_msg = 'something went wrong, please try again later'
            
        })

        
        
    },
    blockUserb(index){
        this.is_loading = true
        axios.post('/dashboard/api/block', {
            blocked_user:this.bitcoin_pending_receiving[index].user,
            expiry_date:this.bitcoin_pending_receiving[index].expiry_date,
            unpaid_amount:this.bitcoin_pending_receiving[index].receiving_amount,
            transaction_type:this.bitcoin_pending_receiving[index].transaction_type
        })
        .then(response=>{
            this.is_loading = false
            if(response.data.stat == 'user_blocked'){
                this.success_msg = 'you will be matched to another member shortly'
                setTimeout(() => {
                            window.location.reload()
                        }, 2000)
            }
            else if(response.data.stat == "still_time"){
                this.error_msg = 'Cannot block this user '
            }
            
        })
        .catch(err=>{
            this.is_loading = false
            this.error_msg = 'something went wrong, please try again later'
        })

        
        
    },
    confirmUser(index){
        this.is_loading = true
        axios.post('/dashboard/api/confirm', {
            payer:this.money_pending_receiving[index].user,
            amount:this.money_pending_receiving[index].receiving_amount,
            type:this.money_pending_receiving[index].transaction_type

        })
        .then(response=>{
            this.is_loading = false
            if(response.data.stat == 'alreaddy_confirmed'){
                this.success_msg = 'You have already confirmed this user'
            }
            else if(response.data.stat == 'success'){
                this.success_msg = 'Transaction successful'
            }
            setTimeout(() => {
                            window.location.reload()
                        }, 2000)
            
        })
        .catch(err=>{
            this.is_loading = false
            
        })
    },
    confirmUserb(index){
        this.is_loading = true
        axios.post('/dashboard/api/confirm', {
            payer:this.bitcoin_pending_receiving[index].user,
            amount:this.bitcoin_pending_receiving[index].receiving_amount,
            type:this.bitcoin_pending_receiving[index].transaction_type

        })
        .then(response=>{
            this.is_loading = false
            if(response.data.stat == 'alreaddy_confirmed'){
                this.success_msg = 'You have already confirmed this user'
            }
            else if(response.data.stat == 'success'){
                this.success_msg = 'Transaction successful'
            }
            setTimeout(() => {
                            window.location.reload()
                        }, 2000)
            
        })
        .catch(err=>{
            this.is_loading = false
            
        })
    }

    },
    created(){
        this.BuildTransact()
        this.BuildTransactB()
        this.BuildReceiversB()
        this.displayMsg()
        this.BuildReceivers()
        
    },
    
}
   
</script>