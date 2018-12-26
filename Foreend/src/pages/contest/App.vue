<template><div id="app">
    <el-container>
        <el-header>
            <NavigationBar :username="musername"></NavigationBar>
        </el-header>

        <el-main>
            <el-row :gutter="0">
                <div class="choose-type">
                    <el-radio-group v-model="the_type" label="比赛类型" @change="SubmitType">
                        <el-radio v-for="(item,index) in comtypes"
                          :label="item.value"
                          :key="index">
                            {{item.label}}
                        </el-radio>
                        <el-radio label="all">全选</el-radio>
                    </el-radio-group>
                </div>
            </el-row>

            <el-row :gutter="0" v-for="(item,index) in contest_list.array" :key="index">
                <el-col :span="12" :offset="6" >
                    <ContestListItem
                            :contestid="item.contestid"
                            :intro="item.intro"
                            :img_url="item.img_url"
                            :title="item.title"
                            :enroll_number="item.enroll_number"
                            @new-contest-detail="ShowContestDetail"></ContestListItem>
                </el-col>
            </el-row>

            <el-pagination
                    layout="prev, pager, next"
                    :current-page="contest_list.current_page_num"
                    :page-count="contest_list.total_page_num"
                    @current-change="CurrentPageChange"
                    @prev-click="PagePrevious"
                    @next-click="PageNext"
                    class="profile-page">
            </el-pagination>
        </el-main>
    </el-container>
    <el-container>
        <el-footer>
            <CCPFooter></CCPFooter>
        </el-footer>
    </el-container>
    </div>
</template>

<script>
    import NavigationBar from "../../components/NavigationBar";
    import ContestListItem from "../../components/ContestListItem"
    import CCPFooter from "../../components/CCPFooter"
    //import axios from 'axios'

    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.headers.common = {
      'X-CSRFToken':document.querySelector('#csrf-token input').value,
        'X-Requested-With': 'XMLHttpRequest'
    };

    export default {
        props:['musername','pageTotal'],
        components: {
            NavigationBar,
            ContestListItem,
            CCPFooter
        },
        data:function(){
            return{
                contest_list:{
                    current_page_num:1,
                    total_page_num:1,
                    array: [
                    ]
                },
                comtypes:[
                    {label:'微信小程序',value:'weixin'},
                    {label:'web开发',value:'web'}],
                the_type:'all',
            }
        },
        mounted:function () {
            let vm = this;
            axios.post('/api/competition/list',{pageNum:1,type:'all'})
                .then(response=>{
                    if(response.data.msg ==='')
                        vm.contest_list = response.data;
                    else {
                        vm.$message({
                            message: `获取信息失败`,
                            type: 'error'
                        });
                    }
                });
        },
        methods:{
            CurrentPageChange:function (cur_page) {
                let vm = this;
                axios.post('/api/competition/list',{pageNum:cur_page,type:this.the_type})
                    .then(response=>{
                        if(response.data.msg ==='')
                            vm.contest_list = response.data;
                        else {
                            vm.$message({
                                message: `获取信息失败`,
                                type: 'error'
                            });
                        }
                    })
            },
            PagePrevious:function (cur_page) {
                this.CurrentPageChange(cur_page);
            },
            PageNext:function (cur_page) {
                this.CurrentPageChange(cur_page);
            },
            ShowContestDetail:function (id) {
                window.location.href = `/detail?contestid=${id}`;
            },
            SubmitType(val)
            {
                let vm = this;
                this.the_type = val;
                axios.post('/api/competition/list', {type:val,pageNum:1})
                    .then(response=>{
                        vm.contest_list = response.data;
                })
            },

        }
    }
</script>

<style>

    .profile-page{
        margin-top: 60px;
        text-align: center;
    }

    .el-row{
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .choose-type{
        text-align: center;
        margin-top: 15px;
        margin-bottom: 15px;
    }


</style>