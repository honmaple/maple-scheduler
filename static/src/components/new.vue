<template>
    <div class="modal fade" id="post-scheduler" tabindex="-1" role="dialog">
        <div class="modal-dialog modal-sm" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                    <h5 class="modal-title">新建任务</h5>
                </div>
                <div class="modal-body" style="padding-bottom:0px;">
                    <form class="form-horizontal">
                        <div class="form-group">
                            <label for="name" class="col-sm-3 control-label">定时类型</label>
                            <div class="col-sm-9">
                                <select class="form-control" v-model="selected">
                                    <option value="date">定时任务</option>
                                    <option value="interval">间隔时间任务</option>
                                </select>
                            </div>
                        </div>
                        <template v-if="selected == 'date'">
                            <div class="form-group">
                                <label for="name" class="col-sm-3 control-label">任务名</label>
                                <div class="col-sm-9">
                                    <input class="form-control" id="name" placeholder="任务名称">
                                </div>
                            </div>
                            <div class="form-group">
                                <label for="name" class="col-sm-3 control-label">参数</label>
                                <div class="col-sm-9">
                                    <input class="form-control" id="name" placeholder="任务名称">
                                </div>
                            </div>
                            <div class="form-group">
                                <label for="name" class="col-sm-3 control-label">运行时间</label>
                                <div class="col-sm-9">
                                    <input class="form-control" id="name" placeholder="运行时间">
                                </div>
                            </div>
                        </template>
                        <template v-else>
                            <div class="form-group">
                                <label for="name" class="col-sm-3 control-label">任务名</label>
                                <div class="col-sm-9">
                                    <input class="form-control" id="name" placeholder="任务名称">
                                </div>
                            </div>
                            <div class="form-group">
                                <label for="name" class="col-sm-3 control-label">参数</label>
                                <div class="col-sm-9">
                                    <input class="form-control" id="name" placeholder="任务名称">
                                </div>
                            </div>
                            <div class="form-group">
                                <label for="name" class="col-sm-3 control-label">间隔时间</label>
                                <div class="col-sm-9">
                                    <input class="form-control" id="name" placeholder="运行时间">
                                </div>
                            </div>
                            <div class="form-group">
                                <label for="name" class="col-sm-3 control-label">开始运行时间</label>
                                <div class="col-sm-9">
                                    <input class="form-control" id="name" placeholder="运行时间">
                                </div>
                            </div>
                            <div class="form-group">
                                <label for="name" class="col-sm-3 control-label">结束运行时间</label>
                                <div class="col-sm-9">
                                    <input class="form-control" id="name" placeholder="运行时间">
                                </div>
                            </div>
                        </template>
                    </form>
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
     data() {
         return {
             selected:'date',
         }
     },
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
