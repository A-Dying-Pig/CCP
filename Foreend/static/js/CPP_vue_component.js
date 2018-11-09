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

//register-user-input
//input component used when sign up
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
            <div class="register-input">   
                <span class="register-input-title">用户名(username)</span>
                <br>
                <input 
                    v-model="msg" 
                    v-on:input="validate"
                >
                <span ><font v-bind:color="status_color">{{signal}}</font></span>  
                <br>
                <span class="register-input-info">输入数字字母的组合,长度大于8</span>
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
            if(this.msg.length > 8){
                this.status = 1;
            }
            else{
                this.status = 0;
            }
        }
    }
});