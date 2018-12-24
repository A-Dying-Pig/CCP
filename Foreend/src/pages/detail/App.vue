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
    //import axios from 'axios'
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
                        beginjudgebutton:false,
                        img:'http://img.zcool.cn/community/01f9ea56e282836ac72531cbe0233b.jpg@2o.jpg',
                        briefintroduction:'本次智能营销科技大赛由平安金融壹账通联合科赛举办，致力于发掘 AI 时代最有创意和趣味的AI 营销产品方案。大赛围绕将已有的 AI 模型应用到生活中的具体营销场景，让技术真正落地。不论你是 AI 技术人才还是营销产品人才，都可以来一决高下！'
                    },
                    signupinfo:{
                        time:[1542593167172,1542593267172],
                        mode:'1',
                        person:[
                            ''
                        ],
                        group:[''
                        ]
                    },
                    stageinfo:[{
                        name:'初赛',
                        details:'',
                        stageTimeBegin:1544827739311,
                        handTimeEnd:1544838739311,
                        evaluationTimeEnd:1554839739311,
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
                        if (showadvance) {
                            self.showlist.push({
                                value: 'advancedparticipants',
                                label: '设置晋级选手名单'
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
            self.getInfo();
        }
    }
</script>
<style></style>