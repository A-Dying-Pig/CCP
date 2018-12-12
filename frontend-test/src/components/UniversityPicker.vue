<template>
    <div class = 'university-picker'>
        <span class='university-picker-label'>所在大学</span>
        <el-select v-model="selected_university" filterable placeholder="请选择大学" @change="OnSelect">
            <el-option
                v-for="(item,index) in all_university"
                :key="index"
                :label="item.label"
                :value="item.value">
            </el-option>
        </el-select>

        <div class="university-picker-others">
            <span class='university-picker-note'>可输入名称搜索,若没有您的学校，请选择'其它'</span>
            <el-input v-show="selected_university === '其它'" v-model="other_university" placeholder="请输入您的学校" @blur="OnInput"></el-input>
        </div>
    </div>
</template>


<script>
    var UniversityData = require('./ChinaUniversity.json');
    export default {
        data:function(){
            return{
                all_university:[],
                other_university:'',
                selected_university:'',
            }
        },
        mounted:function () {
            this.all_university = eval(UniversityData);
        },
        methods:{
            OnSelect:function () {
                if(this.selected_university != '其它'){
                    this.$emit('new-university',this.selected_university);
                }
            },
            OnInput:function () {
                this.$emit('new-university',this.other_university);
            }
        }

    }
</script>


<style>
    .university-picker-others{
        margin-top: 5px;
    }
    .university-picker-label{
        padding-right: 15px;
    }
    .university-picker-note{
        font-size: 14px;
        color:gray;
    }
</style>