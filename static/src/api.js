const API = {
  api_prefix: 'http://127.0.0.1:5000',
  api:{
    scheduler: '/scheduler',
    status: '/scheduler/status',
    pause: '/scheduler/{0}/pause',
    resume: '/scheduler/{0}/resume',
    execute: '/scheduler/{0}/execute',
    jobs: '/jobs'
  },
  create: function() {
    Object.keys(this.api).forEach(key => {
      this.api[key] = this.api_prefix + this.api[key];
    });
    return this.api;
  }
};
export default API.create();
