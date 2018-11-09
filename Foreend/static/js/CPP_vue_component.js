//input, content replaced by ●
Vue.component('anonymous-input',{
    data:function(){
      return{
          msg:'',
          processed_msg:''
      }  
    },
    template:
        `
           <input 
                v-bind:value="processed_msg"
                v-on:input="input_str" 
           > 
        `,
    methods:{
        input_str:function(curr_msg) {
            if(curr_msg.data === null){
                this.msg = this.msg.slice(0,-2);
                this.processed_msg = this.processed_msg.slice(0,-2);
            }
            else{
                this.msg += curr_msg.data;
                this.processed_msg += '●';
            }
            this.$emit('is_input',this.msg);
        }
    }
});

//input component used when sign up
Vue.component('register-input',{
    props:{
        input_status:{
            type:Number,
            default:-1,
        },
        is_anonymous:{
            type:Boolean,
            default:false
        }
    },
    data:function(){
       return {
           msg: '',
           status_color:'gray'
       }
    },
    template:
        `   
            <div class="register-input-unit">   
                <span><slot name="title"></slot></span>
                <br>
                <template v-if="is_anonymous">
                    <anonymous-input 
                        v-on="$listeners"
                        v-on:is_input="msg = $event"
                    ></anonymous-input>
                </template>
                <template v-else>
                    <input 
                        v-model="msg" 
                        v-on:input="$emit('is_input',msg)"
                    >
                </template>
                <span ><font v-bind:color="status_color">{{signal}}</font></span>  
                <br>
                <span v-bind:style="{fontSize:'8px',color:'gray'}"><slot></slot></span>
            </div>
        `,
    computed:{
        signal:function () {
                if (this.input_status === -1 || this.msg.length === 0){
                    this.status_color = 'gray';
                    return '?';
                }
                if (this.input_status ===0){
                    this.status_color = 'red';
                    return '✕';
                }
                if (this.input_status === 1) {
                    this.status_color = 'green';
                    return '✓';
                }
            }
        },
});

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
