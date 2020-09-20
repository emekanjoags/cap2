<template>
    <div>
        <div v-if="is_loading" id="loader"></div>
        <div v-else>
            <div>
                    <h4 class="side-stick">Donation Page</h4>
                    <div>
                        <flip-countdown v-bind:deadline="timer"></flip-countdown>
                    </div>
                    <!-- <p class="info-area"><b>Note: you can only reserve a user whose receiving amount is equal to or greater than the amount you want to donate.</b></p> -->
                    <p class="info-area">Please type in the amount you want to donate and proceed to reserve a member.&nbsp;<a href="#" style="color:#0a8cff">learn more</a></p>
                    <form class="rd-form">

                        <div v-if="donation_mode.use_naira" class="input-group mb-3">
                            <div class="input-group-prepend">
                              <span class="input-group-text" >&#8358;</span>
                            </div>
                            <input type="text" class="form-control" v-on:keyup="check_naira_amount" v-model="amount.naira" placeholder="Donate in Naira" aria-label="Amount (to the nearest dollar)">
                            <div class="input-group-append">
                              <span class="input-group-text" >.00</span>
                            </div>
                            <br><i v-if="amount_enough.naira" style='color:green;' class="info-msg" >Good job, now reserve any user of your choice!</i>
                            <i v-else class="info-msg" style='font-size:12px;'>Please enter an amount not less than &#8358;10,000 before reserving a user</i>
                          </div>
                          <div v-else>
                          <div  class="input-group mb-3">
                            <div class="input-group-prepend">
                              <span class="input-group-text"><i class="fa fa-bitcoin"></i></span>
                            </div>
                            <input type="text" placeholder="Donate in bitcoins" v-on:keyup="check_bitcoin_amount" v-model="amount.bitcoin" class="form-control" aria-label="Amount (to the nearest dollar)">

                          </div>
                            <i v-if="amount_enough.bitcoin"  class="info-msg" style='color:green;font-size:12px;'>Good job, now reserve any user of your choice!</i>
                            <i v-else class="info-msg" style='font-size:12px;'>Please enter an amount not less than 0.0026BTC before reserving a user</i>
                          </div>
                          <div style="text-align:center;">
                              <h4 style="font-weight:bold">or</h4>
                          </div>
                          <div style="text-align:center;margin-bottom:10px;">
                            <button v-if="donation_mode.use_naira" class="btn btn-dark btn-block white-text" @click.prevent='toggle_donation_mode'> Donate with Bitcoin</button>
                            <button v-else @click.prevent="toggle_donation_mode" class="btn btn-dark btn-block white-text"> Donate with Naira</button>
                        </div>

                    </form>
                </div>
                <div v-show="success_msg" class="alert alert-success">
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    &times;
                </button>
                    {{success_msg}}
                </div>
                <div v-show="error_msg" class="alert alert-warning">
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    &times;
                </button>
                    {{error_msg}}
                </div>
                <br><br>
                <div v-show="donation_mode.use_naira" class="table-responsive cash-table">
                    <table class="table">
                        <thead class="thead-dark"></thead>
                          <tr class="tableRow">
                            <th scope="col">S/N</th>
                            <th scope="col">Username</th>
                            <th scope="col">Transaction type </th>
                            <th scope="col">Receiving Amount</th>
                            <th scope="col">Action</th>
                          </tr>

                        <tbody>
                          <tr v-for="(receiver, index) in money_receivers">
                            <th scope="row">{{index+1}}</th>
                            <td>{{receiver.name}}</td>
                            <td>&#8358;</td>
                            <td>{{receiver.amount}}</td>
                            <td><button v-if="amount_enough.naira" type="button"
                                class="btn btn-danger" @click.prevent="reserve(index)">Reserve
                        </button>
                        <button v-else type="button"
                                class="btn btn-danger" @click.prevent="alert_low_naira">Reserve
                        </button>
                        </td>
                          </tr>

                        </tbody>
                      </table>
                </div>
                <div v-show="donation_mode.use_bitcoin" class="table-responsive bitcoin-table">
                  <table class="table">
                      <thead class="thead-dark"></thead>
                        <tr style="background-color:#0a8cff;color:#ffffff">
                          <th scope="col">S/N</th>
                          <th scope="col">Username</th>
                          <th scope="col">Transaction type </th>
                          <th scope="col">Receiving Amount</th>
                          <th scope="col">Action</th>
                        </tr>

                      <tbody>
                        <tr v-for="(receiver, index) in bitcoin_receivers">
                          <th scope="row">{{index+1}}</th>
                          <td>{{receiver.name}}</td>
                          <td><i class="fa fa-bitcoin"></i></td>
                          <td>{{receiver.amount}}</td>
                          <td><button v-if="amount_enough.bitcoin" type="button"
                              class="btn btn-danger" @click.prevent="reserveb(index)">Reserve
                      </button>
                       <button v-else type="button"
                                class="btn btn-danger" @click.prevent="alert_low_bitcoin">Reserve
                        </button>
                        </td>
                        </tr>

                      </tbody>
                    </table>
              </div>
        </div>
            
    </div>
