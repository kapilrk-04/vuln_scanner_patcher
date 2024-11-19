class RateLimiter {
    constructor(minTimeBetweenRequests) {
      this.minTimeBetweenRequests = minTimeBetweenRequests;
      this.lastRequestTime = 0;
      this.queue = [];
      this.isProcessing = false;
    }

    async makeRequest(requestFn) {
      return new Promise((resolve, reject) => {
        this.queue.push({ requestFn, resolve, reject });
        this.processQueue();
      });
    }

    async processQueue() {
      if (this.isProcessing || this.queue.length === 0) return;

      this.isProcessing = true;

      while (this.queue.length > 0) {
        const { requestFn, resolve, reject } = this.queue[0];

        const now = Date.now();
        const timeToWait = Math.max(0, this.lastRequestTime + this.minTimeBetweenRequests - now);

        if (timeToWait > 0) {
          await new Promise(resolve => setTimeout(resolve, timeToWait));
        }

        try {
          const result = await requestFn();
          resolve(result);
        } catch (error) {
          reject(error);
        }

        this.lastRequestTime = Date.now();
        this.queue.shift();
      }

      this.isProcessing = false;
    }
}

module.exports = RateLimiter;
