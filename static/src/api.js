const API = {
    api_prefix: 'http://127.0.0.1:5000',
    create: function() {
        return {
            scheduler: this.api_prefix + '/scheduler/',
            scheduler_status: this.api_prefix + '/scheduler/status/',
        }
    }
};
export default API.create()
