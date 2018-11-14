<template><div class="CompetitionCreatePage">
    <CompetitionInfo typeid="1" v-bind:finfo="allinfo.basicinfo" v-on:infochange="allinfo.basicinfo = $event">比赛基本信息</CompetitionInfo>
    <CompetitionInfo typeid="2" v-bind:finfo="allinfo.signupinfo" v-on:infochange="allinfo.signcinfo = $event">比赛报名设置</CompetitionInfo>
</div></template>
<script>
    import CompetitionInfo from './CompetitionInfo'
    export default {
        components:{CompetitionInfo},
        data:function () {
            return {
                allinfo:{
                  basicinfo:{
                      name:'',
                      holders:[''],
                      sponsors:[''],
                      comtype:'',
                      details:"",
                  },
                  signupinfo:{
                      time:[],
                      mode:'个人赛',
                      person:[
                          ''
                      ],
                      group:[
                          ''
                      ]
                  },
                  //TODO stages
                },
            }
        },
        created:function () {
            //test
            var self=this;
            setInterval(function () {
                //console.log(self.allinfo.basicinfo);
            },500)
        }
    }
</script>
<style></style>