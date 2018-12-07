<template>
    <div>
        <img src="../assets/img/ccpicon.png" class="naviicon">
        <div class = "navi_left">
        <a v-for="(item,index) in navi_left_items" :key="index" :href="item.href" class="navi_btn_left">{{item.name}}</a>
        </div>
        <div class = "navi_right" v-if="username==='#undefined'">
            <a v-for="(item,index) in navi_right_items" :key="index" :href="item.href" class="navi_btn_right">{{item.name}}</a>
        </div>
        <div v-else class = "navi_right">
            <el-badge :value="message_number" :hidden="message_number === 0" class="profile-msg-number-icon" :max="99">
                <a href="/message" class="profile-msg-number"><i class="el-icon-bell"></i> </a>
            </el-badge>
            <a v-for="(item,index) in navi_right_items_login" :key="index" :href="item.href" class="navi_btn_right">{{item.name}}</a>
        </div>
        <hr class="line">
    </div>
</template>

<script>
    import axios from 'axios'
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.headers.common = {
        'X-CSRFToken':document.querySelector('#csrf-token input').value,
        'X-Requested-With': 'XMLHttpRequest'
    };

export default{
    props:{
        username:{
            default:'#undefined',
            type:String
        },
    },
    data:function () {
        return {
            activeIndex: '1',
            navi_left_items:[
                {name:'主页',href:'/'},
                {name:'全部比赛',href:'/contest'},
                {name:'个人中心',href:'/profile'},
                {name:'创建比赛',href:'/addContest'}
            ],
            navi_right_items:[
                {name:'登录',href:'/login'},
                {name:'注册',href:'/register'},
            ],
            navi_right_items_login: [
                {name:this.username,href:'/profile'},
                {name:'登出',href:'/logout'}
            ],
            message_number:13,
        }
    },
    methods: {
    },
    mounted:function () {
        if (this.username !== '') {
            axios.post('/api/message/getnew')
                .then(response => {
                    this.message_number = response.data.num;
                }).catch(function (error) {
                    console.log('错误！！');
                })
        }
    }

}

</script>

<style>

.navi_left{
    font-family: PingFang SC;
    font-size: 16px;
    float:left;
    left: 20px;
    margin-top: 22px;
}

.navi_right{
    font-family: PingFang SC;
    font-size: 16px;
    float:right;
    left: 20px;
    margin-top:22px;
}

.navi_btn_left{
     /*-moz-appearance: button;*/
     text-decoration: none;
     padding-left:20px;
     padding-right:20px;
     left:10px;
     color: initial;

}

.navi_btn_left:hover{
    color: dodgerblue;
    left:10px;
    padding-left:20px;
    padding-right:20px;
}

.navi_btn_right:hover{
    color: dodgerblue;
    left:10px;
    padding-left:20px;
    padding-right:20px;
}

.navi_btn_right{
    padding-left:20px;
    padding-right:20px;
    text-decoration: none;
    color: initial;
}

.naviicon {
    width:120px;
    height:70px;
    float: left;
}

.line{
    width:100%;
    }

.profile-msg-number{
    text-decoration: none;
    color:initial;
}

.profile-msg-number-icon{
    margin-right: 20px;
    margin-left: 20px;
}
</style>



