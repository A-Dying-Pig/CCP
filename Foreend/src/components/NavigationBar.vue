<template>
<div class = "navibar">
    <ul class = "navi-left">
    <li v-for="item in navileftitems" class="navili" :key="item.key"><a v-bind:href="item.href" v-bind:class="item.tclass">{{ item.name }}</a></li>
    </ul>
    <ul class = "navi-right">
    <li v-for="item in navirightitems" class="navili" :key="item.key"><a v-bind:href="item.href" v-bind:class="item.tclass">{{ item.name }}</a></li>
    </ul></div>
</template>

<script>
export default{
data:function () {
        return {
            navileftitems:[
                {name:'',href:'/index',tclass:{'naviicon':true}},
                {name:'主页',href:'/index',tclass:{'navihref':true}},
                {name:'全部比赛',href:'/CompetitionCreate',tclass:{'navihref':true}},
                {name:'个人中心',href:'/',tclass:{'navihref':true}},
            ],
            navirightitems:[
                {name:'登录',href:'/',tclass:{'navihref':true}},
                {name:'注册',href:'/',tclass:{'navihref':true}},
            ]
        }
    },

}
</script>

<style>
.navibar{
    width: 100%;
    z-index: 60;
    padding: 20px 0;
    background: #fff;
    box-shadow: 0 2px 6px rgba(0,0,0,.1);
    position: fixed;
    left: 0;
    top: 0;
    font-size: 40px;
}
.navi-left .navi-right{
    padding: 0;
    margin: 0;
    word-break: break-all;
    word-wrap: break-word;
    list-style: none;
    font-size: inherit;
}
.navi-left{
    float: left;
}
.navi-right{
    float: right;
}
.navili{
    float:left ;
    list-style:none;
    margin: 0 10px;
    font-size: inherit;
}
.navihref:link{
    color: black;
    text-decoration: none;
}
.naviicon {
    width: 119px;
    height: 73px;
    float: left;
    margin: 0 10px;
    background-image: url(./../assets/img/ccpicon.png);
}
</style>