# 15 - Security: Exposing Ollama Beyond Localhost

## Introduction

Chapter 05 noted that `api_key="ollama"` is required by the SDK but
completely unchecked by Ollama itself — fine on `localhost`, where the
only thing that can reach the server is your own machine. This chapter
is what changes, seriously, the moment that stops being true.

## Learning Objectives

After this chapter I should be able to:

-   Explain why Ollama has no authentication by default.
-   Explain the real risk of setting `OLLAMA_HOST=0.0.0.0`.
-   Apply a real access-control layer if network exposure is genuinely
    needed.

------------------------------------------------------------------------

# Why "No Auth" Is Fine on Localhost and Dangerous Beyond It

By default, Ollama binds to `127.0.0.1` — reachable only from the same
machine. Every example in this repository has relied on that boundary
implicitly: `api_key="ollama"` works because Ollama never checks it,
which is only an acceptable design when the network itself is the
actual access control.

``` text
OLLAMA_HOST=127.0.0.1:11434 (default)
  -> only processes on THIS machine can reach it
  -> "no API key checking" is fine, because the OS/network already
     restricts who can even make the request

OLLAMA_HOST=0.0.0.0:11434
  -> ANY device that can reach this machine's IP can call the API
  -> "no API key checking" now means ANYONE on the network can run
     inference, pull/delete models, and consume all your compute
```

## The Real Risk, Concretely

**Platform analogy:** this is the exact same mistake as binding a
database to `0.0.0.0` with no password, "just for local testing" —
module 05's whole RAG pipeline runs against Chroma with no auth
locally, which is correctly fine (module 04 chapter 03) specifically
*because* it's local-only. The moment Ollama (or Chroma, or any
locally-trusted service) becomes network-reachable, the entire trust
model that made "no auth" acceptable is gone, and nothing else has
changed to compensate.

Concrete consequences of an unauthenticated, network-exposed Ollama
instance:

``` text
- Anyone on the network can run (potentially expensive/slow) inference,
  consuming your GPU/CPU
- Anyone can pull new models, consuming disk space and bandwidth
- Anyone can DELETE your models (ollama rm is an API call too)
- If a model is later configured with tool-calling access to
  something real (module 02 chapter 14, module 06, module 07),
  this becomes a much more serious problem
```

## If You Genuinely Need Network Access

``` text
1. Put a reverse proxy (nginx, Caddy) in front of Ollama, with real
   authentication (an API key check, basic auth, or better)
2. Restrict access at the network level (firewall rules, a VPN, or a
   private subnet) rather than exposing it to the open internet
3. Never expose Ollama directly to the public internet with
   OLLAMA_HOST=0.0.0.0 and nothing else
```

``` nginx
# a minimal example: nginx enforcing an API key Ollama itself won't check
location / {
    if ($http_x_api_key != "a-real-secret-you-manage") {
        return 401;
    }
    proxy_pass http://127.0.0.1:11434;
}
```

This is module 06 chapter 13's authentication/authorization lesson,
applied to Ollama specifically — the enforcement has to live in front
of Ollama, since Ollama's own server doesn't provide it.

## Hands-on: Confirm Your Own Instance's Exposure

``` bash
echo $OLLAMA_HOST   # empty or 127.0.0.1 = localhost-only (safe default)
                      # 0.0.0.0 = network-reachable (needs real auth in front)

# from a DIFFERENT machine on the same network, if you have one:
curl http://<this-machine's-IP>:11434/api/tags
# if this succeeds, your instance is network-reachable right now
```

If you've never explicitly set `OLLAMA_HOST`, you're very likely
still on the safe, localhost-only default — worth confirming directly
rather than assuming, especially before following any tutorial that
suggests setting `OLLAMA_HOST=0.0.0.0` "to make it easier to connect
from another device."

## Common Misconceptions

❌ Ollama has some form of built-in authentication that just needs to
be enabled.
(It has none by default — `api_key="ollama"` in every example
throughout this repository was never actually checked. Real
authentication has to be added in front of it, e.g. a reverse proxy.)

❌ Setting `OLLAMA_HOST=0.0.0.0` is only a problem on a public cloud
server.
(It's a problem on any network where untrusted devices might be
present — including a home or office network with guests, IoT
devices, or anything else you don't fully control.)

✔ Treat `OLLAMA_HOST=0.0.0.0` as a deliberate decision requiring a
real access-control layer in front of it — never as a convenience
toggle to "just make it reachable."

## Interview Questions

1.  Why is Ollama's lack of default authentication acceptable on
    localhost but dangerous once network-exposed?
2.  Name three concrete risks of an unauthenticated, network-reachable
    Ollama instance.
3.  What's the correct way to add authentication in front of Ollama?
4.  How would you check whether your own Ollama instance is currently
    network-reachable?

## Summary

Ollama has no authentication by default — a completely reasonable
design for a localhost-only service, and a real security risk the
moment `OLLAMA_HOST` is set to make it network-reachable. If network
access is genuinely needed, real authentication (an API key check, a
reverse proxy, network-level restrictions) has to be added in front of
it — Ollama's own server won't provide that boundary for you.

## Next Chapter

➡️ `16-Performance-Tuning.md`