</template>
<script>
import FlipCountdown from 'vue2-flip-countdown'
export default {
    components: { FlipCountdown },
    data(){
        return{
            donation_mode:{
                use_naira:true,
                use_bitcoin:false
            },
            amount:{
                naira:'',
                bitcoin:''
            },
            amount_enough:{
                naira:false,
                bitcoin:false
            },
            timer:'2020-09-10 15:30:00',
            money_receivers:[],
            bitcoin_receivers:[],
            money:{
                receiver_remnant:'',
                uer_pay:'',
                payer_remnant:'',
                payer_remnant_bal:false
            },
            bitcoin:{
                receiver_remnant:'',
                uer_pay:'',
                payer_remnant:'',
                payer_remnant_bal:false
            },
            amount_top_pay:[],
            success_msg:'',
            error_msg:'',
            is_loading:false
        }
    },
    methods:{
        BuildList(){
            this.is_loading  = true
            axios.get('/dashboard/api/money')
            .then(response=>{
                console.log(response)
                this.money_receivers = response.data.content
                if (response.data.remnant == 'True'){
                    this.money.payer_remnant_bal = true
                }
                this.is_loading = false
                console.log('receivers: ' + this.money_receivers)
            })
            .catch(err=>{
                this.is_loading = false
                console.log('error: ' + err)
            })
        },
        BuildList2(){
            this.is_loading  = true
            axios.get('/dashboard/api/bitcoin')
            .then(response=>{
                console.log(response)
                this.bitcoin_receivers = response.data.content
                if (response.data.remnant == 'True'){
                    this.bitcoin.payer_remnant_bal = true
                }
                this.is_loading = false
                console.log('receivers: ' + this.bitcoin_receivers)
            })
            .catch(err=>{
                console.log('berror: ' + err)
            })
        },
        toggle_donation_mode(){
            this.donation_mode.use_naira = !this.donation_mode.use_naira
            this.donation_mode.use_bitcoin = !this.donation_mode.use_bitcoin
        },
        check_naira_amount(){
            if (this.amount.naira >= 10000 || this.money.payer_remnant_bal && this.amount.naira > 1){
                this.amount_enough.naira = true
            }
            else{
                this.amount_enough.naira = false
            }
        },
        check_bitcoin_amount(){
            if(this.amount.bitcoin >= 0.0026 || this.bitcoin.payer_remnant_bal && this.amount.bitcoin != null){
                this.amount_enough.bitcoin = true
            }
            else{
                this.amount_enough.bitcoin = false
            }
        },
        alert_low_naira(){
            alert('Please enter a donation amount that is greater than or equal to NGN10,000')
        },
        alert_low_bitcoin(){
            alert('Please enter a donation amount that is greater than or equal to 0.0026BTC')
        },
        reserve(index){
           var check = confirm(`Are you sure you want to donate NGN${this.amount.naira} to ${this.money_receivers[index].name}`)
           if (check){

           
            this.is_loading = true
            if(this.amount.naira >= 10000 || this.money.payer_remnant_bal && this.amount.naira > 1){
                
                if (this.money_receivers[index].amount > this.amount.naira){
                    
                    this.money.receiver_remnant = this.money_receivers[index].amount - this.amount.naira
                    this.money.user_pay = this.amount.naira
                    this.amount.naira = 0
                    this.money.payer_remnant = 0
                }
                else if(this.money_receivers[index].amount < this.amount.naira){
                    this.money.payer_remnant = this.amount.naira - this.money_receivers[index].amount
                    this.amount.naira =  this.money.payer_remnant
                    this.money.user_pay = this.money_receivers[index].amount
                    this.money_receivers[index].amount = 0
                    this.money.receiver_remnant = 0

                }
                else if(this.money_receivers[index].amount == this.amount.naira){
                    
                    this.money.user_pay = this.amount.naira
                    this.money.receiver_remnant = 0
                    this.money.payer_remnant = 0
                    this.amount.naira = 0

                }
                console.log('r_remnat ' + this.money.receiver_remnant)
                console.log('p_remnat ' + this.money.payer_remnant)
                console.log('user_pay ' + this.money.user_pay)
                console.log('id ' + this.money_receivers[index].id)
                console.log('id ' + this.money_receivers[index].name)
                axios.post('/dashboard/api/money', {
                    r_remnant : this.money.receiver_remnant,
                    user_pay : this.money.user_pay,
                    p_remnant : this.money.payer_remnant,
                    receiver : this.money_receivers[index].name
                })
                .then(response=>{
                    this.BuildList()
                    if(response.data.stat == 'good'){
                        this.success_msg = `You have successfully pledged to donate NGN${this.money.user_pay} to ${this.money_receivers[index].name}, you have NGN${this.money.payer_remnant} left to donate, go to your dashboard to get ${this.money_receivers[index].name}'s bank details and make payment`
                    }
                    else if(response.data.stat == "taken"){
                        this.error_msg = `${this.money_receivers[index].name} has already been reserved, pick another one`
                    }
                    else if(response.data.stat == "still_on_list"){
                        this.error_msg = `You cannot reserve a member if you still have pending transactions`
                    }
                    else if(response.data.stat == "reserved_in_bit"){
                        this.error_msg = `You cannot reserve a member with Naira and Bitcoin at the same time`
                    }
                    else if(response.data.stat == "no_account_details"){
                        this.error_msg = `Please add your bank details and phone number in the profile page section before you reserve a member`
                    }
                    
                })
                .catch(err=>{
                    console.log('error: ' + err)
                })

                
            }
            else{
                this.alert_low_naira()
            }
           }
        },
        reserveb(index){
            var check = confirm(`Are you sure you want to donate ${this.amount.bitcoin}btc to ${this.bitcoin_receivers[index].name}`)
           if (check){
            this.is_loading = true
            if(this.amount.bitcoin >= 0.0026 || this.bitcoin.payer_remnant_bal && this.amount.bitcoin != null){
                
                if (this.bitcoin_receivers[index].amount > this.amount.bitcoin){
                    
                    this.bitcoin.receiver_remnant = this.bitcoin_receivers[index].amount - this.amount.bitcoin
                    this.bitcoin.user_pay = this.amount.bitcoin
                    this.amount.bitcoin = 0
                    this.bitcoin.payer_remnant = 0
                }
                else if(this.bitcoin_receivers[index].amount < this.amount.bitcoin){
                    this.bitcoin.payer_remnant = this.amount.bitcoin - this.bitcoin_receivers[index].amount
                    this.amount.bitcoin=  this.bitcoin.payer_remnant
                    this.bitcoin.user_pay = this.bitcoin_receivers[index].amount
                    this.bitcoin_receivers[index].amount = 0
                    this.bitcoin.receiver_remnant = 0

                }
                else if(this.bitcoin_receivers[index].amount == this.amount.bitcoin){
                    
                    this.bitcoin.user_pay = this.amount.bitcoin
                    this.bitcoin.receiver_remnant = 0
                    this.bitcoin.payer_remnant = 0
                    this.amount.bitcoin = 0

                }
                console.log('r_remnat ' + this.bitcoin.receiver_remnant)
                console.log('p_remnat ' + this.bitcoin.payer_remnant)
                console.log('user_pay ' + this.bitcoin.user_pay)
                console.log('id ' + this.bitcoin_receivers[index].id)
                console.log('id ' + this.bitcoin_receivers[index].name)
                axios.post('/dashboard/api/bitcoin', {
                    r_remnant : this.bitcoin.receiver_remnant,
                    user_pay : this.bitcoin.user_pay,
                    p_remnant : this.bitcoin.payer_remnant,
                    receiver : this.bitcoin_receivers[index].name
                })
                .then(response=>{
                    this.BuildList2()
                    if(response.data.stat == 'good'){
                        this.success_msg = `You have successfully pledged to donate ${this.bitcoin.user_pay}btc to ${this.bitcoin_receivers[index].name} successfully, you have ${this.bitcoin.payer_remnant}BTC left to donate, go to your dashboard to get ${this.bitcoin_receivers[index].name}'s wallet details and make payment`
                    }
                    else if(response.data.stat == "taken"){
                        this.error_msg = `${this.bitcoin_receivers[index].name} has already been reserved, pick another one`
                    }
                    else if(response.data.stat == "still_on_list"){
                        this.error_msg = `You cannot reserve a member if you still have pending transactions`
                    }
                    else if(response.data.stat == "reserved_in_naira"){
                        this.error_msg = `You cannot reserve a member with Naira and Bitcoin at the same time`
                    }
                    else if(response.data.stat == "no_account_details"){
                        this.error_msg = `Please add your bitcoin wallet address and phone number in the profile page section before you reserve a member`
                    }
                    
                })
                .catch(err=>{
                    console.log('bberror: ' + err)
                })

                
            }
            else{
                this.alert_low_naira()
            }
           }
        },
        
    },
     created(){
        this.BuildList()
        this.BuildList2()
    },
}
</script>
<style scoped>
.tableRow{
    background:#0a8cff;
    color:#ffffff
}
.white-text{
    color:#ffffff
}
.info-msg{
    color:red;
    font-size:14px;
}
</style>