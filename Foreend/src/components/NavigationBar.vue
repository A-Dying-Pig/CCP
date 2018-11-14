<template>
    <div>
        <img src="../assets/img/ccpicon.png" class="naviicon">
        <div class = "navi_left">
        <a v-for="(item,index) in navi_left_items" :key="index" :href="item.href" class="navi_btn_left">{{item.name}}</a>
        </div>
        <div class = "navi_right">
        <a v-for="(item,index) in navi_right_items" :key="index" :href="item.href" class="navi_btn_right">{{item.name}}</a>
        </div>
        <hr class="line">
    </div>
</template>

<script>
export default{
data:function () {
        return {
            activeIndex: '1',
            navi_left_items:[
                {name:'主页',href:'/index'},
                {name:'全部比赛',href:'/competition'},
                {name:'个人中心',href:'/info'},
            ],
            navi_right_items:[
                {name:'登录',href:'/signin'},
                {name:'注册',href:'/signup'},
            ]
        }
    },
    methods: {
    handleSelect(key, keyPath) {
        console.log(key, keyPath);
    }
}

}

</script>

<style>

.navi_left{
    font-size: 16px;
    float:left;
    left: 20px;
    margin-top: 22px;
}

.navi_right{
    font-size: 16px;
    float:right;
    left: 20px;
    margin-top:22px;
}

.navi_btn_left{
     -moz-appearance: button;
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
    -moz-appearance: button;
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
</style>