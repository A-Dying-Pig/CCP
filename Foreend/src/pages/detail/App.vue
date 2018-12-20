<template><div id="app">
    <el-container>
        <el-header>
            <NavigationBar :username="musername"></NavigationBar>
        </el-header>
        <el-main>
            <CompetitionDetailAllInfo :info="allinfo" :type="type" :contestid="contestid"></CompetitionDetailAllInfo>

            <CompetitionDetailContents :info="allinfo" :showlist="showlist" :contestid="contestid" :type="type">
                <template slot="details">{{ allinfo.basicinfo.details }}</template>
            </CompetitionDetailContents>
        </el-main>
    </el-container>
    </div>
</template>
<script>

    import NavigationBar from "../../components/NavigationBar.vue";
    import CompetitionDetailAllInfo from '../../components/CompetitionDetailAllInfo.vue';
    import CompetitionDetailContents from '../../components/CompetitionDetailContents.vue';
    import axios from 'axios'
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.headers.common = {
        'X-CSRFToken':document.querySelector('#csrf-token input').value,
        'X-Requested-With': 'XMLHttpRequest'
    };

    export default {
        components: {NavigationBar,CompetitionDetailAllInfo,CompetitionDetailContents},
        props:{'contestid': {
                    type:Number,
                    default:-1
                },
                'musername':{
                    type:String,
                    default:''
                }
        },
        data:function () {
            return{
                showlist:[],
                type:0,
                allinfo:{
                    basicinfo:{
                        name:'111',
                        holders:[''],
                        sponsors:[''],
                        comtype:'',
                        details:"222",
                        beginjudgebutton:false
                    },
                    signupinfo:{
                        time:[1542593167172,1542593267172],
                        mode:'',
                        person:[
                            ''
                        ],
                        group:[
                        ]
                    },
                    stageinfo:[{
                        name:'',
                        details:'',
                        stageTimeBegin:1544827739311,
                        handTimeEnd:1544838739311,
                        evaluationTimeEnd:1544839739311,
                        mode:''
                    }]
                }
            }
        },
        methods:{
            getInfo:function () {
                let self = this;

                return axios.post('/api/competition/detail',{
                    contestid:self.contestid,
                }).then(function (response) {
                    self.allinfo=[];
                    self.allinfo = response.data.info;
                    self.type = response.data.type;
                    console.log(self.allinfo)
                    let now = Date.now();
                    self.showlist=[];
                    self.showlist.push({
                        value:'competitionfiles',
                        label:'比赛文件'
                    },{
                        value:'discussion',
                        label:'讨论区'
                    });
                    if(self.type===1){
                        //当不在提交阶段时，不可以提交作品
                        let showsubmit = true;
                        let begin = self.allinfo.signupinfo.time[1];
                        for(let stage of self.allinfo.stageinfo){
                            if((now>begin)&&(now<stage.handTimeEnd)){
                                showsubmit = true;
                            }
                            begin = stage.evaluationTimeEnd;
                        }
                        if(showsubmit){
                            self.showlist.push({
                                value:'submitwork',
                                label:'提交作品'
                            });
                        }
                    }
                    else if(self.type===2){
                        //当不在评测阶段时，不可以评测作品
                        let showgrade = true;
                        for(let stage of self.allinfo.stageinfo){
                            if((now<stage.evaluationTimeEnd)&&(now>stage.handTimeEnd)){
                                showgrade = true;
                            }
                        }
                        if(showgrade){
                            self.showlist.push({
                                value:'gradework',
                                label:'评委评分'
                            },{
                                value:'judgefinish',
                                label:'查看过往评分'
                            });
                        }
                    }
                    else if(self.type===3) {
                        self.showlist.push({
                            value: 'infochange',
                            label: '修改信息'
                        });
                        self.showlist.push({
                            value: 'participantstable',
                            label: '选手信息'
                        });
                        self.showlist.push({
                            value: 'judgelist',
                            label: '评委信息'
                        });
                        let showadvance = true;
                        let begin = self.allinfo.signupinfo.time[1];
                        for (let stage of self.allinfo.stageinfo) {
                            if ((now > begin) && (now < stage.stageTimeBegin)) {
                                showadvance = true;
                            }
                            begin = stage.evaluationTimeEnd;
                        }
                        if (showadvance) {
                            self.showlist.push({
                                value: 'advancedparticipants',
                                label: '设置晋级选手名单'
                            });
                        }
                        //if(self.allinfo.basicinfo.judgebegin === false){
                        let showjudgebegin = true;
                        for (let stage of self.allinfo.stageinfo) {
                            if ((now > stage.handTimeEnd) && (now < stage.evaluationTimeEnd)) {
                                showjudgebegin = true;
                            }
                        }
                        if (showjudgebegin) {
                            self.allinfo.basicinfo.beginjudgebutton = true;
                        }
                        else {
                            self.allinfo.basicinfo.beginjudgebutton = false;
                        }
                        //}
                        console.log(self.allinfo)

                    }

                }).catch(function (error) {
                    console.log('/api/competition/detail'+'错误！！')
                })
            }
        },
        created:function () {
            let self = this;
            console.log(self.contestid);
            self.getInfo();
        }
    }
</script>
<style></style>