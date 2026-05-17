# HW8: Мониторинг ML-системы Virtual Product Placement

##  1. Дерево метрик и ADR
*   **4 уровня:** Бизнес (LTV, CTR), Приложение (RPS, Latency), ML (PSI, IoU), Инфраструктура (CPU, GPU).
*   **ADR:** Переход на **Kappa-архитектуру** (Kafka + ClickHouse) для достижения цели в **10 000 RPS**.

##  2. Стек мониторинга
*   **Сервис:** FastAPI с экспортером `prometheus_client` (порт 8001).
*   **Сбор данных:** Prometheus (Targets: UP).
*   **Визуализация:** Grafana Dashboard (PSI, Latency p95, Throughput).

##  3. Обнаружение дрифта (Инцидент)
*   **Симуляция:** Подача `?drift=true` подняла PSI до **0.35**.
*   **Результат:** Сработка алерта в Grafana (статус **Firing**). Порог 0.2 успешно пройден.

##  4. Data Quality Ops
*   **Инструмент:** Попытка внедрения DQOps.
*   **Статус:** Ограничение из-за лицензионной политики (API Key). Контроль качества данных перенесен на уровень PSI в Grafana.

##  5. Архитектура (Kappa)
*   **Поток:** Video Source -> Kafka -> ML Service -> ClickHouse.
*   **Автоматизация:** При PSI > 0.2 триггерится пайплайн переобучения в SageMaker.

---
**Стек:** Python, Docker, Prometheus, Grafana, Diagrams.

