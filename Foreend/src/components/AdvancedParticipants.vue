<template>
    <div class="advanced-participants">
        <el-card  class="advanced-header">
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
            <div class="advanced-number">
                晋级规则:&nbsp;
                前
                <div v-if="already === -1" class="advanced-number-counter">
                    <el-input-number :min="0"
                                     :max="participants_number"
                                     maxwidth="30px"
                                     v-model="advanced_number"
                                     controls-position="right"
                                     size="small">
                    </el-input-number>
                </div>

                <div v-else class="advanced-number-counter">
                    <el-tag type="info">{{already}}</el-tag>
                </div>
                名晋级

                <div class="advanced-number-btn" v-if="already === -1">
                    <el-button type="success"
                               @click="ConfirmSubmit"
                    >设置</el-button>
                </div>
            </div>
        </el-card>


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
            <div > 选手共 {{participants_number}} 人</div>
        </div>

        <el-card>
            <el-table
                :data="current_page_participants"
                style="width: 100%">

                <el-table-column
                    min-width="1"
                    prop="no"
                    label="排名"
                >
                </el-table-column>
                <el-table-column
                    prop="username"
                    label="选手名称"
                    min-width="2"
                >
                </el-table-column>

                <el-table-column
                    label="分数"
                    min-width="2"
                >
                    <template slot="header" slot-scope="scope">
                        分数<el-button type="text" icon="el-icon-arrow-down" @click="SortCurrentParticipants"></el-button>
                    </template>
                    <template slot-scope="scope" >
                        <span v-if="current_page_participants[scope.$index].grade !== -1">
                            {{current_page_participants[scope.$index].grade}}
                        </span>
                        <el-button v-if="already === -1" type="text" icon="el-icon-edit" @click="ChangeGrade(scope.$index)"></el-button>
                    </template>

                </el-table-column>

                <el-table-column
                        label="原分数"
                        min-width="1"
                >
                    <template slot-scope="scope" v-if="current_page_participants[scope.$index].oldgrade !== -1">
                        {{current_page_participants[scope.$index].oldgrade}}
                    </template>
                </el-table-column>

                <el-table-column
                        prop="reason"
                        label="修改分数原因"
                        min-width="3">
                </el-table-column>


                <el-table-column
                        prop="university"
                        label="大学"
                        min-width="2">
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

        <el-dialog
                title="修改分数"
                :visible.sync="new_grade_visible"
                width="30%"
                >
            <div class="new-grade-item">
            新分数:
            <el-input-number
                v-model="new_grade_mark"
                size="small"
                :min="0"
                :max="100"
                >
            </el-input-number>
            </div>
            <div class="new-grade-item">
            修改原因：
            <el-input
                v-model="new_grade_reason"
                type="textarea"
                :row="3">
            </el-input>
            </div>

            <span slot="footer" class="new-grade-footer">
                <el-button @click="NewGradeCancel">取消</el-button>
                <el-button type="primary" @click="NewGradeConfirm">确定</el-button>
            </span>
        </el-dialog>
    </div>


</template>



