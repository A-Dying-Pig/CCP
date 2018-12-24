import CompetitionCreatePage from '../../src/components/CompetitionCreatePage.vue'
import moxios from 'moxios'
import Vue from 'vue'
import ElementUI from 'element-ui'
Vue.use(ElementUI);
import { shallowMount,mount } from '@vue/test-utils'
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
describe('比赛创建', () => {
    let info = {
        basicinfo:{
            name:'121111',
            holders:['11123'],
            sponsors:['45678'],
            comtype:'微信小程序',
            details:"22111112",
            beginjudgebutton:false,
            img:'https://srv.carbonads.net/ads/click/x/GTND42QWCWSDV27YF6YLYKQMCEBI5K3ECKSIKZ3JCWBDP27ICYYIKK3KC6BIV2QNCW7DEK3EHJNCLSIZ?segment=placement:vuejsorg;'
        },
        signupinfo:{
            time:[1542593167172,1542593267172],
            mode:'1',
            person:[
                '61166'
            ],
            group:[
            ]
        },
        stageinfo:[{
            name:'111111111',
            details:'22222222',
            stageTimeBegin:1544827739311,
            handTimeEnd:1544838739311,
            evaluationTimeEnd:1544839739311,
            mode:'1'
        }]};
    let contestid = 2;
    let change = false;
    beforeEach(function () {
        moxios.install()
    });

    afterEach(function () {
        moxios.uninstall()
    });
    it('比赛创建信息发送成功', function (done) {
        moxios.withMock(function () {
            const wrapper = shallowMount(CompetitionCreatePage, {
                propsData: {
                    info: info,
                    change:change,
                    contestid: contestid
                }
            });
            let subbutton = wrapper.find('.submitbtn');
            console.log(subbutton.trigger('clllick'));

            moxios.wait(function () {
                let request = moxios.requests.mostRecent();
                expect(request.config.data).toEqual(JSON.stringify(info))
                request.respondWith({
                    status: 200,
                    response: {
                        code:0,
                        msg: ''
                    }
                }).then(function () {
                    done();
                })
            });
        });
    });
});