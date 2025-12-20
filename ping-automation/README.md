1. Currently (ping runs once, results are static) it's a snapshot service: TO-DO: Extend this to periodic checks using schedulars or worker threads. [Add continuous ping loop

Add timeouts & retries

Add health endpoint

Add Gunicorn config
]

 OUTCOME: First design (API-based):

/ping endpoint → runs ping

Results stored in memory (results dict)

/status endpoint → returns JSON over HTTP

No file is written to disk

So:

JSON exists in API response

Not persisted to filesystem


APIs respond with JSON

Persistence is optional (DB / file / object storage)
![alt text](<Screenshot 2025-12-20 164439.png>)
![alt text](<Screenshot 2025-12-20 164521.png>)

: Current (file-based) 