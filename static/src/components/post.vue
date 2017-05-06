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
     run_date:'',
     trigger:'date'
 }
 var intervalForm = {
     name:'',
     func:'',
     kwargs:'',
     seconds:'',
     start_date:'',
     end_date:'',
     trigger:'interval'
 }
 export default {
     data() {
         return {
             form:dateForm,
             jobs:[],
             selected:'date'
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
             console.log(this.form)
             if (this.form.trigger == 'interval') {
                 this.form.seconds = parseInt(this.form.seconds)
                 if (!this.form.start_date) {
                     delete this.form.start_date
                 }
                 if (!this.form.end_date) {
                     delete this.form.end_date
                 }
             }
             this.$parent.postItem(this.form)
         }
     },
     watch: {
         selected: function() {
             if(this.selected == 'date') {
                 this.form = dateForm
                 this.form.trigger = 'date'
             } else {
                 this.form = intervalForm
                 this.form.trigger = 'interval'
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
