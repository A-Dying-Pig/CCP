<template>
    <div>
        <el-button type="primary" plain @click="OnSubmit">确认修改</el-button>
        <el-table
                :data="contests"
                style="width: 100%">

            <el-table-column
                    prop="title"
                    label="比赛名称"
                    min-width="4"
            >
            </el-table-column>
            <el-table-column
                    label="轮播比赛?"
                    min-width="2"
            >
                <template slot-scope="scope">
                    <div v-show="contests[scope.$index].is_slider === 1">
                        是
                        <el-button type="danger" icon="el-icon-minus" circle @click="Slider_No(scope.$index)" size="mini"></el-button>
                    </div>
                    <div v-show="contests[scope.$index].is_slider === 0">
                        否
                        <el-button type="success" icon="el-icon-plus" circle @click="Slider_Yes(scope.$index)" size="mini"></el-button>
                    </div>
                </template>
            </el-table-column>


            <el-table-column
                    label="热门比赛?"
                    min-width="2"
            >
                    <template slot-scope="scope">
                        <div v-show="contests[scope.$index].is_hot === 1">
                            是
                            <el-button type="danger" icon="el-icon-minus" circle @click="Hot_No(scope.$index)" size="mini"></el-button>
                        </div>
                        <div v-show="contests[scope.$index].is_hot === 0">
                            否
                            <el-button type="success" icon="el-icon-plus" circle @click="Hot_Yes(scope.$index)" size="mini"></el-button>
                        </div>
                    </template>
            </el-table-column>
        </el-table>


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
        props: {},
        data:function () {
            return{
                contests:[],
                hot_number:0,
                max_hot:4,
            }
        },
        mounted:function () {
            let vm = this;
            axios.post('/api/super/indexinfo')
                .then(response=>{
                    if (response.data.msg === ''){
                        vm.contests = response.data.contests;
                        vm.hot_number = 0;
                        let len = vm.contests.length;
                        for (let  i = 0 ; i < len; i++){
                            if(vm.contests[i].is_hot === 1){
                                vm.hot_number += 1;
                            }
                        }
                    }
                    else{
                        vm.$message({
                            message:`获取首页信息失败! ${response.data.msg}`,
                            type:'error'
                        });
                    }
                })
                .catch(error=>{
                    console.log(error);
                    vm.contests = [
                        {contestid:1,is_slider:1,is_hot:0,title:'测试比赛1'},
                        {contestid:2,is_slider:0,is_hot:1,title:'测试比赛2'},
                        {contestid:3,is_slider:1,is_hot:1,title:'测试比赛3'},
                        {contestid:4,is_slider:0,is_hot:0,title:'测试比赛4'},
                        {contestid:5,is_slider:0,is_hot:1,title:'测试比赛5'},
                        {contestid:6,is_slider:1,is_hot:1,title:'测试比赛6'},
                        {contestid:7,is_slider:0,is_hot:0,title:'测试比赛7'},
                    ];
                    vm.hot_number = 0;
                    let len = vm.contests.length;
                    for (let  i = 0 ; i < len; i++){
                        if(vm.contests[i].is_hot === 1){
                            vm.hot_number += 1;
                        }
                    }
                });
        },
        methods:{
            OnSubmit:function () {
                let len = this.contests.length;
                let temp = {};
                temp.slider = [];
                temp.hot = [];
                for (let i = 0; i < len; i++){
                    if (this.contests[i].is_slider === 1)
                        temp.slider.push(this.contests[i].contestid);
                    if (this.contests[i].is_hot === 1)
                        temp.hot.push(this.contests[i].contestid);
                }
                let vm = this;
                axios.post('/api/super/setindex',temp)
                    .then(response=>{
                        if(response.data.msg === ''){
                            vm.$message({
                                message:`修改首页信息成功!`,
                                type:'success'
                            });
                        }
                        else{
                            vm.$message({
                                message:`修改首页信息失败! ${response.data.msg}`,
                                type:'error'
                            });
                        }
                    })
                },
            Slider_Yes:function (index) {
                this.contests[index].is_slider = 1;
            },
            Slider_No:function (index) {
                this.contests[index].is_slider = 0;
            },
            Hot_Yes:function (index) {
                if(this.hot_number < this.max_hot){
                    this.contests[index].is_hot = 1;
                    this.hot_number += 1;
                }
                else{
                    this.$message({
                        message:`最多设置${this.max_hot}个热门比赛!`,
                        type:'error'
                    });
                }

            },
            Hot_No:function (index) {
                this.contests[index].is_hot = 0;
                this.hot_number -= 1 ;
            }
        }
    }

</script>

<style>



</style>