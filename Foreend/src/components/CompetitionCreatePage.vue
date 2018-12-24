<template>
    <div class="CompetitionCreatePage">
        <el-row>
            <el-col :offset="6" :span="12"><CompetitionInfo ref="basic" typeid=1 v-bind:finfo="allinfo.basicinfo" :change="change">比赛基本信息</CompetitionInfo></el-col>
            <el-col :offset="6" :span="12"><CompetitionInfo ref="signup" typeid=2 v-bind:finfo="allinfo.signupinfo" :change="change">比赛报名设置</CompetitionInfo></el-col>
            <el-col :offset="6" :span="12"><CompetitionInfo ref="stage" typeid=3 v-bind:finfo="allinfo.stageinfo" :change="change" :signend="info.signupinfo.time[1]">比赛阶段设置</CompetitionInfo></el-col>
        </el-row>
            <p></p>
            <p></p>
        <el-row :gutter=20 class="commit_style">
            <el-col :span=12 :offset=6>
                <el-button type="primary" @click="summitForm">提交</el-button>
            </el-col>
        </el-row>
    </div>
</template>

<script>
    import CompetitionInfo from './CompetitionInfo.vue'
    //import axios from 'axios'

    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.headers.common = {
        'X-CSRFToken':document.querySelector('#csrf-token input').value,
        'X-Requested-With': 'XMLHttpRequest'
    };
    
    export default {
        components:{
            CompetitionInfo,
        },
        props:{
            change:{
              type:Boolean,
              default:false
            },
            contestid:{
                type:Number,
                default:-1
            },
            info:{
                type:Object,
                default:function () {
                    return {
                        basicinfo:{
                            name:'',
                            holders:[''],
                            sponsors:[],
                            comtype:'',
                            details:"",
                            img:'',
                            briefintroduction:'',
                        },
                        signupinfo:{
                            time:[],
                            mode:'1',
                            person:[
                                ''
                            ],
                            group:[
                            ],
                            teamnum:[3,
                                5
                            ],
                        },
                        stageinfo:[{
                            name:'',
                            details:'',
                            mode:'在线预览',
                            zone:'统一赛区'
                        }]
                    }
                }
            }
        },
        data:function () {
            return {
                allinfo:this.info,
            }
        },
        methods:{
            summitForm:function () {
                var self = this;
                let res=[];
                var flag=true;
                console.log(self.allinfo)
                res.push(this.$refs.basic.validate());
                res.push(this.$refs.signup.validate());
                res.push(this.$refs.stage.validate());
                for(let one of res){
                    if(!one){
                        flag=false;
                    }
                }
                if(!flag) return;
                //put check here
                if(this.allinfo.basicinfo.img === ''){
                    alert('需要提交比赛图片！');
                    return
                }
                if(this.allinfo.basicinfo.holders.length===0){
                    alert('至少要有一个主办方！');
                    return;
                }
                if(this.allinfo.stageinfo.length===0){
                    alert('至少要有一个阶段！');
                    return;
                }
                if(this.allinfo.signupinfo.person.length===0){
                    alert('至少要有一个选手信息！');
                    return;
                }
                for(let sp of this.allinfo.basicinfo.sponsors){
                    if(sp===''){
                        alert('承办方输入框不可空！');
                        return;
                    }
                }
                if(this.allinfo.signupinfo.time[0]>=this.allinfo.signupinfo.time[1]){
                    alert('报名时间错误！');
                    return;
                }
                let begin = this.allinfo.signupinfo.time[1];
                for(let stage of this.allinfo.stageinfo){
                    if(begin>=stage.stageTimeBegin){
                        alert('阶段开始时间错误！');
                        return;
                    }
                    begin = stage.stageTimeBegin;
                    if(begin>=stage.handTimeEnd){
                        alert('阶段提交结束时间错误！');
                        return;
                    }
                    begin = stage.handTimeEnd;
                    if(begin>=stage.evaluationTimeEnd){
                        alert('阶段评测结束时间错误！');
                        return;
                    }
                    begin = stage.evaluationTimeEnd;
                }
                //change teamnum format
                let teamnumtmp = self.allinfo.signupinfo.teamnum;
                if(flag){
                    if(self.change){
                        self.allinfo['contestid']=self.contestid;
                        axios.post('/api/admin/modify',self.allinfo)
                            .then(function (response) {
                                console.log(response);
                            self.$message({
                                    message: '操作成功!',
                                    type: 'success'
                                });
                            })
                            .catch(function (error) {
                                console.log(error);
                            });
                    }
                    else {
                        axios.post('/api/competition/create',self.allinfo)
                            .then(function (response) {
                                if(response.data.msg!==''){
                                    self.$message({
                                        message: response.data.msg,
                                        type: 'error'
                                    });
                                    return
                                }
                                self.$message({
                                    message: '操作成功!',
                                    type: 'success'
                                });
                                location.href = "/";
                            })
                            .catch(function (error) {
                                self.$message({
                                    message: '操作失败!',
                                    type: 'error'
                                });
                            });
                    }

                }
                else {
                    alert('submit error');
                }
            }
        },
        created:function () {

        }
    }
</script>

<style>
</style>