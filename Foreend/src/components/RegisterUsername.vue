<template>
<div class="register-input-username">   
                <span class="register-input-title">用户名(username)</span>
                <br>
                <input 
                    v-model.trim="msg" 
                    v-on:input="validate"
                    class="register-input"
                >
                <span><font v-bind:color="status_color">{{signal}}</font></span>
                <br>
                <span class="register-input-info">数字,字母,下划线的组合</span>
            </div>
</template>

<script>
export default{
data:function(){
return {
            msg: '',
            status_color:'gray',
            status:-1,
        }
    },
computed:{
        signal:function () {
            if (this.status === -1 || this.msg.length === 0) {
                this.status_color = 'gray';
                return '?';
            }
            if (this.status === 0) {
                this.status_color = 'red';
                return '✕';
            }
            if (this.status === 1) {
                this.status_color = 'green';
                return '✓';
            }
        }
    },
    methods:{
        validate:function () {
            if(/^[a-zA-Z0-9_]+$/.test(this.msg) === false) {
                this.status = 0;
                return;
            }
            this.status = 1;
        }
    }}
</script>

<style src="./commonCSS/input.css"></style>