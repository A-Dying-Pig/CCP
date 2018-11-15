<template><div class="CompetitionCreatePage">
    <cinfo ref="basic" typeid=1 v-bind:finfo="allinfo.basicinfo">比赛基本信息</cinfo>
    <cinfo ref="signup" typeid=2 v-bind:finfo="allinfo.signupinfo">比赛报名设置</cinfo>
    <cinfo ref="stage" typeid=3 v-bind:finfo="allinfo.stageinfo">比赛阶段设置</cinfo>
    <el-row :gutter="20">
        <el-col :space="10" :offset="5">
            <el-button type="primary" @click="summitForm">提交</el-button>
        </el-col>
    </el-row>
</div></template>
<script>
    import CompetitionInfo from './CompetitionInfo'
    export default {
        components:{
            'cinfo':CompetitionInfo,
        },
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
                      ]
                  },
                  stageinfo:[{}]
                },
            }
        },
        methods:{
            summitForm:function () {
                let res=[];
                var flag=true;
                res.push(this.$refs.basic.validate());
                res.push(this.$refs.signup.validate());
                res.push(this.$refs.stage.validate());
                for(let one of res){
                    if(!one){
                        flag=false;
                    }
                }
                if(flag){
                    alert('submit');
                }
                else {
                    alert('submit error');
                }
            }
        },
        created:function () {
            //test
            var self=this;
            setInterval(function () {
                //console.log(self.allinfo.stageinfo);
            },500)
        }
    }
</script>
<style></style>