<script>
    //import axios from 'axios'
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
              zone_menu: [{id:-1,value:'比赛统一赛区'}],
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
              advanced_number:0,
              already:-1,
              new_grade_visible:false,
              new_grade_mark:0,
              new_grade_reason:'',
              new_grade_index:0,
          }
        },
        mounted:function () {
            let vm = this;
            axios.post('/api/admin/zone',{contestid:this.contestid})
                .then(response=>{
                    if(response.data.msg === ''){
                        let len = response.data.list.length;
                        if (len === 0){
                            vm.zone_menu.splice(0,1,{id:-1,value:'比赛统一赛区'});
                        }
                        else{
                            for (let i = 0 ; i < len; i++){
                                vm.zone_menu.push(response.data.list[i]);
                            }
                        }
                        //automatically select first zone
                        vm.selected_zone = vm.zone_menu[0].id;
                        vm.ZoneChanged();
                    }
                    else{
                        vm.$message({
                            message: `获取赛区信息失败! ${response.data.msg}`,
                            type: 'error'
                        });

                    }
                })
                .catch(error=>{
                    //automatically select first zone
                    vm.selected_zone = vm.zone_menu[0].id;
                    vm.ZoneChanged();
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
                this.advanced_number = 0;
                this.total_page = 0;

                let vm = this;
                axios.post('/api/admin/advanced',{contestid:this.contestid,target:this.selected_zone})
                    .then(response=>{
                        if(response.data.msg === ''){
                            vm.participants_number = response.data.participants.length;
                            vm.participants = response.data.participants;
                            vm.already = response.data.already;
                            vm.SortParticipants();
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
                            {username:'1',grade:120,university:'ss',oldgrade:-1,reason:''},
                            {username:'2',grade:12,university:'dss',oldgrade:-1,reason:''},
                            {username:'3',grade:1122,university:'dss',oldgrade:-1,reason:''},
                            {username:'4',grade:-1,university:'dss',oldgrade:-1,reason:''},
                            {username:'5',grade:123,university:'dss',oldgrade:12,reason:'走后门打算打算的撒打算打算打算打算打算打算打算打算打算'},
                            {username:'6',grade:32,university:'dss',oldgrade:-1,reason:''},
                            {username:'7',grade:2,university:'dss',oldgrade:-1,reason:''},
                            {username:'8',grade:37,university:'dss',oldgrade:-1,reason:''},
                            {username:'9',grade:23213,university:'dss',oldgrade:-1,reason:''},
                            {username:'10',grade:3,university:'dss',oldgrade:-1,reason:''},
                            {username:'11',grade:43,university:'dss',oldgrade:-1,reason:''},
                            {username:'12',grade:17,university:'dss',oldgrade:-1,reason:''},
                        ];
                        vm.already = -1;
                        vm.participants_number = vm.participants.length;
                        vm.SortParticipants();
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
                temp.advanced = this.advanced_number;
                let vm = this;
                axios.post('/api/admin/setadvanced',temp)
                    .then(response=>{
                        if (response.data.msg !==''){
                            vm.$message({
                                message: `设置晋级选手失败! ${response.data.msg}`,
                                type: 'error'
                            });
                        }
                        else{
                            vm.$message({
                                message: `设置晋级选手成功!`,
                                type: 'success'
                            });
                            vm.already = vm.advanced_number;
                        }
                    });
            },
            SortParticipants:function(){
                this.participants.sort(function (a,b) {
                    return b.grade - a.grade;
                });
                //no
                for (let i = 0 ; i < this.participants_number; i++)
                    this.participants[i].no = i + 1;
            },
            SortCurrentParticipants:function () {
                this.current_participants.sort(function (a,b) {
                    return b.grade - a.grade;
                });
                this.CurrentPageChange(1);
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
            },
            ChangeGrade:function (index) {
                this.new_grade_reason = '';
                this.new_grade_mark = this.current_page_participants[index].grade;
                this.new_grade_index = index;
                this.new_grade_visible = true;
            },
            ConfirmSubmit:function () {
                let vm = this;
                this.$confirm('提交晋级名单后不可修改, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    vm.SubmitParticipants();
                }).catch(() => {
                    vm.$message({
                        type: 'info',
                        message: '已取消'
                    });
                });
            },
            NewGradeConfirm:function () {
                this.new_grade_visible = false;
                this.SubmitNewGrade();

            },
            NewGradeCancel:function () {
                this.new_grade_visible = false;
            },
            SubmitNewGrade:function () {
                let vm = this;
                if (this.new_grade_reason === ''){
                    vm.$message({
                        type: 'error',
                        message: `修改分数的原因不能为空!`
                    });
                    return;
                }

                if (this.new_grade_mark === this.current_page_participants[this.new_grade_index].grade){
                    vm.$message({
                        type: 'error',
                        message: `新分数和原分数不能一致!`
                    });
                    return;
                }

                axios.post('/api/admin/setnewgrade ',
                    {
                        contestid:this.contestid,
                        username:this.current_page_participants[this.new_grade_index].username,
                        grade:this.new_grade_mark,
                        reason:this.new_grade_reason
                    })
                    .then(
                        response=>{
                            if(response.data.msg === ''){
                                vm.$message({
                                    type: 'success',
                                    message: '修改分数成功'
                                });
                                if(vm.current_page_participants[vm.new_grade_index].oldgrade === -1)
                                    vm.current_page_participants[vm.new_grade_index].oldgrade = vm.current_page_participants[vm.new_grade_index].grade;
                                vm.current_page_participants[vm.new_grade_index].grade = vm.new_grade_mark;
                                vm.current_page_participants[vm.new_grade_index].reason = vm.new_grade_reason;
                                vm.SortParticipants();
                                vm.SortCurrentParticipants();
                            }
                            else{
                                vm.$message({
                                    type: 'error',
                                    message: `修改分数失败${response.data.msg}`
                                });
                            }
                        }
                    ).catch(error=>{
                    if(vm.current_page_participants[vm.new_grade_index].oldgrade === -1)
                        vm.current_page_participants[vm.new_grade_index].oldgrade = vm.current_page_participants[vm.new_grade_index].grade;
                    vm.current_page_participants[vm.new_grade_index].grade = vm.new_grade_mark;
                    vm.current_page_participants[vm.new_grade_index].reason = vm.new_grade_reason;
                    vm.SortParticipants();
                    vm.SortCurrentParticipants();
                });

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

.advanced-number{
    margin-top: 20px;
    margin-bottom: 20px;
}

.advanced-number-btn{
    margin-left: 30px;
    display: inline-block;
}

.advanced-number-counter{
    display: inline-block;
}
.new-grade-item{
    display: inline-block;
    margin-top: 10px;
    margin-bottom: 10px;
}
</style>