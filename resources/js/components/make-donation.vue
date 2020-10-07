<template>
    <div>
        <div v-if="is_loading" id="loader"></div>
        <div v-else>
        
        <div v-if="investors">
            <p><b>Note: </b>You cannot make more than one investment at the same time</p>
            <p>Your current investment is:</p>
            <div  class="package-area"  v-for="investor in investors">
                        <h6 style="text-align:center;"><b v-if="investor.package == 1" class="package" style="background:#054680;">Standard Package</b><b v-else class="package" style="background:purple;">Standard Package</b></h6>
                        <br><p v-if="investor.transaction_type == 1"><span>Amount: &#8358;<span v-if="!investor.matched">{{investor.amount}}</span><span v-else>{{investor.invested_amt}}</span> - <span v-if="investor.package == 1">(50% ROI in 7days)</span><span v-else>(30% ROI in 7days)</span></span></p>
                        <p v-else><span>Amount: <i class="fa fa-btc"></i> <span v-if="!investor.matched">{{investor.amount}}</span><span v-else>{{investor.invested_amt}}</span> - <span v-if="investor.package == 1">(50% ROI in 7days)</span><span v-else>(50% ROI in 7days)</span></span></p>
                        <p>Status: <b v-if="!investor.matched">Not Matched</b><span v-else><span v-if="investor.completed" style="color:green;font-weight:bold">Invested(awaiting ROI)</span><span v-else style="color:orange;font-weight:bold">Matched</span></span></p>
            </div><br>
            <div v-show="error_msg" class="alert alert-warning">
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    &times;
                </button>
                    <p><b>Failed!</b>&nbsp; {{error_msg}}</p>
            </div>
        </div>
        <div v-show="!investors">
            <div>
                <h6>Available Packages</h6>
                <div  class="package-area">
                    <h6 style="text-align:center;"><b class="package" style="background:#054680;">Standard Package</b></h6>
                    <br><p><span> &#8358;2000 - &#8358;49,999 (50% ROI in 7days)</span></p>
                    <p><span> <i class="fa fa-btc"></i> 0.0045 - 0.0035 (50% ROI in 7days)</span></p>
                </div><br>
                <div  class="package-area">
                    <h6 style="text-align:center;"><b class="package" style="background:purple;">Premium Package</b></h6>
                    <br><p><span>  &#8358;50,000 - &#8358;500,000 (30% ROI in 7days)</span></p>
                    <p><span> <i class="fa fa-btc"></i> 0.0045 - 0.05 (30%  ROI in 7days)</span></p>
                </div>
                
            </div><br><hr>
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
            <h6>Current Package:</h6>
            <p v-show="naira_amount_stat.standard"><span><b class="package" style="background:#054680;font-size:10px;">Standard Package</b><span>&#8358;2000 - 49,999</span></span>&nbsp;<i style="color:green" class="fa fa-check"></i></p>
            <p v-show="naira_amount_stat.premium"><span><b class="package" style="background:purple;font-size:10px;">Premium Package</b><span>&#8358;50,000 - 500,000</span></span>&nbsp;<i style="color:green" class="fa fa-check"></i></p>
            <p v-show="bitcoin_amount_stat.standard"><span><b class="package" style="background:#054680;font-size:10px;">Standard Package</b><span>BTC 000.49 - 0.0119</span></span>&nbsp;<i style="color:green" class="fa fa-check"></i></p>
            <p v-show="bitcoin_amount_stat.premium"><span><b class="package" style="background:purple;font-size:10px;">Premium Package</b><span>BTC 0.012 - 0.13</span></span>&nbsp;<i style="color:green" class="fa fa-check"></i></p>
        </div>

        <form class="rd-form" v-show="!investors">

                        <div v-if="donation_mode.use_naira" class="input-group mb-3">
                            <div class="input-group-prepend">
                              <span class="input-group-text" >&#8358;</span>
                            </div>
                            <input type="number" class="form-control" v-on:keyup="check_naira_amount" v-model="amount.naira" placeholder="Donate in Naira" aria-label="Amount (to the nearest dollar)">
                            <div class="input-group-append">
                              <span class="input-group-text" >.00</span>
                            </div>
                            <br><i v-if="naira_amount_stat.standard || naira_amount_stat.premium" style='color:green;' class="info-msg" >Good job, now click "Make Investment"</i>
                           <span v-else>
                               <i v-if="naira_amount_stat.low" class="info-msg" style='font-size:12px;'>Please enter an amount not less than &#8358;2,000</i>
                                <i v-else class="info-msg" style='font-size:12px;'>Please enter an amount not greater than &#8358;500,000</i>
                            </span>
                        </div>
                        <div v-else>
                          <div  class="input-group mb-3">
                            <div class="input-group-prepend">
                              <span class="input-group-text"><i class="fa fa-bitcoin"></i></span>
                            </div>
                            <input type="number" placeholder="Donate in bitcoins" v-on:keyup="check_bitcoin_amount" v-model="amount.bitcoin" class="form-control" aria-label="Amount (to the nearest dollar)">

                          </div>
                            <i v-if="bitcoin_amount_stat.standard || bitcoin_amount_stat.premium"  class="info-msg" style='color:green;font-size:12px;'>Good job, now click "Make Investment"</i>
                            <span v-else>
                               <i v-if="bitcoin_amount_stat.high" class="info-msg" style='font-size:12px;'>Please enter an amount less than 0.13 BTC before reserving a user</i>
                                <i v-else class="info-msg" style='font-size:12px;'>Please enter an amount not less than 0.00049 BTC before reserving a user</i>
                            </span>
                        </div>
                        <div v-if="donation_mode.use_naira">
                            <button v-show="naira_amount_stat.low || naira_amount_stat.high" class="btn btn-danger btn-block" @click.prevent="low_naira()"> Make Investment</button><button v-show="naira_amount_stat.standard || naira_amount_stat.premium" @click.prevent="investNaira()" class="btn btn-success btn-block"> Make Investment</button>
                        </div>
                        <div v-else>
                            <button v-show="bitcoin_amount_stat.low || bitcoin_amount_stat.high" class="btn btn-danger btn-block" @click.prevent="low_bitcoin()"> Make Investment</button><button v-show="bitcoin_amount_stat.standard || bitcoin_amount_stat.premium" @click.prevent="investBitcoin()" class="btn btn-success btn-block"> Make Investment</button>
                        </div>
                          <!-- <div style="text-align:center;">
                              <h4 style="font-weight:bold">or</h4>
                          </div> -->
                          <div style="margin-bottom:10px;margin-top:20px;">
                            <button v-if="donation_mode.use_naira" class="btn btn-dark white-text" @click.prevent='toggle_donation_mode'> Invest with Bitcoin</button>
                            <button v-else @click.prevent="toggle_donation_mode" class="btn btn-dark white-text"> Invest with Naira</button>
                        </div>
                        
                    </form>
        </div>
    </div>
