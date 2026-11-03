# Generates the 3,000-line test log used in the video (deterministic, seed 11). One ERROR at line 2418.
import random
random.seed(11)
svc = ["api", "auth", "billing", "search", "worker"]
L, t = [], 0
for i in range(3000):
    t += random.randint(80, 400)
    s = t // 1000; ts = f"2026-11-03T14:{(s//60)%60:02d}:{s%60:02d}.{t%1000:03d}Z"
    if i == 2417:
        L.append(f"{ts} ERROR billing db: connection pool exhausted (max=10, waiting=37) — request timed out after 30000 ms")
    elif i in (2418, 2419, 2420):
        L.append(f"{ts} WARN api upstream billing returned 503 (retry {i-2417}/3)")
    elif i % 97 == 0:
        L.append(f"{ts} WARN {random.choice(svc)} slow response {random.randint(900,1900)} ms")
    else:
        sv = random.choice(svc)
        L.append(f"{ts} INFO {sv} {random.choice(['GET','POST'])} /{sv}/{random.choice(['list','get','update','health','sync'])} 200 {random.randint(3,180)} ms user={random.randint(1000,9999)}")
open("server.log", "w").write("\n".join(L) + "\n")
print(len(L), "lines written to server.log")
