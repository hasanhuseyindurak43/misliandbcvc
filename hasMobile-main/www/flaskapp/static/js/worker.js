// worker.js

self.addEventListener('message', function(e) {
    const workerId = e.data.id;
    console.log('Worker ' + workerId + ' started on thread');

    performCpuIntensiveTask(workerId);
    self.postMessage('Worker ' + workerId + ' completed task');
});

function performCpuIntensiveTask(workerId) {
    console.log('Worker ' + workerId + ' is performing CPU intensive task');
    let sum = 0;
    for (let i = 0; i < 1e7; i++) {
        sum += i;
    }
    console.log('Worker ' + workerId + ' completed the task with sum: ' + sum);
}
