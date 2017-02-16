<template>
    <div class="scheduler-list">
        <div class="container-fluid">
            <ol class="breadcrumb text-left">
                <li><a href="#">定时任务管理</a></li>
                <li class="active">任务列表</li>
            </ol>
            <div>
                <div class="pull-right">
                    <form class="form-inline">
                        <div class="form-group">
                            <input type="text" class="form-control input-sm" id="start" placeholder="定时任务ID" style="border-radius:3px 0 0 3px">
                            <!-- <button type="button" class="btn btn-sm btn-primary pull-right" style="width:100px;border-radius:0 3px 3px 0;">搜索</button> -->
                        </div>
                    </form>
                </div>
                <div class="text-left" style="margin-bottom:7px;">
                    <button type="button" class="btn btn-sm btn-primary opeara" v-on:click="startScheduler">启动</button>
                    <button type="button" class="btn btn-sm btn-warning opeara" v-on:click="stopScheduler">关闭</button>
                    <button type="button" class="btn btn-sm btn-success opeara"  data-toggle="modal" data-target="#post-scheduler">新建任务</button>
                </div>
            </div>
            <div>
                <div class="pull-right">
                    <select class="form-control input-sm pull-right" style="padding:2px;">
                        <option>全部</option>
                        <option>定时任务</option>
                        <option>间隔时间任务</option>
                    </select>
                </div>
                <div class="text-left">
                    <button type="button" class="btn btn-sm btn-primary opeara">全选</button>
                    <button type="button" class="btn btn-sm btn-warning opeara">取消全选</button>
                    <button type="button" class="btn btn-sm btn-danger opeara">删除选中</button>
                </div>
            </div>
            <hr/>
            <table class="table table-hover table-striped table-bordered">
                <thead>
                    <tr>
                        <th v-for="th in table.th">{{ th }}</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="item in items">
                        <td><input type="checkbox" value=""></td>
                        <td>{{ item.id }}</td>
                        <td>{{ item.name }}</td>
                        <td>{{ item.next_run_time }}</td>
                        <td>{{ item.pending }}</td>
                        <td style="width:240px;">
                            <div class="btn-group btn-group-justified" role="group" style="margin-bottom:7px;">
                                <a class="btn btn-sm btn-warning opeara-item" v-on:click="getScheduler(item)">查看</a>
                                <a class="btn btn-sm btn-success opeara-item" v-on:click="updateScheduler(item.id)">修改</a>
                                <a class="btn btn-sm btn-danger opeara-item" v-on:click="deleteScheduler(item.id)">删除</a>
                            </div>
                            <div class="btn-group btn-group-justified" role="group">
                                <a class="btn btn-sm btn-warning opeara-item">暂停</a>
                                <a class="btn btn-sm btn-success opeara-item">恢复</a>
                                <a class="btn btn-sm btn-danger opeara-item">执行</a>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <NewScheduler></NewScheduler>
        <ViewScheduler :scheduler="scheduler"></ViewScheduler>
        <DeleteScheduler :schedulerId="schedulerId"></DeleteScheduler>
        <UpdateScheduler :schedulerId="schedulerId"></UpdateScheduler>
    </div>
</template>

<script>
 import PageInfo from './common/pageinfo'
 import NewScheduler from './new'
 import ViewScheduler from './item'
 import UpdateScheduler from './update'
 import DeleteScheduler from './delete'

 export default {
     components: {
         PageInfo,
         NewScheduler,
         ViewScheduler,
         UpdateScheduler,
         DeleteScheduler
     },
     data() {
         return {
             table: {
                 'th': ['选择', 'ID', '定时类型', '运行时间', '运行状态', '操作']
             },
             items: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
             scheduler:0,
             schedulerId:0,
             pageinfo: {}
         }
     },
     created() {
         this.getSchedulerList()
     },
     methods: {
         getSchedulerList: function() {
             this.$http.get('http://127.0.0.1:5000/scheduler/')
                 .then((response) => {
                     this.items = response.body.data
                     this.pageinfo = response.body.pageinfo
                 })
                 .catch(function(response) {
                     console.log(response)
                 })
         },
         getScheduler: function(scheduler) {
             this.scheduler = scheduler
             $('#get-scheduler').modal('toggle')
         },
         updateScheduler: function(schedulerId) {
             this.schedulerId = schedulerId
             $('#update-scheduler').modal('toggle')
         },
         deleteScheduler: function(schedulerId) {
             this.schedulerId = schedulerId
             $('#delete-scheduler').modal('toggle')
         },
         startScheduler: function(event) {
             this.$http.post('http://127.0.0.1:5000/scheduler/status/', {
                 headers: {
                     "Content-Type": 'application/json',
                 }
             })
                 .then((response) => {
                     alert('success')
                 })
                 .catch(function(response) {
                     console.log(response)
                 })
         },
         stopScheduler: function(event) {
             this.$http.delete('http://127.0.0.1:5000/scheduler/status/', {
                 headers: {
                     "Content-Type": 'application/json',
                 }
             })
                 .then((response) => {
                     alert('success')
                 })
                 .catch(function(response) {
                     console.log(response)
                 })
         },
     }
 }
</script>

<style>
 .opeara {
     width: 85px;
 }
 
 .opeara-item {
     width: 56px;
 }
 /* .scheduler-list {
    background-color: #f5f5f5;
    border-radius: 4px;
    } */
 
 .breadcrumb {
     background-color: #fff;
 }
</style>
