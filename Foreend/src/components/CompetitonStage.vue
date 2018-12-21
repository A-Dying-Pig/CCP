<template>
<div>
    <el-row :gutter="12" type="flex" class="row-bg" justify="center"><el-col><div class="title">阶段{{ index+1 }}</div></el-col></el-row>
    <el-form v-bind:model="info" :rules="rules" ref="info" label-width="100px" label-position="top">
        <el-row>
            <el-col>
                <el-form-item label="阶段名称" prop="name" label-width="100" class="stage-name">
                    <el-input  v-model="info.name" :disabled="editableinput.name"></el-input>
                </el-form-item>
            </el-col>
        </el-row>

        <el-row>
            <el-col>
                <el-form-item label="阶段详细信息" prop="details" label-width="100" class="stage-info">
                <el-input type="textarea" :rows="5" placeholder="请输入详细信息" v-model="info.details" :disabled="editableinput.details">
                </el-input>
            </el-form-item>
            </el-col>
        </el-row>

        <el-row>
            <el-col>
                <el-form-item label="阶段开始时间" prop="stageTimeBegin" class="stage-start-time">
                    <el-date-picker v-model="info.stageTimeBegin" type="datetime" placeholder="选择日期时间" :disabled="editableinput.stageTimeBegin"></el-date-picker>
                </el-form-item>
            </el-col>
        </el-row>

        <el-row>
            <el-col>
                <el-form-item label="选手提交截止时间（开始时间为阶段开始时间）" prop="handTimeEnd" class="stage-submit-end-time">
                    <el-date-picker v-model="info.handTimeEnd" type="datetime" placeholder="选择日期时间" :disabled="editableinput.handTimeEnd"></el-date-picker>
                </el-form-item>
            </el-col>
        </el-row>

        <el-row>
            <el-col>
                <el-form-item label="评测截止时间（开始时间承接选手提交截止时间）" prop="evaluationTimeEnd" class="stage-judge-end-time">
                    <el-date-picker v-model="info.evaluationTimeEnd" type="datetime" placeholder="选择日期时间" :disabled="editableinput.evaluationTimeEnd"></el-date-picker>
                </el-form-item>
            </el-col>
        </el-row>

        <el-row>
            <el-col>
                <el-form-item label="赛区划分" prop="zone" class="region-select">
                    <el-radio-group v-model="info.zone" :disabled="editableinput.zone">
                        <el-radio-button label="统一赛区"></el-radio-button>
                        <el-radio-button label="按省划分"></el-radio-button>
                        <el-radio-button label="按地区划分"></el-radio-button>
                    </el-radio-group>
                </el-form-item>
            </el-col>
        </el-row>

    </el-form>
</div>
</template>

<style>

</style>

<script>

export default {
        components:{

        },
        props:['tinfo','index','change','stagebegintime'],
        data:function () {
            let hourVali=function (rule, value, callback) {
                let date = new Date(value);
                if(date.getMinutes()||date.getSeconds()){
                    callback(new Error("必须为整小时数"));
                }
                callback();
            };
            return {
                info:this.tinfo,
                rules:{
                    name:[{required:true,message:'请输入阶段名称',trigger:'blur'},
                        {max:10,message:'长度不超过10个字符',trigger:'blur'}],
                    handTimeEnd:[{required:true,message:'请指定提交截止时间',trigger:'change'}],
                    evaluationTimeEnd:[{required:true,message:'请指定评测截止时间',trigger:'change'}],
                    zone:[{required:true,message:'请指定赛区划分方式',trigger:'change'}],
                    detail:[{required:true,message:'请输入阶段信息',trigger:'blur'}],
                    stageTimeBegin:[{required:true,message:'请指定阶段开始时间',trigger:'change'}],
                },
                editableinput:{
                    name:false,
                    details:false,
                    stageTimeBegin:false,
                    handTimeEnd:false,
                    evaluationTimeEnd:false,
                    zone:false
                }
            }
        },
    mounted:function(){
    },
    methods:{
        validate:function () {
            var flag=true;
            this.$refs.info.validate((valid) => {
                if (valid) {
                    flag = true;
                } else {
                    flag = false;
                }
            });
            return flag;
        },
        checkhour:function (time) {
            console.log(time)
            return false;
        }
    },
    created:function () {
            if(this.change){
                //console.log(this.stagebegintime);
                let now = Date.now();
                //let now = 1542893167173;
                if(!this.stagebegintime){
                    return;
                }
                if(now<this.info.stageTimeBegin){
                    return;
                }
                else if((now>this.info.stageTimeBegin)&&(now<this.info.handTimeEnd)){
                    this.editableinput['name']=true;
                    this.editableinput['details']=true;
                    this.editableinput['stageTimeBegin']=true;
                    this.editableinput['zone']=true;
                }
                else if((now>this.info.handTimeEnd)&&(now<this.info.evaluationTimeEnd)){
                    this.editableinput['name']=true;
                    this.editableinput['details']=true;
                    this.editableinput['stageTimeBegin']=true;
                    this.editableinput['handTimeEnd']=true;
                    this.editableinput['zone']=true;
                }
                else {
                    this.editableinput['name']=true;
                    this.editableinput['details']=true;
                    this.editableinput['stageTimeBegin']=true;
                    this.editableinput['handTimeEnd']=true;
                    this.editableinput['evaluationTimeEnd']=true;
                    this.editableinput['zone']=true;
                }
            }

    }
}
</script>