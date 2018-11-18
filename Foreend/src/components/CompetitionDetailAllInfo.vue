<template>
    <div>
        <el-row :gutter="20">
            <el-col :offset="5" :span="14">
                <el-card shadow="always">
                    <el-row :gutter="20">
                        <el-col :space="10" class="title">
                            {{ info.basicinfo.name }}
                        </el-col>
                    </el-row>
                    <p></p>
                    <el-row :gutter="20">
                        <el-steps :space="50" :active="getActivestage()" finish-status="success" simple style="height:80px;font-size:small">
                            <el-step :title="timestamp2datestr(info.signupinfo.time[0]) + '报名开始'"></el-step>
                            <el-step :title="timestamp2datestr(info.signupinfo.time[1]) + '报名结束'"></el-step>
                            <template v-for="item in info.stageinfo">
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
        props:['info'],
        data:function () {
            return{
                activeStage:0,
            }
        },
        methods:{
          timestamp2datestr:function (stamp) {
              let date = new Date(stamp);
              return date.getMonth()+'月'+date.getDate()+'日'+date.getHours()+':'+date.getMinutes();
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
                    if(now<this.info.stageinfo[idx].handTimeEnd){
                        return idx*2+2;
                    }
                    if(now<this.info.stageinfo[idx].handTimeEnd){
                        return idx*2+3;
                    }
                }
                return this.info.stageinfo.length*2+2;
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
    font-size: 20px;
}
</style>