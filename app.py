import time, random, uvicorn, psutil
from fastapi import FastAPI
from fastapi.responses import Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI(title="ML Full Stack Monitoring")

# --- 1. БИЗНЕС-МЕТРИКИ ---
BIZ_REVENUE = Counter('biz_revenue_total', 'Выручка (LTV)')
BIZ_CTR = Gauge('biz_ctr_ratio', 'CTR рекламных вставок')

# --- 2. МЕТРИКИ ПРИЛОЖЕНИЯ ---
APP_REQUESTS = Counter('http_requests_total', 'Throughput (RPS)')
APP_LATENCY = Histogram('app_request_latency_seconds', 'Latency p95', buckets=(0.05, 0.1, 0.2, 0.5))
APP_ERRORS = Counter('http_errors_total', 'Error Rate')

# --- 3. ML-МЕТРИКИ ---
ML_PSI = Gauge('ml_psi_index', 'Data Drift (PSI)')
ML_PRECISION = Gauge('ml_precision_score', 'Precision (Точность)')
ML_IOU = Gauge('ml_iou_score', 'IoU (Качество наложения)')

# --- 4. МЕТРИКИ ИНФРАСТРУКТУРЫ ---
INFRA_CPU = Gauge('infra_cpu_usage', 'Загрузка CPU %')
INFRA_RAM = Gauge('infra_ram_usage_bytes', 'Использование RAM')

@app.get("/metrics")
def metrics():
    # Обновляем метрики инфраструктуры перед отдачей в Prometheus
    INFRA_CPU.set(psutil.cpu_percent())
    INFRA_RAM.set(psutil.virtual_memory().used)
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/predict")
async def predict(drift: bool = False, error: bool = False):
    APP_REQUESTS.inc()
    start_time = time.time()
    
    if error:
        APP_ERRORS.inc()
        return Response(status_code=500)

    # Симуляция ML-метрик
    ML_PSI.set(random.uniform(0.3, 0.5) if drift else random.uniform(0.01, 0.09))
    ML_PRECISION.set(random.uniform(0.85, 0.95))
    ML_IOU.set(random.uniform(0.7, 0.85))

    # Симуляция бизнеса
    BIZ_REVENUE.inc(random.randint(1, 10))
    BIZ_CTR.set(random.uniform(0.02, 0.06))

    time.sleep(random.uniform(0.05, 0.18))
    APP_LATENCY.observe(time.time() - start_time)
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)