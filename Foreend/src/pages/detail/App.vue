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

    <el-container>
        <el-footer>
            <CCPFooter></CCPFooter>
        </el-footer>
    </el-container>
    </div>
</template>
<script>

    import NavigationBar from "../../components/NavigationBar.vue";
    import CompetitionDetailAllInfo from '../../components/CompetitionDetailAllInfo.vue';
    import CompetitionDetailContents from '../../components/CompetitionDetailContents.vue';
    import CCPFooter from "../../components/CCPFooter"
    //import axios from 'axios'
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.headers.common = {
      'X-CSRFToken':document.querySelector('#csrf-token input').value,
        'X-Requested-With': 'XMLHttpRequest'
    };

    export default {
        components: {NavigationBar,CompetitionDetailAllInfo,CompetitionDetailContents,CCPFooter},
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
                        name:'比赛标题',
                        holders:[''],
                        sponsors:[''],
                        comtype:'',
                        details:"",
                        beginjudgebutton:false,
                        img:'https://gss1.bdstatic.com/9vo3dSag_xI4khGkpoWK1HF6hhy/baike/crop%3D0%2C310%2C514%2C339%3Bc0%3Dbaike80%2C5%2C5%2C80%2C26/sign=e07c6748befd5266b36466549628bb18/bba1cd11728b4710d8a5966fcbcec3fdfd03238e.jpg',
                        briefintroduction:'比赛信息',
                    },
                    signupinfo:{
                        time:[1545874889225,1545974889225],
                        mode:'1',
                        person:[
                            ''
                        ],
                        group:[''
                        ]
                    },
                    stageinfo:[{
                        name:'',
                        details:'',
                        stageTimeBegin:1546074889225,
                        handTimeEnd:1546174889225,
                        evaluationTimeEnd:1546274889225,
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
                        let showsubmit = false;
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
                        let showgrade = false;
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
                        let showadvance = false;
                        let begin = self.allinfo.signupinfo.time[1];
                        for (let stage of self.allinfo.stageinfo) {
                            if ((now > begin) && (now < stage.stageTimeBegin)) {
                                showadvance = true;
                            }
                            begin = stage.evaluationTimeEnd;
                        }
                        if(now>begin){
                            showadvance = true;
                        }
                        if (showadvance) {
                            self.showlist.push({
                                value: 'advancedparticipants',
                                label: '设置晋级选手名单'
                            });
                        }
                        let showgrade = false;
                        for(let stage of self.allinfo.stageinfo){
                            if((now<stage.evaluationTimeEnd)&&(now>stage.handTimeEnd)){
                                showgrade = true;
                            }
                        }
                        if(showgrade===true){
                            self.showlist.push({
                                value: 'judgeprogress',
                                label: '评委进度查询'
                            });
                        }
                        if(self.allinfo.basicinfo.judgebegin === false){
                        let showjudgebegin = false;
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
                        }

                    }

                }).catch(function (error) {
                    console.log('/api/competition/detail'+'错误！！')
                })
            }
        },
        created:function () {
            let self = this;
            //self.getInfo();
        }
    }
</script>
<style></style>