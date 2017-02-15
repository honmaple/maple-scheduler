<template>
    <div class="scheduler-list">
        <div class="container-fluid">
            <ol class="breadcrumb text-left">
                <li><a href="#">定时任务管理</a></li>
                <li class="active">任务列表</li>
            </ol>
            <div class="pull-right">
            <form class="form-inline">
                <div class="form-group">
                    <input type="text" class="form-control input-sm" id="start" placeholder="定时任务ID" style="border-radius:3px 0 0 3px">
                    <button type="button" class="btn btn-sm btn-primary pull-right" style="width:100px;border-radius:0 3px 3px 0;">搜索</button>
                </div>
            </form>
            </div>
            <div class="text-left" style="margin-bottom:7px;">
                <button type="button" class="btn btn-sm btn-primary opeara">启动</button>
                <button type="button" class="btn btn-sm btn-warning opeara">关闭</button>
                <button type="button" class="btn btn-sm btn-success opeara">新建任务</button>
            </div>
            <div class="text-left">
                <button type="button" class="btn btn-sm btn-primary opeara">全选</button>
                <button type="button" class="btn btn-sm btn-warning opeara">取消全选</button>
                <button type="button" class="btn btn-sm btn-danger opeara">删除选中</button>
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
                        <td></td>
                        <td>{{ item.title }}</td>
                        <td>{{ item.content }}</td>
                        <td>{{ item.created_at }}</td>
                        <td style="width:240px;">
                            <div class="btn-group btn-group-justified" role="group" style="margin-bottom:7px;">
                                <a class="btn btn-sm btn-warning opeara-item">查看</a>
                                <a class="btn btn-sm btn-success opeara-item">修改</a>
                                <a class="btn btn-sm btn-danger opeara-item">删除</a>
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
            <PageInfo :pageinfo="pageinfo"></PageInfo>
        </div>
    </div>
</template>

<script>
    import PageInfo from './common/pageinfo'

    export default {
        components: {
            PageInfo,
        },
        data() {
            return {
                table: {
                    'th': ['选择', 'ID', '运行时间', '定时类型', '运行状态', '操作']
                },
                items: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                pageinfo: {}
            }
        },
        created() {
            this.getScheduler()
        },
        methods: {
            getScheduler: function() {
                this.$http.get('http://127.0.0.1:8000/message/', {
                        params: {
                            cloud_token: 'MQ.C3hMJA.5NFkzsF2fErXKYHXWFefi9SYVFc'
                        }
                    })
                    .then((response) => {
                        this.items = response.body.data
                        this.pageinfo = response.body.pageinfo
                    })
                    .catch(function(response) {
                        console.log(response)
                    })
            }
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