</template>
<script>
export default {
    data(){
        return{
            investors:[],
            is_loading:false,
            success_msg:'',
            error_msg:'',
            donation_mode:{
                use_naira:true,
                use_bitcoin:false
            },
            amount:{
                naira:''
            },
            naira_amount_stat:{
                low:true,
                standard:false,
                premium:false,
                high:false
            },
            bitcoin_amount_stat:{
                low:true,
                standard:false,
                premium:false,
                high:false
            },
        }
    },
    methods:{
        getInvestors(){
            this.loading = true;
            axios.get('/dashboard/api/get-investors')
            .then(response=>{
                if(response.data.stat == 'good'){
                   this.investors = response.data.content 
                }
                else if(response.data.stat == 'none'){
                    this.investors = false
                }
                console.log('resp: ' + response.data.stat)
            })
            .catch(err=>{
                console.log(err)
            })
            .finally(()=>{
                this.is_loading = false
            })
        },
        check_naira_amount(){
            if(this.amount.naira < 2000){
                this.naira_amount_stat.low = true
                this.naira_amount_stat.standard = false
                this.naira_amount_stat.premium = false
                this.naira_amount_stat.high = false
            }
            else if(this.amount.naira >=2000 && this.amount.naira < 50000){
                this.naira_amount_stat.low = false
                this.naira_amount_stat.standard = true
                this.naira_amount_stat.premium = false
                this.naira_amount_stat.high = false
            }
            else if(this.amount.naira >=50000 && this.amount.naira <= 500000){
                this.naira_amount_stat.low = false
                this.naira_amount_stat.standard = false
                this.naira_amount_stat.premium = true
                this.naira_amount_stat.high = false
            }
            else if(this.amount.naira >500000){
                this.naira_amount_stat.low = false
                this.naira_amount_stat.standard = false
                this.naira_amount_stat.premium = false
                this.naira_amount_stat.high = true
            }
        },
        check_bitcoin_amount(){
            if(this.amount.bitcoin < 0.00049){
                this.bitcoin_amount_stat.low = true
                this.bitcoin_amount_stat.standard = false
                this.bitcoin_amount_stat.premium = false
                this.bitcoin_amount_stat.high = false
            }
            else if(this.amount.bitcoin >=0.00049 && this.amount.bitcoin < 0.012){
                this.bitcoin_amount_stat.low = false
                this.bitcoin_amount_stat.standard = true
                this.bitcoin_amount_stat.premium = false
                this.bitcoin_amount_stat.high = false
            }
            else if(this.amount.bitcoin >=0.012 && this.amount.bitcoin <= 0.13){
                this.bitcoin_amount_stat.low = false
                this.bitcoin_amount_stat.standard = false
                this.bitcoin_amount_stat.premium = true
                this.bitcoin_amount_stat.high = false
            }
            else if(this.amount.bitcoin >0.13){
                this.bitcoin_amount_stat.low = false
                this.bitcoin_amount_stat.standard = false
                this.bitcoin_amount_stat.premium = false
                this.bitcoin_amount_stat.high = true
            }
        }, 
        toggle_donation_mode(){
            this.donation_mode.use_naira = !this.donation_mode.use_naira
            this.donation_mode.use_bitcoin = !this.donation_mode.use_bitcoin
        },
        low_naira(){
            alert('enter an amount between 2,000 and 500,000 NGN')
        },
        low_bitcoin(){
            alert('enter an amount between 0.0049 and 0.13 BTC')
        },
        investNaira(){
           var check = confirm(`Are you sure you want to invest NGN${this.amount.naira}`)
           if(check){
            this.is_loading = true
            axios.post('/dashboard/api/invest',
            {amount:this.amount.naira})
            .then(response=>{
                if(response.data.stat == 'good'){
                    this.success_msg = `you have pledged to invest NGN${this.amount.naira} and will soon be matched`
                }
                else if(response.data.stat == 'no_account_details'){
                    this.error_msg = 'you must fill in your bank account details and phone number in the profile section before making an investment'
                }
                else if(response.data.stat == 'no_testimony'){
                    this.error_msg = 'you need to write a testimony for the recent return on investment you received before making a new investment'
                }
                else if(response.data.stat == 'already_invested'){
                    this.error_msg = 'you can only make one investment at a time'
                }
            })
            .catch(err=>{
                console.log(err)
            })
            .finally(()=>{
                this.is_loading = false
            })
           }
            
        },
        investBitcoin(){
           var check = confirm(`Are you sure you want to invest BTC ${this.amount.bitcoin}`)
           if(check){
            this.is_loading = true
            axios.post('/dashboard/api/investb',
            {amount:this.amount.bitcoin})
            .then(response=>{
                if(response.data.stat == 'good'){
                    this.success_msg = `you have pledged to invest BTC${this.amount.bitcoin} and will soon be matched`
                }
                else if(response.data.stat == 'no_account_details'){
                    this.error_msg = 'you must fill in a bitcoin wallet address and phone number in the profile section before making an investment'
                }
                else if(response.data.stat == 'no_testimony'){
                    this.error_msg = 'you need to write a testimony for the recent return on investment you received before making a new investment'
                }
                else if(response.data.stat == 'already_invested'){
                    this.error_msg = 'you can only make one investment at a time'
                }
            })
            .catch(err=>{
                console.log(err)
            })
            .finally(()=>{
                this.is_loading = false
            })
           }
            
        }
    },
    created(){
        this.getInvestors()
    }
}
</script>
<style scoped>
.white-text{
    color:#ffffff;
}
.info-msg{
    color:red;
    font-size:14px;
}
.package{
    background: red;
    color:#ffffff;
    border-radius:10px;
    padding:10px;
    margin:10px;
    max-width:50%;
    text-align:center;
}
.package-area{
    background:gainsboro;
    box-shadow: 5px 5px 5px gray;
    padding-left:15px;
    padding-bottom:15px;

}
.dot{
    background: grey;
    border-radius:50%;
    height:10px;
    width:15px;
}
</style>