import http from "k6/http";
import { Trend } from "k6/metrics";
import { check } from "k6";

const statusTrend = new Trend("status_codes");

export const options = {
    // Escenario de carga básico para desarrollo local
    stages: [
        { duration: "10s", target: 100 },  // sube hasta 100 usuarios virtuales
        { duration: "20s", target: 100 },  // mantiene 100
        { duration: "10s", target: 0 },    // baja a 0
    ],
    // Para http://localhost NO hace falta TLS:
    // insecureSkipTLSVerify: true,
};

// Endpoint del microservicio_alumno

const BASE_URL = "http://localhost:5000/alumnos";

export default function () {
    // Para Sysacad usamos GET sobre el listado de alumnos
    const res = http.get(BASE_URL);

    // Registramos el código de estado en la métrica
    statusTrend.add(res.status);

    // Mismos códigos que usa la cátedra en sus ejemplos
    check(res, {
        "status is 200": (r) => r.status === 200,
        "status is 409": (r) => r.status === 409,
        "status is 404": (r) => r.status === 404,
        "status is 400": (r) => r.status === 400,
        "status is 429": (r) => r.status === 429,
        "status is 500": (r) => r.status === 500,
    });
}
