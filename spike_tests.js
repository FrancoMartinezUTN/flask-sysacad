import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '10s', target: 10 },   // subida suave
    { duration: '20s', target: 100 },  // carga sostenida
    { duration: '10s', target: 0 },    // bajada
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% de las requests < 500 ms
    http_req_failed: ['rate<0.01'],    // menos del 1% de errores
  },
};

const BASE_URL = __ENV.SYSACAD_BASE_URL || 'http://127.0.0.1:5000';

export default function () {
  const res = http.get(`${BASE_URL}/alumnos`);

  check(res, {
    'status 200': (r) => r.status === 200,
    'response is JSON': (r) =>
      String(r.headers['Content-Type'] || '').includes('application/json'),
  });

  sleep(1);
}
