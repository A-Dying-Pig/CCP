import Vue from 'vue'
import CompetitionInfo from '@/components/CompetitionInfo'

describe('CompetitionInfo.vue', () => {
	it('提交创建比赛信息', () => {
    const wrapper = mount(CompetitionInfo);
    wrapper.setProps({
      finfo:{
        name:"肥宅大赛",
        holders:["1","2"],
        sponsors:["1"],
      //info.comtype:
        details:"hhhhhhhh"
      },
      typeid:1
    })
    const buttonGroup = wrapper.findAll('el-button')
    const button_submit = buttonGroup.at(0)
    button_submit.trigger('click')
    expect(wrapper.basicrules['name'][1]['message']).tobeequal("长度在5到30个字符")
  })
})