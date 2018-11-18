<template>
<div>
    <el-row type="flex" class="row-bg" justify="center"><el-col :span="6"><div class="title">阶段{{ index+1 }}</div></el-col></el-row>
    <el-form v-bind:model="info" :rules="rules" ref="info" label-width="100px" label-position="top">
        <el-row :gutter="20">
            <el-col :span="12" :offset="6">
                <el-form-item label="阶段名称" prop="name" label-width="100">
                    <el-input v-model="info.name"></el-input>
                </el-form-item>
            </el-col>
        </el-row>

        <el-row :gutter="20">
            <el-col :offset="6" :span="12">
                <el-form-item label="阶段详细信息" prop="details" label-width="100">
                <el-input type="textarea" :rows="5" placeholder="请输入详细信息" v-model="info.details">
                </el-input>
            </el-form-item>
            </el-col>
        </el-row>

        <el-row :gutter="20">
            <el-col :offset="6">
                <el-form-item label="选手提交截止时间（开始时间承接上一阶段）" prop="handTimeEnd">
                    <el-date-picker v-model="info.handTimeEnd" type="datetime" placeholder="选择日期时间"></el-date-picker>
                </el-form-item>
            </el-col>
        </el-row>

        <el-row :gutter="20">
            <el-col :offset="6">
                <el-form-item label="评测截止时间（开始时间承接选手提交截止时间）" prop="evaluationTimeEnd">
                    <el-date-picker v-model="info.evaluationTimeEnd" type="datetime" placeholder="选择日期时间"></el-date-picker>
                </el-form-item>
            </el-col>
        </el-row>

        <el-row :gutter="20">
            <el-col :offset="6">
                <el-form-item label="评测方式" prop="mode">
                    <el-radio-group v-model="info.mode">
                        <el-radio-button label="在线预览"></el-radio-button>
                        <el-radio-button label="本地评测"></el-radio-button>
                        <el-radio-button label="线下评测"></el-radio-button>
                        <el-radio-button label="无评测"></el-radio-button>
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
        props:['tinfo','index'],
        data:function () {
            return {
                info:this.tinfo,
                rules:{
                    name:[{required:true,message:'请输入阶段名称',trigger:'blur'},
                        {max:10,message:'长度不超过10个字符',trigger:'blur'}],
                    handTimeEnd:[{required:true,message:'请指定提交截止时间',trigger:'change'}],
                    evaluationTimeEnd:[{required:true,message:'请指定评测截止时间',trigger:'change'}],
                    mode:[{required:true,message:'请指定评测方式',trigger:'change'}],
                    detail:[{required:true,message:'请输入阶段信息',trigger:'blur'}]
                }
            }
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
        }
    }
}
</script>