<template>
    <div>
        <div v-if="is_loading" id="loader"></div>
        <div v-else>
           <div class="container">
               <div class='row'>
                   <div class="col-12">
                       <div class="toggle">
                            <button v-if="naira_mode" class="btn btn-danger" @click="toggle_view">Naira</button><button v-else class="btn btn-outline-danger" @click="toggle_view">Naira</button>
                             &nbsp;<button v-if="naira_mode" class="btn btn-outline-danger"  @click="toggle_view">Bitcoin</button><button v-else class="btn btn-danger"  @click="toggle_view">Bitcoin</button>
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
                    </div>
                    
                        
                            
                                <div class="col-6" v-show="naira_mode">
                                    <h6>Investor</h6>
                                    <p>Name : {{naira.current_name_i}}</p>
                                    <p>Amount: {{naira.current_amount_i}}</p>
                                </div>
                                <div class="col-6" v-show="naira_mode">
                                     <h6>Receiver</h6>
                                    <p>Name : {{naira.current_name_r}}</p>
                                    <p>Amount: {{naira.current_amount_r}}</p>
                                </div>
                                <div class='col-12' style="text-align:center;" v-show="naira_mode">
                                    <button class="btn btn-success" v-on:click.prevent="match_naira()">Match</button>
                                </div>
                            
                        

                          <br>
                        <div class="col-12" v-show="naira_mode">
                            <h6>Investors</h6>
                            <ol>
                                <li v-for="(investor, index) in investors">
                                <span><button class='btn btn-danger' @click.prevent="current_investor_n(index)">{{investor.name}}</button> - {{investor.amount}}</span>&nbsp;&nbsp;
                                </li><br>
                            </ol>
                        </div><br>
                        <div class="col-12" v-show="naira_mode">
                            <h6>Receivers</h6>
                            <ol>
                                <li v-for="(receiver, index) in receivers">
                                <span style="border-left:solid 3px black;margin-left:10px;">&nbsp;<b v-show="receiver.is_priority">Priority</b><button v-if='receiver.mod' class='btn btn-primary' @click.prevent="current_receiver_n(index)">{{receiver.name}}</button><button v-else class='btn btn-warning' @click.prevent="premature_receiver_n(index)">{{receiver.name}}</button> - {{receiver.amount}}</span>
                                </li><br>
                            </ol>
                        </div>

                          <div class="col-6" v-show="!naira_mode">
                                    <h6>Investor</h6>
                                    <p>Name : {{bitcoin.current_name_i}}</p>
                                    <p>Amount: {{bitcoin.current_amount_i}}</p>
                                </div>
                                <div class="col-6" v-show="!naira_mode">
                                     <h6>Receiver</h6>
                                    <p>Name : {{bitcoin.current_name_r}}</p>
                                    <p>Amount: {{bitcoin.current_amount_r}}</p>
                                </div>
                                <div class='col-12' style="text-align:center;" v-show="!naira_mode">
                                    <button class="btn btn-success" v-on:click.prevent="match_bitcoin()">Match</button>
                                </div>
                            
                        

                          <br>
                        <div class="col-12" v-show="!naira_mode">
                            <h6>Investors</h6>
                            <ol>
                                <li v-for="(investor, index) in investorsb">
                                <span><button class='btn btn-danger' @click.prevent="current_investor_b(index)">{{investor.name}}</button> - {{investor.amount}}</span>&nbsp;&nbsp;
                                </li><br>
                            </ol>
                        </div><br>
                        <div class="col-12" v-show="!naira_mode">
                            <h6>Receivers</h6>
                            <ol>
                                <li v-for="(receiver, index) in receiversb">
                                <span style="border-left:solid 3px black;margin-left:10px;">&nbsp;<b v-show="receiver.is_priority">Priority</b><button v-if="receiver.mod" class='btn btn-primary' @click.prevent="current_receiver_b(index)">{{receiver.name}}</button><button v-else class='btn btn-warning' @click.prevent="premature_receiver_b(index)">{{receiver.name}}</button> - {{receiver.amount}}</span>
                                </li><br>
                            </ol>
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
            naira_mode:true,
            success_msg:'',
            error_msg:'',
            is_loading:false,
            investors:[],
            investorsb:[],
            receiversb:[],
            receivers:[],
            naira:{
                current_name_i:'',
                current_amount_i:'',
                current_name_r:'',
                current_amount_r:'',
                user_pay:'',
                receiver_remnant:'',
                payer_remnant:''
            },
            bitcoin:{
                current_name_i:'',
                current_amount_i:'',
                current_name_r:'',
                current_amount_r:'',
                user_pay:'',
                receiver_remnant:'',
                payer_remnant:''
            }
        }
    },
    methods:{
        toggle_view(){
            this.naira_mode = !this.naira_mode
        },
        getInvestors(){
            this.is_loading = true
            axios.get('/account/api/investors')
            .then(response=>{
                this.investors = response.data.content
            })
            .catch(err=>{
                console.log(err)
            })
            .finally(()=>{
                this.is_loading = false
            })
        },
        getReceivers(){
            this.is_loading = true
            axios.get('/account/api/match-money')
            .then(response=>{
               this.receivers = response.data.content
               var data = response.data.content
               if( new Date() > new Date(data.date_end)){
                   alert('before')
               }
               for(var obj = 0; obj < data.length; obj++){
                   if(new Date() > new Date(data[obj].date_end)){
                       data[obj].mod = 1
                       alert('hmm')
                   }
                   else{
                       data[obj].mod = 0
                   }
               } 
            })
            .catch(err=>{
                console.log(err)
            })
            .finally(()=>{
                this.is_loading = false
            })
        },
        getInvestorsb(){
            this.is_loading = true
            axios.get('/account/api/investorsb')
            .then(response=>{
                this.investorsb = response.data.content
                
            })
            .catch(err=>{

            })
            .finally(()=>{
                this.is_loading = false
            })
        },
        getReceiversb(){
            this.is_loading = true
            axios.get('/account/api/match-bitcoin')
            .then(response=>{
               this.receiversb = response.data.content
               var data = response.data.content
               if( new Date() > new Date(data.date_end)){
                   alert('before')
               }
               for(var obj = 0; obj < data.length; obj++){
                   if(new Date() > new Date(data[obj].date_end)){
                       data[obj].mod = 1
                       alert('hmm')
                   }
                   else{
                       data[obj].mod = 0
                   }
               } 
            })
            .catch(err=>{
                console.log(err)
            })
            .finally(()=>{
                this.is_loading = false
            })
        },
        current_investor_n(index){
            var investor = this.investors[index]
            this.naira.current_name_i = investor.name
            this.naira.current_amount_i = investor.amount
        },
        premature_receiver_n(index){
            var check = confirm('this receivers time has not yet reached, are you sure master?')
            if(check){
                this.current_receiver_n(index)
            }
        },
        current_receiver_n(index){
            var receiver = this.receivers[index]
            this.naira.current_name_r = receiver.name
            this.naira.current_amount_r = receiver.amount
        },
        premature_receiver_b(index){
            var check = confirm('this receivers time has not yet reached, are you sure master?')
            if(check){
                this.current_receiver_b(index)
            }
        },
        current_investor_b(index){
            var investor = this.investorsb[index]
            this.bitcoin.current_name_i = investor.name
            this.bitcoin.current_amount_i = investor.amount
        },
        current_receiver_b(index){
            var receiver = this.receiversb[index]
            this.bitcoin.current_name_r = receiver.name
            this.bitcoin.current_amount_r = receiver.amount
        },
        match_naira(){
            if(this.naira.current_amount_i && this.naira.current_amount_r){
                var check = confirm(`Are you sure you want to match ${this.naira.current_name_i} to pay ${this.naira.current_name_r}`)
                if(check){
                    this.is_loading = true;
                    if(this.naira.current_amount_i < this.naira.current_amount_r){
                        this.naira.user_pay = this.naira.current_amount_i
                       this.naira.receiver_remnant =  this.naira.current_amount_r - this.naira.current_amount_i
                       this.naira.payer_remnant = 0
                    }
                    else if(this.naira.current_amount_i > this.naira.current_amount_r){
                        this.naira.user_pay = this.naira.current_amount_r
                        this.naira.payer_remnant = this.naira.current_amount_i - this.naira.current_amount_r
                        this.naira.receiver_remnant = 0
                    }
                    else if(this.naira.current_amount_i == this.naira.current_amount_r){
                        this.naira.user_pay = this.naira.current_amount_r
                        this.naira.payer_remnant = 0
                        this.naira.receiver_remnant = 0
                    }
                    else{
                        this.error_msg = 'something went wrong'
                    }
                }
            
            
                axios.post('/account/api/investors', {
                    user_pay:this.naira.user_pay,
                    receiver_remnant:this.naira.receiver_remnant,
                    payer_remnant:this.naira.payer_remnant,
                    investor:this.naira.current_name_i,
                    receiver:this.naira.current_name_r
                })
                .then(response=>{
                    this.getReceivers()
                    this.getInvestors()
                    if(response.data.stat == 'good'){
                        this.success_msg = 'User matched!'
                        setTimeout(() => {
                            window.location.reload()
                        }, 3000)
                    }
                    
                })
                .catch(err=>{
                    console.log(err)
                })
                .finally(()=>{
                    this.is_loading = false
                })
            
            }
            else{
                alert('please fill both investor and receiver fields')
            }

        },
        match_bitcoin(){
            if(this.bitcoin.current_amount_i && this.bitcoin.current_amount_r){
                var check = confirm(`Are you sure you want to match ${this.bitcoin.current_name_i} to pay ${this.bitcoin.current_name_r}`)
                if(check){
                    this.is_loading = true;
                    if(this.bitcoin.current_amount_i < this.bitcoin.current_amount_r){
                        this.bitcoin.user_pay = this.bitcoin.current_amount_i
                       this.bitcoin.receiver_remnant =  this.bitcoin.current_amount_r - this.bitcoin.current_amount_i
                       this.bitcoin.payer_remnant = 0
                    }
                    else if(this.bitcoin.current_amount_i > this.bitcoin.current_amount_r){
                        this.bitcoin.user_pay = this.bitcoin.current_amount_r
                        this.bitcoin.payer_remnant = this.bitcoin.current_amount_i - this.bitcoin.current_amount_r
                        this.bitcoin.receiver_remnant = 0
                    }
                    else if(this.bitcoin.current_amount_i == this.bitcoin.current_amount_r){
                        this.bitcoin.user_pay = this.bitcoin.current_amount_r
                        this.bitcoin.payer_remnant = 0
                        this.bitcoin.receiver_remnant = 0
                    }
                    else{
                        this.error_msg = 'something went wrong'
                    }
                }
            
            
                axios.post('/account/api/investorsb', {
                    user_pay:this.bitcoin.user_pay,
                    receiver_remnant:this.bitcoin.receiver_remnant,
                    payer_remnant:this.bitcoin.payer_remnant,
                    investor:this.bitcoin.current_name_i,
                    receiver:this.bitcoin.current_name_r
                })
                .then(response=>{
                    this.getReceivers()
                    this.getInvestors()
                    if(response.data.stat == 'good'){
                        this.success_msg = 'User matched!'
                        setTimeout(() => {
                            window.location.reload()
                        }, 3000)
                    }
                    
                })
                .catch(err=>{
                    console.log(err)
                })
                .finally(()=>{
                    this.is_loading = false
                })
            
            }
            else{
                alert('please fill both investor and receiver fields')
            }

        }
    },
    created(){
        this.getInvestors()
        this.getReceivers()
        this.getInvestorsb()
        this.getReceiversb()
    }
}
</script>
<style scoped>
ol{
    display:flex;
}
</style>