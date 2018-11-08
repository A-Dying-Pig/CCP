var register_username = new Vue({
    el: '.register-username',
    data:{
        status:-1,
    },
    methods:{
        validate_input:function (msg) {
            if(msg.length > 8){
                this.status = 1;
            }
            else{
                this.status = 0;
            }
        }
    }
});



