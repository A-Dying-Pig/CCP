<template>
<div class="input-wordlimit">   
                <span class="register-input-title">{{ title }}</span>
                <br>
                <input 
                    v-model.trim = "msg" 
                    v-on:input="validate"
                    class="register-input"
                >
                <span ><font v-bind:color="status_color">{{signal}}</font></span>  
                <br>
                <span class="register-input-info" v-if="wordmin && wordmax">字数限制{{ wordmin }}字到{{ wordmax }}字之间</span>
                <span class="register-input-info" v-else-if="wordmin">至少输入{{ wordmin }}字</span>
                <span class="register-input-info" v-else-if="wordmax">至多输入{{ wordmax }}字</span>
                <span class="register-input-info" v-else>无字数限制</span>
            </div>
</template>

<script>
export default{
props:['title','wordmin','wordmax'],
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
            var len = this.msg.length;
            if(this.wordmin&&this.wordmax){
                if((len>=this.wordmin)&&(len<=this.wordmax)){
                    this.status = 1;
                }
                else this.status=0;
                return;
            }
            else if(this.wordmin){
                if(len>=this.wordmin){
                    this.status = 1;
                }
                else this.status=0;
                return;
            }
            else if(this.wordmax){
                if(len<=this.wordmax){
                    this.status = 1;
                }
                else this.status=0;
                return;
            }
            else{
                this.status=0;
                return;
            }
        }
    }
}
</script>

<style src="./commonCSS/input.css"></style>