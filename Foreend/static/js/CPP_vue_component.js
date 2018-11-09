//competition info
Vue.component("competition-profile",{
    props:{
        w:{
            type:Number,
            default:200,
        },
        h:{
            type:Number,
            default:400,
        },
        img_url: {
            type: String,
            default: ''
        },
        title:{
            type:String,
            default:''
        },
        intro:{
            type:String,
            default:''
        },
        comp_url:{
            type:String,
            default:''
        }
    },
    template:
        `
            <div class="competition-profile-unit"
                 :style="{width:w +'px'}"
                 style="white-space:normal;word-break:break-all;text-overflow: ellipsis"
            >
                <img
                    v-bind:src=img_url
                    :style="{width:w+'px',height:w+'px'}"
                >
                <br>
                <span><center>{{title}}</center></span>
                <p>{{intro}}</p>
            </div>
        `,
});

//register-input
//username
Vue.component('register-username',{
    data:function(){
        return {
            msg: '',
            status_color:'gray',
            status:-1,
        }
    },
    template:
        `   
            <div class="register-input-username">   
                <span class="register-input-title">用户名(username)</span>
                <br>
                <input 
                    v-model.trim="msg" 
                    v-on:input="validate"
                    class="register-input"
                >
                <span><font v-bind:color="status_color">{{signal}}</font></span>
                <br>
                <span class="register-input-info">数字,字母,下划线的组合</span>
            </div>
        `,
    computed:{
        signal:function () {
            if (this.status === -1 || this.msg.length === 0) {
                this.status_color = 'gray';
                return '?';
            }
            if (this.status === 0) {
                this.status_color = 'red';
                return '✕';
            }
            if (this.status === 1) {
                this.status_color = 'green';
                return '✓';
            }
        }
    },
    methods:{
        validate:function () {
            if(/^[a-zA-Z0-9_]+$/.test(this.msg) === false) {
                this.status = 0;
                return;
            }
            this.status = 1;
        }
    }
});

//password
Vue.component('register-password',{
    data:function(){
        return {
            msg: '',
            re_msg:'',
            status_color:'gray',
            status:-1,
            re_status_color:'gray',
            re_status:-1,
        }
    },
    template:
        `   
            <div class="register-input-password">   
                <span class="register-input-title">密码(username)</span>
                <br>
                <input 
                    v-model.trim="msg" 
                    v-on:input="validate"
                    type="password"
                    class="register-input"
                >
                <span ><font v-bind:color="status_color">{{signal}}</font></span>
                <br>
                <span class="register-input-info">数字,字母,下划线的组合,长度大于6</span>
                <br>
                <span class="register-input-title">再次输入确认密码</span>
                <br>
                <input 
                    v-model.trim="re_msg" 
                    v-on:input="re_validate"
                    type="password"
                    class="register-input"
                >
                <span ><font v-bind:color="re_status_color">{{re_signal}}</font></span>         
            </div>
        `,
    computed:{
        signal:function () {
            if (this.status === -1 || this.msg.length === 0) {
                this.status_color = 'gray';
                return '?';
            }
            if (this.status === 0) {
                this.status_color = 'red';
                return '✕';
            }
            if (this.status === 1) {
                this.status_color = 'green';
                return '✓';
            }
        },
        re_signal:function () {
            if (this.re_status === -1)  {
                this.re_status_color = 'gray';
                return '?';
            }
            if (this.re_status === 0) {
                this.re_status_color = 'red';
                return '✕';
            }
            if (this.re_status === 1) {
                this.re_status_color = 'green';
                return '✓';
            }
        }
    },
    methods:{
        validate:function () {
            if(this.msg.length < 6){
                this.status = 0;
                return;
            }
            if(/^[a-zA-Z0-9_]+$/.test(this.msg) === false) {
                this.status = 0;
                return;
            }
            this.status = 1;
        },
        re_validate:function () {
            if(this.msg === this.re_msg)
                this.re_status = 1;
            else
                this.re_status = 0;
        }
    }
});



//email
Vue.component('register-email',{
    data:function(){
        return {
            msg: '',
            status_color:'gray',
            status:-1,
        }
    },
    template:
        `   
            <div class="register-input-email">   
                <span class="register-input-title">邮箱(email address)</span>
                <br>
                <input 
                    v-model.trim = "msg" 
                    v-on:input="validate"
                    class="register-input"
                >
                <span ><font v-bind:color="status_color">{{signal}}</font></span>  
                <br>
                <span class="register-input-info">请输入合法的邮箱地址</span>
            </div>
        `,
    computed:{
        signal:function () {
            if (this.status === -1 || this.msg.length === 0) {
                this.status_color = 'gray';
                return '?';
            }
            if (this.status === 0) {
                this.status_color = 'red';
                return '✕';
            }
            if (this.status === 1) {
                this.status_color = 'green';
                return '✓';
            }
        }
    },
    methods:{
        validate:function () {
            if(/^[a-zA-Z0-9_]+@[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+/.test(this.msg) === false) {
                this.status = 0;
                return;
            }
            this.status = 1;
        }
    }
});