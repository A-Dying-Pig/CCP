<template>
    <div>
        <el-row>
            <el-col :offset="3" :span="18">
                <el-card shadow="always">
                    <el-row :gutter="24">
                        <el-col class="title" :span="5">
                            <b>{{ info.basicinfo.name }}</b>
                        </el-col>
                        <el-col :span="2" :offset="14">
                            <p style="font-size: 12px">已报名<span style="color: #3a8ee6">{{ enrollnum }}</span>人</p>
                        </el-col>
                        <el-col v-if="showbutton" :span="3" >
                            <el-button @click="clicksign" type="primary">报名参赛！</el-button>
                        </el-col>

                    </el-row>
                    <p></p>
                    <el-row :gutter="20">
                        <el-steps :space="50" :active="getActivestage()" finish-status="success" simple style="height:80px;font-size:small">
                            <el-step :title="timestamp2datestr(info.signupinfo.time[0]) + '报名开始'"></el-step>
                            <el-step :title="timestamp2datestr(info.signupinfo.time[1]) + '报名结束'"></el-step>
                            <template v-for="item in info.stageinfo">
                                <el-step :title="timestamp2datestr(item.stageTimeBegin)+item.name+'开始'" :key="item.key"></el-step>
                                <el-step :title="timestamp2datestr(item.handTimeEnd)+item.name+'提交截止'" :key="item.key"></el-step>
                                <el-step :title="timestamp2datestr(item.evaluationTimeEnd)+item.name+'评测截止'" :key="item.key"></el-step>
                            </template>
                        </el-steps>
                    </el-row>
                    <el-row :gutter="20" v-if="info.basicinfo.beginjudgebutton">
                        <el-col>
                            <p>比赛已经进入评测阶段，请点击<el-button @click="assignproject" type="primary">分配作品</el-button>自动为每位评委分配作品</p>
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
          timestamp2datestr:function (stamp) {
              let date = new Date(stamp);
              return (Number(date.getMonth())+1)+'月'+date.getDate()+'日'+date.getHours()+'时';
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
                        return idx*3+2;
                    }
                    if(now<this.info.stageinfo[idx].handTimeEnd){
                        return idx*3+3;
                    }
                    if(now<this.info.stageinfo[idx].handTimeEnd){
                        return idx*3+4;
                    }
                }
                return this.info.stageinfo.length*3+2;
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
    font-size: 40px;
}
</style>