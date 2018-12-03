<template>
    <div>
        <el-row :gutter="20">
            <el-col :offset="5" :span="14">
                <el-card shadow="always">
                    <el-row :gutter="24">
                        <el-col class="title" :span="5">
                            <b>{{ info.basicinfo.name }}</b>
                        </el-col>
                        <el-col v-if="(type == 0)&&(Date.now()>info.signupinfo.time[0])&&(Date.now()<info.signupinfo.time[1])" :span="5" :offset="14">
                            <el-button @click="clicksign" type="primary">报名参赛！</el-button>
                        </el-col>
                    </el-row>
                    <p></p>
                    <el-row :gutter="20">
                        <el-steps :space="50" :active="getActivestage()" finish-status="success" simple style="height:80px;font-size:small">
                            <el-step :title="timestamp2datestr(info.signupinfo.time[0]) + '报名开始'"></el-step>
                            <el-step :title="timestamp2datestr(info.signupinfo.time[1]) + '报名结束'"></el-step>
                            <template v-for="item in info.stageinfo">
                                <el-step :title="timestamp2datestr(item.stageTimeBegin)+item.name+'开始'"></el-step>
                                <el-step :title="timestamp2datestr(item.handTimeEnd)+item.name+'提交截止'"></el-step>
                                <el-step :title="timestamp2datestr(item.evaluationTimeEnd)+item.name+'评测截止'"></el-step>
                            </template>
                        </el-steps>
                    </el-row>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script>

    export default {
        props:['info','type','contestid'],
        data:function () {
            return{
                activeStage:0,
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
            }
        },
        created:function () {
            //activeStage
        }
    }
</script>

<style>
.title{
    text-align: left;
    font-size: 40px;
}
</style>