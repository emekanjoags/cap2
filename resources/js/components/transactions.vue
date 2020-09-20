<template>
    <div>
         <div v-if="is_loading" id="loader"></div>
         <div else>
             <div class="toggle">
                <button v-if="donation_view" class="btn btn-danger" @click="toggle_view">Donations</button><button v-else class="btn btn-outline-danger" @click="toggle_view">Donations</button>
                 &nbsp;<button v-if="donation_view" class="btn btn-outline-danger"  @click="toggle_view">Withdrawals</button><button v-else class="btn btn-danger"  @click="toggle_view">Withdrawals</button>
            </div>
            <div v-if="donation_view">
                <div v-if="no_transact">You have no completed donations</div>
                <div v-else>
                    <div class="col-md-4 list" v-for="(transact, index) in donations">
                         <ul>
                             <li> Username: {{transact.receivers_name}}<li>
                             <div v-if="transact.transaction_type == 1">
                                <li>Account Name: {{transact.account_name}}</li>
                                <li>Bank Name: {{transact.bank}}</li>
                                <li>Account Number: {{transact.account_number}}</li>
                                <li>Amount: &#8358;{{receiving_amount}}</li>
                            </div>
                            <div v-else>
                                <li>Wallet ID: {{transact.bitcoin_wallet}}</li>
                                <li>Amount: BTC {{transact.receiving_amount}}</li>
                            </div>
                             <li>Date: {{transact.date_reserved}}</li>
                             <li>Phone: {{transact.phone}}</li>
                             <li>Status: <span v-if="transact.have_received">Confirmed</span><span v-else>Awaiting confirmation</span></li>
                         </ul><br>

                    </div>
                </div>
            </div>

            <div v-else>
                <div v-if="no_withdraw">No member has paid you yet</div>
                <div v-else>
                    <div class="col-md-4 list" v-for="(transact, index) in withdrawals">
                     <ul>
                         <li>Username: {{transact.givers_name}}</li>
                         <li v-if="transact.transaction_type == 1">Amount: &#8358;{{transact.receiving_amount}}</li>
                         <li v-else>Amount: BTC {{transact.receiving_amount}}</li>
                         <li>Date: {{transact.date_reserved}}</li>
                         <li>Phone: {{transact.givers_phone}}</li>
                         <li>Status: Received</li>
                     </ul><br>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    data(){
        return{
            donations:[],
            withdrawals:[],
            donation_view:true,
            is_loading:false,
            no_transact:false,
            no_withdraw:false,
            r_timer_list:[],
            timer_list:[],

        }
    },
    methods:{
        toggle_view(){
            this.donation_view = !this.donation_view
        },
        GetDonations(){
            this.is_loading = true
            axios.get('/dashboard/api/transact')
            .then(response=>{
                if(response.data.stat == 'empty'){
                    this.no_transact = true
                    console.log('empty')
                }
                else if(response.data.stat == 'good'){
                    this.donations = response.data.content
                    for(var i = 0; i < this.donations.length;i++){
                    var py_time = this.donations[i].date_reserved
                    var ymd = py_time.slice(0,10)
                    var time = ymd
                    this.donations[i].date_reserved = time
                    this.timer_list.push({converted_time:time})
                    console.log('jvt: ' + time)
                    console.log('good')
                    }
                }
                this.is_loading = false
            })
            .catch(err=>{
                this.is_loading = false
                console.log(err)
            })
        },
        GetWithdrawal(){
            this.is_loading = true
            axios.get('/dashboard/api/transactw')
            .then(response=>{
                if(response.data.stat == 'empty'){
                    this.no_withdraw = true
                    console.log('empty')
                }
                else if(response.data.stat == 'good'){
                    this.withdrawals = response.data.content
                    for(var i = 0; i < this.withdrawals.length;i++){
                    var py_time = this.withdrawals[i].date_reserved
                    var ymd = py_time.slice(0,10)
                    var time = ymd
                    this.withdrawals[i].date_reserved = time
                    this.timer_list.push({converted_time:time})
                    console.log('jvt: ' + time)
                    console.log('good')
                    }
                    console.log(response.data.content)
                    console.log(new Date())
                    console.log('good')
                }
                this.is_loading = false
            })
            .catch(err=>{
                this.is_loading = false
                console.log(err)
            })
        }
    },
    created(){
        this.GetWithdrawal()
        this.GetDonations()
        
        
    }
}
</script>