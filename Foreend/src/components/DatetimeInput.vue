<template>
<div class="datetime-input">
    <span class="register-input-title">{{ title }}</span><br>
    <input type="datetime-local" v-bind:value="value" v-on:input="$emit('input', $event.target.value)">
</div>
</template>

<script>
export default {
props:['value','title'],
}
</script>

<style>
.cdatetime-input{

}
</style>