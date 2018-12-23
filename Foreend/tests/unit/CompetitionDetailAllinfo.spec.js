import CompetitionDetailAllinfo from '../../src/components/CompetitionDetailAllInfo.vue'
import moxios from 'moxios'
import Vue from 'vue'
import ElementUI from 'element-ui'
Vue.use(ElementUI);
import { shallowMount } from '@vue/test-utils'
const { getComputedStyle } = window
window.getComputedStyle = function getComputedStyleStub(el) {
    return {
        ...getComputedStyle(el),
        transitionDelay: '',
        transitionDuration: '',
        animationDelay: '',
        animationDuration: '',
    }
};
describe('props传值是否正确', () => {
    let info = {
            basicinfo:{
                name:'121',
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
            }]};
    let type = 1;
    let contestid = 5;
    beforeEach(function () {
        moxios.install()
    });

    afterEach(function () {
        moxios.uninstall()
    });
    moxios.withMock(function () {
        const wrapper = shallowMount(CompetitionDetailAllinfo,{
            propsData:{
                info:info,
                type:type,
                contestid:contestid
            }
        });
        moxios.wait(function () {
            let request = moxios.requests.mostRecent();
            let enrollnum = 100;
            request.respondWith({
                status: 200,
                response: {
                    enrollnum:enrollnum,
                    msg:''
                }
            }).then(function () {
                it('info传入成功', function (done) {
                    expect(wrapper.vm.info).toEqual(info);
                });

                it('type传入成功', function (done) {
                    expect(wrapper.vm.type).toEqual(type);
                });

                it('contestid传入成功', function (done) {
                    expect(wrapper.vm.contestid).toEqual(contestid);
                });
                done();
            })
        });
    });
});

describe('axios获取已经报名人数正确', () => {
    let info = {
        basicinfo:{
            name:'121',
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
        }]};
    let type = 1;
    let contestid = 5;
    moxios.install();
    moxios.withMock(function () {
            const wrapper = shallowMount(CompetitionDetailAllinfo,{
                propsData:{
                    info:info,
                    type:type,
                    contestid:contestid
                }
            });
            moxios.wait(function () {
                let request = moxios.requests.mostRecent();
                let enrollnum = 100;
                it('发送的request符合要求', function () {
                    console.log('------------------------',request.config.data)
                    expect(request.config.data["contestid"]).toEqual(contestid);
                });
                request.respondWith({
                    status: 200,
                    response: {
                        enrollnum:enrollnum,
                        msg:''
                    }
                }).then(function () {
                    it('返回的报名人数正确', function () {
                        console.log('**********************',wrapper.vm)
                        expect(wrapper.vm.enrollnum).toEqual(enrollnum);
                    });
                    done();
                })
            });
    });
});