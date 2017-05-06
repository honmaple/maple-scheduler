<template>
  <div class="modal fade" id="post-scheduler" tabindex="-1" role="dialog">
    <div class="modal-dialog modal-sm" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
          <h5 class="modal-title">新建任务</h5>
        </div>
        <div class="modal-body" style="padding-bottom:0px;">
          <form class="form-horizontal" id="post-form">
            <div class="form-group">
              <label class="col-sm-3 control-label">定时类型</label>
              <div class="col-sm-9">
                <select class="form-control" v-model="selected">
                  <option value="date">定时任务</option>
                  <option value="interval">间隔时间任务</option>
                </select>
              </div>
            </div>
            <div class="form-group">
              <label class="col-sm-3 control-label">任务列表</label>
              <div class="col-sm-9">
                <select class="form-control" v-model="form.func">
                  <option :value="job.name" v-for="job in jobs">{{ job.doc }}</option>
                </select>
              </div>
            </div>
            <div class="form-group" v-for="value,key in form">
              <label class="col-sm-3 control-label">{{ key }}</label>
              <div class="col-sm-9">
                <input class="form-control" :placeholder="key" v-model="form[key]">
              </div>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-sm btn-default pull-left" data-dismiss="modal" style="width:120px;">Close</button>
          <button type="button" class="btn btn-sm btn-primary" style="width:120px;" v-on:click="post">确定</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script type="text/javascript">
 import api from 'api'
 import {jobs} from 'service'

 var dateForm = {
     name:'',
     func:'',
     kwargs:'',
     run_date:''
 }
 var intervalForm = {
     name:'',
     func:'',
     kwargs:'',
     interval:'',
     start_date:'',
     end_date:''
 }
 /* var dateForm = {
  *     name:'任务名',
  *     kwargs:'参数',
  *     date:'运行时间'
  * }
  * var intervalForm = {
  *     name:'任务名',
  *     kwargs:'参数',
  *     interval:'间隔时间',
  *     start_date:'开始运行时间',
  *     end_date:'结束运行时间'
  * }*/
 export default {
     data() {
         return {
             selected:'date',
             form:dateForm,
             jobs:[]
         }
     },
     methods: {
         getJobList: function() {
             jobs().then((response) => {
                 this.jobs = response.data.data
             }).catch(function(response) {
                 console.log(response)
             })
         },
         post: function() {
             this.$parent.postItem(this.form)
         }
     },
     watch: {
         selected: function () {
             if(this.selected == 'interval'){
                 this.form = intervalForm
             }else {
                 this.form = dateForm
             }
         }
     }
 }
</script>

<style>
 .model {
     font-size: 12px;
 }
 
 .modal-sm {
     width: 360px;
 }
</style>
