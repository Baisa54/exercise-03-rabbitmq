# Exercise 03 — RabbitMQ Event-Driven Architecture

> **Distributed Systems & Parallel Programming — UNLu 2026**
>
> This exercise is part of the continuous assessment for the course. Throughout the semester you will solve hands-on exercises that are graded automatically. Each exercise builds on the previous one and reinforces concepts you will need for the major assignments: REST APIs, Docker, Compose, Kubernetes, messaging, etc.
>
> The goal is not just to "pass the tests" but to understand what you are building. Tests validate the output — comprehension is on you.

## Course topics covered

| Unit | Topic | How it applies here |
|------|-------|-------------------|
| **U3.1** | Cloud Computing: messaging patterns | You implement pub/sub with RabbitMQ |
| **U4.3** | Docker Compose: multi-container | 4-service stack: API, DB, RabbitMQ, Consumer |

### What you will practice

- Publishing events to **RabbitMQ** when state changes occur
- Implementing a **consumer** that processes events asynchronously
- Understanding **event-driven architecture** in distributed systems
- Orchestrating **4 services** with Docker Compose

---

## Automated grading

Hidden tests cover:
- docker-compose.yml has 4 services (api, db, rabbitmq, consumer)
- RabbitMQ management UI responds on port 15672
- POST /api/nodes publishes "node_registered" event
- DELETE /api/nodes/{name} publishes "node_deleted" event
- Consumer receives and logs events
- All 6 API endpoints still work

You have a maximum of **5 submissions**.

**Deadline: Sunday, September 27, 2026 at 23:59 (UTC-3)** (2 late days allowed with penalty)

---

## Context

In real distributed systems, services communicate asynchronously via message brokers. When a node registers or leaves the registry, other services need to know — but they should not be tightly coupled. RabbitMQ provides this decoupling.

## Objective

Extend the Node Registry to **publish events** to RabbitMQ and implement a **consumer** service.

## How to submit

1. Fork, implement, push

## Message format

```json
{"event": "node_registered", "node_name": "node-alpha", "timestamp": "2026-05-01T12:00:00Z"}
{"event": "node_deleted", "node_name": "node-alpha", "timestamp": "2026-05-01T12:05:00Z"}
```

Queue name: `node_events`

## Running locally

```bash
docker compose up --build -d
# API: http://localhost:8080
# RabbitMQ Management: http://localhost:15672 (guest/guest)
# Check consumer logs: docker compose logs consumer -f
docker compose down -v
```
