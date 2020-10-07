<template>
    <div>
        <div v-if="is_loading" id="loader"></div>
        <div v-else>
            <div>
                    <h4 class="side-stick">Donation Page</h4>
                    <div v-show="!no_list">
                        <p style="text-align:center"><b>Note: </b>The list will  close as soon as the timer runs out and will appear again by {{time_text}}. </p>
                        <flip-countdown v-bind:deadline="timer_disappear"></flip-countdown>
                        
                    </div>
                    <!-- <p class="info-area"><b>Note: you can only reserve a user whose receiving amount is equal to or greater than the amount you want to donate.</b></p> -->
                    <p class="info-area">Please type in the amount you want to donate and proceed to reserve a member on the receiver's list.&nbsp;<a href="#" style="color:#0a8cff">learn more</a></p>
                    <form class="rd-form">

                        <div v-if="donation_mode.use_naira" class="input-group mb-3">
                            <div class="input-group-prepend">
                              <span class="input-group-text" >&#8358;</span>
                            </div>
                            <input type="number" class="form-control" v-on:keyup="check_naira_amount" v-model="amount.naira" placeholder="Donate in Naira" aria-label="Amount (to the nearest dollar)">
                            <div class="input-group-append">
                              <span class="input-group-text" >.00</span>
                            </div>
                            <br><i v-if="amount_enough.naira" style='color:green;' class="info-msg" >Good job, now reserve any user of your choice!</i>
                           <span v-else>
                               <i v-if="amount_much.naira" class="info-msg" style='font-size:12px;'>Please enter an amount less than &#8358;500,000 before reserving a user</i>
                                <i v-else class="info-msg" style='font-size:12px;'>Please enter an amount not less than &#8358;10,000 before reserving a user</i>
                            </span>
                          </div>
                          <div v-else>
                          <div  class="input-group mb-3">
                            <div class="input-group-prepend">
                              <span class="input-group-text"><i class="fa fa-bitcoin"></i></span>
                            </div>
                            <input type="number" placeholder="Donate in bitcoins" v-on:keyup="check_bitcoin_amount" v-model="amount.bitcoin" class="form-control" aria-label="Amount (to the nearest dollar)">

                          </div>
                            <i v-if="amount_enough.bitcoin"  class="info-msg" style='color:green;font-size:12px;'>Good job, now reserve any user of your choice!</i>
                            <span v-else>
                               <i v-if="amount_much.bitcoin" class="info-msg" style='font-size:12px;'>Please enter an amount less than 0.13 BTC before reserving a user</i>
                                <i v-else class="info-msg" style='font-size:12px;'>Please enter an amount not less than 0.0026 BTC before reserving a user</i>
                            </span>
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
                    <p><span style="color:green;">Success <i class="fa fa-check"></i></span>&nbsp;{{success_msg}}</p>
                </div>
                <div v-show="error_msg" class="alert alert-warning">
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    &times;
                </button>
                    <p><b>Failed!</b>&nbsp; {{error_msg}}</p>
                </div>
                
            <div v-if="no_list" style="text-align:center;font-weight:bold;color:#000000">
                     <flip-countdown v-bind:deadline="next_list_time"></flip-countdown>
                    <p>The receiver's list will appear as soon as the countdown runs out which is by {{time_text}}. </p>
                    <p>While you wait for the list, ensure you have entered your phone number and bank account details in the profile section. For more information on how to donate please go to the Frequently Asked Question (FAQ) section</p> 
            </div>
            <div v-else>
                <div v-show="donation_mode.use_naira" class="table-responsive cash-table" style="font-size:12px;">
                    <table class="table">
                        <thead class="thead-dark"></thead>
                          <tr class="tableRow">
                            <th scope="col">S/N</th>
                            <th scope="col">Action</th>
                            <th scope="col">Transaction type </th>
                            <th scope="col">Receiving Amount</th>
                            <th scope="col">Username</th>
                          </tr>

                        <tbody>
                          <tr v-for="(receiver, index) in money_receivers">
                            <th scope="row">{{index+1}}</th>
                            <td><button v-if="amount_enough.naira" type="button"
                                class="btn btn-danger" @click.prevent="reserve(index)">Reserve
                            </button>
                            <button v-else type="button"
                                    class="btn btn-danger" @click.prevent="alert_low_naira">Reserve
                            </button>
                            </td>
                            
                            <td>&#8358;</td>
                            <td>{{receiver.amount}}</td>
                            <td>{{receiver.name}}</td>
                            
                          </tr>
                          <tr v-show="empty_list">
                            <td  colspan="100%" class="text-center">All available Naira receivers on the list have been reserved, please look out for the next list by {{time_text}}.</td>
                        </tr>

                        </tbody>
                      </table>
                </div>
                <div v-show="donation_mode.use_bitcoin" class="table-responsive bitcoin-table" style="font-size:12px;">
                  <table class="table">
                      <thead class="thead-dark"></thead>
                        <tr style="background-color:#0a8cff;color:#ffffff">
                          <th scope="col">S/N</th>
                          <th scope="col">Action</th>
                          <th scope="col">Transaction type </th>
                          <th scope="col">Receiving Amount</th>
                          <th scope="col">Username</th>
                        </tr>

                      <tbody>
                        <tr v-for="(receiver, index) in bitcoin_receivers">
                          <th scope="row">{{index+1}}</th>
                          <td><button v-if="amount_enough.bitcoin" type="button"
                              class="btn btn-danger" @click.prevent="reserveb(index)">Reserve
                      </button>
                       <button v-else type="button"
                                class="btn btn-danger" @click.prevent="alert_low_bitcoin">Reserve
                        </button>
                        </td>
                          
                          <td><i class="fa fa-bitcoin"></i></td>
                          <td>{{receiver.amount}}</td>
                          <td>{{receiver.name}}</td>
                        </tr>
                        <tr>
                            <td v-show="empty_listb" colspan="100%" class="text-center">All available Bitcoin receivers on the list have been reserved, please look out for the next list by {{time_text}}.</td>
                        </tr>

                      </tbody>
                    </table>
              </div>
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
            amount_much:{
                naira:false,
                bitcoin:false
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
            is_loading:false,
            timer_appear:'',
            timer_disappear:'',
            no_list:true,
            next_list_time:'',
            time_text:'',
            empty_list:false,
            empty_listb:false
        }
    },
    methods:{
        timerToggle(){
            this.is_loading = true
            axios.get('/dashboard/api/timer')
            .then(response=>{
                var py_time_start = response.data.list_appear
                var py_time_end = response.data.list_disappear
                var ymd = py_time_start.slice(0,10)
                var tt = py_time_start.slice(11, 19)
                this.timer_appear = ymd + " " + tt
                var ymd = py_time_end.slice(0,10)
                var tt = py_time_end.slice(11, 19)
                this.timer_disappear = ymd + " " + tt

                var py_time = response.data.list_next_time
                var ymd = py_time.slice(0,10)
                var tt = py_time.slice(11, 19)
                this.next_list_time = ymd + ' ' + tt
                this.time_text = response.data.text
                if(new Date > new Date(response.data.list_appear) && new Date() < new Date(response.data.list_disappear)){
                    this.BuildList()
                    this.BuildList2()
                    this.no_list = false
                }
                else{
                this.no_list = true
                }
                this.is_loading = false
            })
            .catch(err=>{
                console.log('err')
                this.is_loading = false
        
            })
        },
        BuildList(){
            this.is_loading  = true
            axios.get('/dashboard/api/money')
            .then(response=>{
            
                this.money_receivers = response.data.content
                if (response.data.remnant == 'True'){
                    this.money.payer_remnant_bal = true
                }
                if(response.data.stat == 'empty'){
                    this.empty_list = true
                }
                this.is_loading = false
                
            })
            .catch(err=>{
                this.is_loading = false
                console.log('err')
            })
        },
        BuildList2(){
            this.is_loading  = true
            axios.get('/dashboard/api/bitcoin')
            .then(response=>{
                
                this.bitcoin_receivers = response.data.content
                if (response.data.remnant == 'True'){
                    this.bitcoin.payer_remnant_bal = true
                }
                if(response.data.stat == 'empty'){
                    this.empty_listb = true
                }
                this.is_loading = false
                
            })
            .catch(err=>{
                console.log('err')
            })
        },
        toggle_donation_mode(){
            this.donation_mode.use_naira = !this.donation_mode.use_naira
            this.donation_mode.use_bitcoin = !this.donation_mode.use_bitcoin
        },
        check_naira_amount(){
            if (this.amount.naira >= 10000 && this.amount.naira > 1 && this.amount.naira <= 500000 || this.money.payer_remnant_bal ){
                this.amount_enough.naira = true
                this.amount_much.naira = false
            }
            else if(this.amount.naira > 500000){
                this.amount_enough.naira = false
                this.amount_much.naira = true
            }
            else{
                this.amount_enough.naira = false
                this.amount_much.naira = false
            }
        },
        check_bitcoin_amount(){
            if(this.amount.bitcoin >= 0.0026 && this.amount.bitcoin != null && this.amount.bitcoin <= 0.13 || this.bitcoin.payer_remnant_bal ){
                this.amount_enough.bitcoin = true
                this.amount_much.bitcoin = false
            }
            else if(this.amount.bitcoin > 0.13){
                this.amount_enough.bitcoin = false
                this.amount_much.bitcoin = true
            }
            else{
                this.amount_enough.bitcoin = false
                this.amount_much.bitcoin = false
            }
        },
        alert_low_naira(){
            alert('Please enter a donation amount that is greater than or equal to NGN10,000 and less than NGN500,000')
        },
        alert_low_bitcoin(){
            alert('Please enter a donation amount that is greater than or equal to 0.0026BTC and less than 0.13')
        },
        
        reserve(index){
           var check = confirm(`Are you sure you want to donate NGN${this.amount.naira} to ${this.money_receivers[index].name}`)
           if (check){

           
            this.is_loading = true
            if(this.amount.naira >= 10000 && this.amount.naira > 1 && this.amount.naira <= 500000 || this.money.payer_remnant_bal ){
                
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
                
        
        
                
                axios.post('/dashboard/api/money', {
                    r_remnant : this.money.receiver_remnant,
                    user_pay : this.money.user_pay,
                    p_remnant : this.money.payer_remnant,
                    receiver : this.money_receivers[index].name
                })
                .then(response=>{
                    this.BuildList()
                    if(response.data.stat == 'good'){
                        this.success_msg = `You have pledged to donate NGN${this.money.user_pay} to ${this.money_receivers[index].name}, go to your dashboard to get ${this.money_receivers[index].name}'s bank details and make payment`
                    }
                    else if(response.data.stat == "taken"){
                        this.error_msg = `${this.money_receivers[index].name} has already been reserved and is no longer on the list, pick another member`
                    }
                    else if(response.data.stat == "still_on_list"){
                        this.error_msg = `You cannot reserve a member if you still have pending transactions`
                    }
                    else if(response.data.stat == "amount_changed"){
                        this.error_msg = `This members receiving amount has been updated, try and make the reservation again`
                    }
                    else if(response.data.stat == "mod2"){
                        this.error_msg = `This members receiving amount has been updated, try and make the reservation again`
                    }
                    else if(response.data.stat == "no_testimony"){
                        this.error_msg = `You are required to write a testimony after receiving your ROI before making another donation!`
                    }
                    else if(response.data.stat == "reserved_in_bit"){
                        this.error_msg = `You cannot reserve a member with Naira and Bitcoin at the same time`
                    }
                    else if(response.data.stat == "mod"){
                        this.error_msg = `${this.money_receivers[index].name} has already been reserved and is no longer on the list, pick another member`
                    }
                    else if(response.data.stat == "no_account_details"){
                        this.error_msg = `You must add your bank details and phone number in the profile page section before you reserve a member`
                    }
                    
                })
                .catch(err=>{
                    console.log('err')
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
                
        
        
                
                axios.post('/dashboard/api/bitcoin', {
                    r_remnant : this.bitcoin.receiver_remnant,
                    user_pay : this.bitcoin.user_pay,
                    p_remnant : this.bitcoin.payer_remnant,
                    receiver : this.bitcoin_receivers[index].name
                })
                .then(response=>{
                    this.BuildList2()
                    if(response.data.stat == 'good'){
                        this.success_msg = `You have pledged to donate ${this.bitcoin.user_pay}btc to ${this.bitcoin_receivers[index].name}, go to your dashboard to get ${this.bitcoin_receivers[index].name}'s wallet details and make payment`
                    }
                    else if(response.data.stat == "taken"){
                        this.error_msg = `${this.bitcoin_receivers[index].name} has already been reserved and is no longer on the list, pick another member`
                    }
                    else if(response.data.stat == "still_on_list"){
                        this.error_msg = `You cannot reserve a member if you still have pending transactions`
                    }
                    else if(response.data.stat == "amount_changed"){
                        this.error_msg = `This members receiving amount has been updated, try and make the reservation again`
                    }
                    else if(response.data.stat == "no_testimony"){
                        this.error_msg = `You are required to write a testimony after receiving your ROI before making another donation!`
                    }
                    else if(response.data.stat == "mod"){
                        this.error_msg = `${this.bitcoin_receivers[index].name} has already been reserved and is no longer on the list, pick another member`
                    }
                    else if(response.data.stat == "reserved_in_naira"){
                        this.error_msg = `You cannot reserve a member with Naira and Bitcoin at the same time`
                    }
                    else if(response.data.stat == "no_account_details"){
                        this.error_msg = `you must add your bitcoin wallet address and phone number in the profile page section before you reserve a member`
                    }
                    
                })
                .catch(err=>{
                    console.log('bberror')
                })

                
            }
            else{
                this.alert_low_naira()
            }
           }
        },
        
    },
     created(){
        this.timerToggle()
        
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