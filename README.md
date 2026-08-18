# HTTP Smuggle (`http-smuggle`)

**Category:** networking · **Difficulty:** hard · **Points:** 400

A request-smuggling desync reaches an internal admin panel that shows the seed.

## Run it

```bash
docker build -t sparflag/http-smuggle .
# `deca-ai start http-smuggle` (or the web UI) prints the docker run line with your
# SPARFLAG_SERVER + SPARFLAG_INSTANCE_TOKEN
```

## Recover the flag

The delivery blob is Fernet ciphertext. Discover the key seed, derive the Fernet key, then decrypt.

The plaintext flag is never written to disk or served — only the encoded delivery blob
is. When you have it:

```bash
deca-ai submit http-smuggle 'sparflag{...}'
```

## Hints

- Craft CL.TE or TE.CL to reach the back-end admin route.
- The smuggled response includes the Fernet seed.
