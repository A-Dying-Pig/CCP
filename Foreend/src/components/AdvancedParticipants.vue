<template>
    <div class="advanced-participants">
        <div class = "advanced-zone">
            选择赛区: &nbsp; <el-select v-model="selected_zone" placeholder="请选择赛区" @change="ZoneChanged">
                <el-option
                    v-for="item in zone_menu"
                    :key="item.id"
                    :label="item.value"
                    :value="item.id"
                >
                </el-option>
            </el-select>
        </div>

        <el-card  class="advanced-selector">
            <div class="advanced-selector-btn">
                快速查找 <el-button icon="el-icon-search" type="text"></el-button>
            </div>

            <div class="advanced-selector-item">
                <el-input placeholder="输入选手名称" v-model="username_search" @blur="AdvancedSearch">
                    <span slot="prepend">选手名称</span>
                </el-input>
            </div>
            <div class="advanced-selector-item">
                <el-input placeholder="输入大学名称" v-model="university_search" @blur="AdvancedSearch">
                    <span slot="prepend">大学名称</span>
                </el-input>
            </div>
        </el-card>

        <div class="advanced-selected">
            <div >已选择晋级选手 {{select_count}}/{{participants_number}} 人</div>
        </div>

        <el-card>
            <div>
                <el-button @click="SelectCurrent" type="text"> 全选当前选手 </el-button>
            </div>
            <el-table
                :data="current_page_participants"
                style="width: 100%">

                <el-table-column
                    min-width="2">
                    <template slot="header" slot-scope="scope">
                    <el-checkbox :indeterminate="select_all_participants_of_current_page" v-model="select_all_current" @change="SelectCurrentPage"></el-checkbox>
                    全选页
                    </template>

                    <template slot-scope="scope">
                        <el-checkbox v-model="current_page_participants[scope.$index].advanced" @change="SelectChange(scope.$index)"></el-checkbox>
                    </template>
                </el-table-column>
                <el-table-column
                    prop="username"
                    label="选手名称"
                    min-width="3"
                >
                </el-table-column>
                <el-table-column
                    prop="grade"
                    label="分数"
                    min-width="2"
                >
                    <template slot="header" slot-scope="scope">
                        分数<el-button type="text" icon="el-icon-arrow-down" @click="SortByGrade"></el-button>
                    </template>
                </el-table-column>

                <el-table-column
                        prop="university"
                        label="大学"
                        min-width="3">
                </el-table-column>

            </el-table>
        </el-card>



        <el-pagination
                layout="prev, pager, next"
                :current-page="current_page"
                :page-count="total_page"
                @current-change="CurrentPageChange"
                @prev-click="PagePrevious"
                @next-click="PageNext"
                class="advanced-page">
        </el-pagination>

        <div class="submit-btn">
            <el-button @click="SubmitParticipants" type="success"> 提交 </el-button>
        </div>

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
        props:{
            contestid:{
                default:-1,
            },
        },
        data:function(){
          return {
              zone_menu: [{id:-1,value:'全部选手'}],
              selected_zone: null,

              participants_per_page:8,
              participants:[],
              current_participants:[],
              current_page_participants:[],
              current_participants_number:0,
              participants_number:0,
              current_page_participants_number:0,
              current_page:0,
              total_page:0,
              username_search:'',
              university_search:'',
              select_all_participants_of_current_page:true,
              select_all_current:false,
              select_count:0,
          }
        },
        mounted:function () {
            let vm = this;
            axios.post('/api/admin/zone',{contestid:this.contestid})
                .then(response=>{
                    if(response.data.msg === ''){
                        let len = response.data.list.length;
                        if (len === 0){
                            vm.zone_menu.splice(0,1,{id:-1,value:'全部赛区'});
                        }
                        else{
                            for (let i = 0 ; i < len; i++){
                                vm.zone_menu.push(response.data.list[i]);
                            }
                        }
                    }
                    else{
                        vm.$message({
                            message: `获取赛区信息失败! ${response.data.msg}`,
                            type: 'error'
                        });
                    }
                });
        },
        methods:{
            ZoneChanged:function () {
                this.current_page_participants_number = 0;
                this.participants.splice(0);
                this.current_page_participants.splice(0);
                this.current_participants.splice(0);
                this.participants_number = 0;
                this.current_participants_number = 0;
                this.current_page = 0;
                this.total_page = 0;
                this.select_count = 0;

                let vm = this;
                axios.post('/api/admin/advanced',{contestid:this.contestid,target:this.selected_zone})
                    .then(response=>{
                        if(response.data.msg === ''){
                            vm.participants_number = response.data.participants.length;
                            vm.participants = response.data.participants;
                            for (let i = 0; i < vm.participants_number; i++){
                                vm.participants[i].advanced = Boolean(vm.participants[i].advanced);
                                if(vm.participants[i].advanced)
                                    vm.select_count ++;
                            }
                             //default
                            vm.current_participants = [].concat(vm.participants);
                            vm.current_participants_number = vm.participants_number;
                            vm.total_page = Math.ceil(vm.current_participants_number / vm.participants_per_page);
                            if (vm.current_participants_number === 0 )
                                vm.total_page = 1;
                            vm.CurrentPageChange(1);
                        }
                        else{
                            vm.$message({
                                message: `获取选手信息失败! ${response.data.msg}`,
                                type: 'error'
                            });
                        }
                    })
                    .catch(error=>{
                        console.log(error);
                        vm.participants = [
                            {username:'1',grade:120,university:'ss',advanced:1},
                            {username:'2',grade:12,university:'dss',advanced:0},
                            {username:'3',grade:1122,university:'dss',advanced:0},
                            {username:'4',grade:122,university:'dss',advanced:0},
                            {username:'5',grade:112,university:'dss',advanced:1},
                            {username:'6',grade:32,university:'dss',advanced:0},
                            {username:'7',grade:2,university:'dss',advanced:0},
                            {username:'8',grade:37,university:'dss',advanced:1},
                            {username:'9',grade:23213,university:'dss',advanced:0},
                            {username:'10',grade:3,university:'dss',advanced:0},
                            {username:'11',grade:43,university:'dss',advanced:0},
                            {username:'12',grade:17,university:'dss',advanced:0},
                        ];
                        vm.participants_number = vm.participants.length;
                        for (let i = 0; i < vm.participants_number; i++){
                            vm.participants[i].advanced = Boolean(vm.participants[i].advanced);
                            if(vm.participants[i].advanced)
                                vm.select_count ++;
                        }
                        //default
                        vm.current_participants = [].concat(vm.participants);
                        vm.current_participants_number = vm.participants_number;
                        vm.total_page = Math.ceil(vm.current_participants_number / vm.participants_per_page);
                        if (vm.current_participants_number === 0 )
                            vm.total_page = 1;
                        vm.CurrentPageChange(1);

                    });

            },
            CurrentPageChange:function (cur_page) {
                this.current_page = cur_page;
                this.current_page_participants.splice(0);
                let offset = (this.current_page - 1 ) * this.participants_per_page;
                this.current_page_participants_number = this.participants_per_page;
                if (this.current_page === this.total_page)
                    this.current_page_participants_number = this.current_participants_number - (this.current_page - 1) * this.participants_per_page;
                for (let i = 0; i < this.current_page_participants_number; i ++ ){
                    this.current_page_participants.push(this.current_participants[offset + i]);
                }

                //select current page settings
                let sum = 0;
                for (let i = 0; i < this.current_page_participants_number; i++)
                    if (this.current_page_participants[i].advanced)
                        sum += 1;

                if (sum > 0 && sum < this.current_page_participants_number) {
                    this.select_all_participants_of_current_page = true;
                }
                else if (sum === 0) {
                    this.select_all_participants_of_current_page = false;
                    this.select_all_current = false;
                }
                else{
                    this.select_all_participants_of_current_page = false;
                    this.select_all_current = true;
                }

            },
            PagePrevious:function (cur_page) {
                this.CurrentPageChange(cur_page);
            },
            PageNext:function (cur_page) {
                this.CurrentPageChange(cur_page);
            },
            SubmitParticipants:function () {
                let temp = {};
                temp.contestid = this.contestid;
                temp.target = this.selected_zone;
                temp.participants = [];
                for (let i = 0; i < this.participants_number; i++){
                    if (this.participants[i].advanced){
                        temp.participants.push(this.participants[i].username);
                    }
                }
                let vm = this;
                axios.post('/api/admin/setadvanced',temp)
                    .then(response=>{
                        if (response.data.msg !==''){
                            vm.$message({
                                message: `设置晋级选手失败! ${response.data.msg}`,
                                type: 'error'
                            });
                        }
                    })
            },
            SelectChange:function (index) {
                //current page participants
                let ad = this.current_page_participants[index].advanced;
                if (ad)
                    this.select_count ++;
                else
                    this.select_count --;

                let sum = 0;
                for (let i = 0; i < this.current_page_participants_number; i++)
                    if (this.current_page_participants[i].advanced)
                        sum += 1;
                //current participants
                //this.current_participants[(this.current_page - 1) * this.participants_per_page + index].advanced = ad;
                //participants
                //for (let i = 0; i < this.participants_number; i++){
                //    if (this.participants[i].username === this.current_page_participants[index].username){
                //        this.participants[i].advanced = ad;
                //    }
                //}
                //console.log(this.participants);

                if (sum > 0 && sum < this.current_page_participants_number) {
                    this.select_all_participants_of_current_page = true;
                }
                else if (sum === 0) {
                    this.select_all_participants_of_current_page = false;
                    this.select_all_current = false;
                }
                else{
                    this.select_all_participants_of_current_page = false;
                    this.select_all_current = true;
                }

            },
            SelectCurrentPage:function (all) {
                this.select_all_participants_of_current_page = false;
                //current page participants
                for (let i = 0; i < this.current_page_participants_number; i++) {
                    this.current_page_participants[i].advanced = all;
                }

                //current participants
                //let offset = (this.current_page - 1) * this.participants_per_page;
                //for (let i = 0; i < this.current_page_participants_number; i++) {
                //    this.current_participants[offset + i].advanced = all;
                //}
                //participants
                //for (let i = 0; i < this.participants_number; i++){
                //    for (let j = 0; j < this.current_page_participants_number; j++){
                //        if (this.participants[i].username === this.current_page_participants[j].username){
                //            this.participants[i].advanced = all;
                //            break;
                //        }
                //    }
                //}
                //console.log(this.participants);
                this.GetCount();
            },
            SortByGrade:function () {
                this.current_participants.sort(function (a,b) {
                    return b.grade - a.grade;
                });
                if (this.total_page !== 0) {
                    this.CurrentPageChange(1);
                }
            },
            SelectCurrent:function () {
                this.select_all_participants_of_current_page = false;
                //current page participants
                this.select_all_current = true;
                //current participants
                for (let i = 0 ; i < this.current_participants_number; i++)
                    this.current_participants[i].advanced = true;
                //participants
                //for (let i = 0 ; i < this.participants_number; i++)
                //    for (let j = 0; j < this.current_participants_number; j++)
                //        if (this.participants[i].username === this.current_participants[j].username){
                //            this.participants[i].advanced = true;
                //        }
                //console.log(this.participants);
                this.GetCount();
            },
            GetCount:function () {
                this.select_count = 0;
                for (let i = 0 ; i < this.participants_number; i++)
                        if (this.participants[i].advanced){
                            this.select_count ++;
                        }
            },
            AdvancedSearch:function () {
                this.current_participants.splice(0);
                this.current_participants_number = 0;
                this.total_page = 0;
                this.current_page = 0;

                //default
                this.current_participants = [].concat(this.participants);
                if (this.username_search !== ''){
                    //select name
                    let vm = this;
                    this.current_participants = this.current_participants.filter(function (element) {
                        return element.username === vm.username_search;
                    });
                }

                if (this.university_search !== ''){
                    let vm = this;
                    this.current_participants = this.current_participants.filter(function (element) {
                        return element.university === vm.university_search;
                    });
                }

                this.current_participants_number = this.current_participants.length;
                this.total_page = Math.ceil(this.current_participants_number / this.participants_per_page);
                if(this.total_page === 0)
                    this.total_page = 1;

                this.CurrentPageChange(1);
            }
        },
    }


</script>


<style>
.advanced-page{
    text-align: center;
    margin-top: 40px;
    margin-bottom: 20px;
}

.submit-btn{
    margin-top: 10px;
    text-align: center;
}

.advanced-selector{
    margin-top: 20px;
    margin-bottom: 20px;
}

.advanced-selector-item{
    margin-top: 10px;
    margin-bottom: 10px;
    font-size: 12px;
}
.advanced-selected{
    margin-top: 10px;
    margin-bottom: 10px;
}
</style>