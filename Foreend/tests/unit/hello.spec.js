import hello from '../../src/components/hello.vue'
require('babel-register')();
require('chai')
require('@vue/test-utils')
describe('hello.vue', () => {
  it('increments count when button is clicked', () => {
    const wrapper = shallowMount(hello)
    wrapper.find('button').trigger('click')
    expect(wrapper.find('div').text()).contains('1')
  })
})