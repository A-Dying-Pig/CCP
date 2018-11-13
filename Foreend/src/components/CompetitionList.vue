<template>
<div class="competition-list">
        <td>{{com.number}}</td>
        <td>{{com.name}}</td>
        <td>{{com.organizer}}</td>
        <td>{{com.information}}</td>
        <td>{{com.detail}}</td>  
    </div>
</template>

<script>
export default{
props:['com'],
}
</script>

<style>
</style>