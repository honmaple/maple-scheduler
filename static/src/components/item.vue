<template>
    <div class="modal fade" id="get-scheduler" tabindex="-1" role="dialog">
        <div class="modal-dialog modal-sm" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                    <h5 class="modal-title">查看任务</h5>
                </div>
                <div class="modal-body" style="padding-bottom:0px;">
                    <table class="table table-hover table-striped table-bordered">
                        <thead>
                            <tr>
                                <th>key</th>
                                <th>value</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="value,key in scheduler">
                                <td>{{ key }}</td>
                                <td class="auto-wrap">{{ value }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-sm btn-default pull-left" data-dismiss="modal" style="width:120px;">Close</button>
                    <button type="button" class="btn btn-sm btn-primary" style="width:120px;">确定</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script type="text/javascript">
 export default {
     props: ['scheduler'],
     data() {
         return {
             scheduler: this.scheduler,
         }
     },
     /* created() {
      *     this.getScheduler()
      * },
      * methods: {
      *     getScheduler: function() {
      *         this.$http.get('http://127.0.0.1:5000/scheduler/')
      *             .then((response) => {
      *                 this.items = response.body.data
      *                 this.pageinfo = response.body.pageinfo
      *             })
      *             .catch(function(response) {
      *                 console.log(response)
      *             })
      *     },
      * }*/
 }
</script>

<style>
 .auto-wrap {
     word-wrap:break-word;
     word-break:break-all;
 }
</style>
