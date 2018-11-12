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

//navigation bar
Vue.component('navigation-bar',{
    data:function () {
        return {
            navileftitems:[
                {name:'',href:'/index',tclass:{'naviicon':true}},
                {name:'主页',href:'/index',tclass:{'navihref':true}},
                {name:'全部比赛',href:'/',tclass:{'navihref':true}},
                {name:'个人中心',href:'/',tclass:{'navihref':true}},
            ],
            navirightitems:[
                {name:'登录',href:'/',tclass:{'navihref':true}},
                {name:'注册',href:'/',tclass:{'navihref':true}},
            ]
        }
    },
    template:`<div class = "navibar">
    <ul class = "navi-left">
    <li v-for="item in navileftitems" class="navili" ><a v-bind:href="item.href" v-bind:class="item.tclass">{{ item.name }}</a></li>
    </ul>
    <ul class = "navi-right">
    <li v-for="item in navirightitems" class="navili"><a v-bind:href="item.href" v-bind:class="item.tclass">{{ item.name }}</a></li>
    </ul></div>
   `,
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

//word limit input
/*
    title is required
    wordmin and wordmax are optional
 */
Vue.component('register-wordlimit',{
    props:['title','wordmin','wordmax'],
    data:function(){
        return {
            msg: '',
            status_color:'gray',
            status:-1,
        }
    },
    template:
        `   
            <div class="register-input-wordlimit">   
                <span class="register-input-title">{{ title }}</span>
                <br>
                <input 
                    v-model.trim = "msg" 
                    v-on:input="validate"
                    class="register-input"
                >
                <span ><font v-bind:color="status_color">{{signal}}</font></span>  
                <br>
                <span class="register-input-info" v-if="wordmin && wordmax">字数限制{{ wordmin }}字到{{ wordmax }}字之间</span>
                <span class="register-input-info" v-else-if="wordmin">至少输入{{ wordmin }}字</span>
                <span class="register-input-info" v-else-if="wordmax">至多输入{{ wordmax }}字</span>
                <span class="register-input-info" v-else>无字数限制</span>
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
            var len = this.msg.length;
            if(this.wordmin&&this.wordmax){
                if((len>=this.wordmin)&&(len<=this.wordmax)){
                    this.status = 1;
                }
                else this.status=0;
                return;
            }
            else if(this.wordmin){
                if(len>=this.wordmin){
                    this.status = 1;
                }
                else this.status=0;
                return;
            }
            else if(this.wordmax){
                if(len<=this.wordmax){
                    this.status = 1;
                }
                else this.status=0;
                return;
            }
            else{
                this.status=0;
                return;
            }
        }
    }
});

Vue.component('competition-list',{
    props:['com'],
    template:`
    <div class="competition-list">
        <td>{{com.number}}</td>
        <td>{{com.name}}</td>
        <td>{{com.organizer}}</td>
        <td>{{com.information}}</td>
        <td>{{com.detail}}</td>  
    </div>`
});

Vue.component('datetime-input',{
   props:['value','title'],
   data:function(){
      return{

      }
    },
   template:`
<div class="cdatetime-input">
    <span class="register-input-title">{{ title }}</span><br>
    <input type="datetime-local" v-bind:value="value" v-on:input="$emit('input', $event.target.value)">
</div>
   `,
});