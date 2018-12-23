<template>
    <div>
        <el-row>
            <el-col :offset="3" :span="18">
                <el-card shadow="always">
                    <el-row :gutter="24">
                        <el-col :span="4">
                            <img :src="info.basicinfo.img" style="width: 150px;"/>
                        </el-col>
                        <el-col :span="20">
                            <el-row :gutter="24">
                                <el-col :span="4" class="title">
                                    <b>{{ info.basicinfo.name }}</b>
                                </el-col>
                                <el-col :span="6" :offset="14">
                                    <p style="font-size: 12px">已报名<span style="color: #3a8ee6">{{ enrollnum }}</span>人</p>
                                </el-col>
                            </el-row>

                            <el-row :gutter="24">
                                <el-col :span="20">
                                    <div class="brief"> <p style="font-size: 12px">{{ info.basicinfo.briefintroduction }}</p></div>
                                </el-col>
                            </el-row>

                            <el-row :gutter="24">
                                <el-col :span="18">
                                    <el-popover
                                            placement="top-start"
                                            :title="gethovertitle()"
                                            width="200"
                                            trigger="hover"
                                            :content="gethovercontent()">
                                    <el-steps :active="getActivestage()" style="float: bottom" slot="reference">
                                        <el-step title="报名" :description="timestamp2datestr(info.signupinfo.time[0],false)"></el-step>
                                        <template v-for="item in info.stageinfo">
                                            <el-step :title="item.name" :description="timestamp2datestr(item.stageTimeBegin,false)" :key="item.key"></el-step>
                                        </template>
                                        <el-step title="结束" :description="timestamp2datestr(info.stageinfo[info.stageinfo.length-1].evaluationTimeEnd,false)"></el-step>
                                    </el-steps>
                                    </el-popover>
                                </el-col>
                                <el-col v-if="((type === 0)&&(Date.now()>info.signupinfo.time[0])&&(Date.now()<info.signupinfo.time[1]))" :span="6" >
                                    <el-button @click="clicksign" type="primary">报名参赛！</el-button>
                                </el-col>
                            </el-row>

                            <el-row :gutter="20" v-if="info.basicinfo.beginjudgebutton">
                                <el-col :span="16">
                                    <p>比赛已经进入评测阶段，请点击“评委信息”标签自动为每位评委分配作品</p>
                                </el-col>
                            </el-row>
                        </el-col>
                    </el-row>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script>
    import axios from 'axios'
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.headers.common = {
        'X-CSRFToken':document.querySelector('#csrf-token input').value,
        'X-Requested-With': 'XMLHttpRequest'
    };
    export default {
        props:['info','type','contestid'],
        data:function () {
            return{
                activeStage:0,
                enrollnum:0,
                showbutton:1
            }
        },
        methods:{
          timestamp2datestr:function (stamp,showdetail) {
              let date = new Date(stamp);
              let hour = date.getHours()<10?'0'+date.getHours().toString():date.getHours().toString();
              let minite = date.getMinutes()<10?'0'+date.getMinutes().toString():date.getMinutes().toString();
              if(showdetail === true){
                  return (Number(date.getMonth())+1)+'月'+date.getDate()+'日' + hour+'时'+minite+'分';
              }
              return (Number(date.getMonth())+1)+'月'+date.getDate()+'日';
          },
            getActivestage:function () {
                let now = Date.now();
                if(now<this.info.signupinfo.time[0]){
                    return 0;
                }
                if(now<this.info.signupinfo.time[1]){
                    return 1;
                }
                for(let idx in this.info.stageinfo){
                    if(now<this.info.stageinfo[idx].stageTimeBegin){
                        return Number(idx)+1;
                    }
                }
                if(now<this.info.stageinfo[this.info.stageinfo.length-1].evaluationTimeEnd){
                    return this.info.stageinfo.length+1;
                }
                return this.info.stageinfo.length+2;
            },
            clicksign:function () {
                location.href="/enroll?contestid="+this.contestid;
            },
            assignproject:function () {
                let self = this;
                axios.post('/api/admin/alloc',{
                    contestid:self.contestid
                }).then(function (response) {
                    if(response.data.msg!==''){
                        self.$message({
                            message:response.data.msg,
                            type:'error'
                        })
                    }
                    else {
                        self.$message({
                            message:'评委分配成功！',
                            type:'success'
                        })
                    }
                }).catch(function (error) {
                    self.$message({
                        message:'评委分配失败！',
                        type:'error'
                    })
                })
            },
            gethovertitle:function () {
                let status = this.getActivestage();
                if(status===0){
                    return '报名未开始'
                }
                else if(status === 1){
                    return '报名进行中'
                }
                else if(status === this.info.stageinfo.length+2){
                    return '比赛已结束'
                }
                else {
                    return this.info.stageinfo[status-2].name;
                }
            },
            gethovercontent:function () {
                let status = this.getActivestage();
                if(status===0){
                    return ''
                }
                else if(status === 1){
                    return '报名开始时间:'+this.timestamp2datestr(this.info.signupinfo.time[0],true)+'\n报名结束时间:'
                        +this.timestamp2datestr(this.info.signupinfo.time[1],true)
                }
                else if(status === this.info.stageinfo.length+2){
                    return ''
                }
                else {
                    return '开始时间:'+this.timestamp2datestr(this.info.stageinfo[status-2].stageTimeBegin,true)+'\n提交截止时间:'
                    +this.timestamp2datestr(this.info.stageinfo[status-2].handTimeEnd,true)+'\n评测截止时间:'
                    +this.timestamp2datestr(this.info.stageinfo[status-2].evaluationTimeEnd,true)
                }
            }
        },
        created:function () {
            let self = this;
            self.showbutton = ((self.type === 0)&&(Date.now()>self.info.signupinfo.time[0])&&(Date.now()<self.info.signupinfo.time[1]));
            axios.post('/api/competition/enrollnum',{
                contestid:self.contestid
            }).then(function (response) {
                if(response.data.msg!==''){
                    self.$message({
                        message:'获取报名人数错误！'+response.data.msg,
                        type:'error'
                    });
                    return;
                }
                self.enrollnum = response.data.enrollnum;
            }).catch(function (error) {
                self.$message({
                    message:'获取报名人数错误！',
                    type:'error'
                });
            })
        }
    }
</script>

<style>
    .title{
        text-align: left;
        font-size: 50px;
    }
    .brief{
        border-left: 2px #4da9fe solid;
        background-color: #f9fafa;
    }
</style>