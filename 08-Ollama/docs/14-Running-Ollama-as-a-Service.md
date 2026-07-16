# 14 - Running Ollama as a Service

## Introduction

Every example in this repository has assumed Ollama is "just running."
This chapter is what actually makes that true on a real machine that
reboots, and what changes when Ollama needs to run unattended, as an
actual service rather than a foreground terminal process.

## Learning Objectives

After this chapter I should be able to:

-   Explain how Ollama runs as a background service on each major OS.
-   Set up Ollama to start automatically on boot.
-   Run Ollama inside a container when that's the right fit.

------------------------------------------------------------------------

# How Ollama Runs in the Background, Per OS

``` text
macOS:    the Ollama app installs a background launchd service -
           starts automatically at login, no manual `ollama serve` needed

Windows:   similarly, a background service starts with the OS

Linux:      `ollama serve` runs the server directly - the install
             script typically also sets up a systemd service
```

## Setting Up systemd on Linux

``` bash
sudo systemctl status ollama    # check if it's already set up as a service
sudo systemctl enable ollama     # start automatically on boot
sudo systemctl start ollama       # start it now
sudo systemctl restart ollama      # restart after a config change
```

**Platform analogy:** this is exactly how you'd manage any other
long-running local service — the same `systemctl` commands used for
nginx, postgres, or any daemon. Ollama isn't special in this regard;
it's a normal background process that benefits from the same
lifecycle management.

## Configuring Ollama via Environment Variables

Service-level configuration (host binding, model storage location,
concurrency limits) is set through environment variables, typically in
the systemd unit file or a shell profile:

``` bash
OLLAMA_HOST=0.0.0.0:11434        # bind address (chapter 15's security topic)
OLLAMA_MODELS=/data/ollama-models   # custom model storage location
OLLAMA_NUM_PARALLEL=4                 # concurrent request handling (chapter 11)
OLLAMA_MAX_LOADED_MODELS=2              # cap on simultaneously loaded models
```

On Linux with systemd, these are typically set via:

``` bash
sudo systemctl edit ollama
# add: [Service]
#      Environment="OLLAMA_HOST=0.0.0.0:11434"
sudo systemctl restart ollama
```

## Running Ollama in a Container

``` bash
docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

This is a legitimate way to run Ollama for a shared team environment or
as part of a larger containerized stack (module 05's RAG pipeline could
reasonably run this way in production) — `-v ollama:/root/.ollama`
persists pulled models across container restarts, and `--gpus=all`
passes through GPU access if available (chapter 09's GPU discussion,
now in a container context).

## Verifying the Service Is Actually Configured Correctly

``` bash
curl -s http://localhost:11434/api/tags   # the same check from chapter 02,
                                            # now confirming the SERVICE
                                            # setup, not just a foreground process
```

The exact same verification from chapter 02 applies here — a service
that's "enabled" but not actually reachable is still broken, and this
one `curl` call catches that regardless of which OS or deployment
method was used to set it up.

## Hands-on: Confirm Your Own Setup Survives a Restart

``` bash
# Linux
sudo systemctl restart ollama
sleep 2
curl -s http://localhost:11434/api/tags

# macOS/Windows - quit and reopen the Ollama app, or restart the machine
curl -s http://localhost:11434/api/tags
```

If this `curl` call succeeds after a restart, the service is
genuinely configured to survive one — worth confirming directly rather
than assuming "it's installed" means "it starts automatically."

## Common Misconceptions

❌ Installing Ollama guarantees it survives a machine restart.
(On Linux specifically, this depends on whether `ollama serve` is
actually registered as a systemd service and enabled — verify with
`systemctl status ollama`, don't assume.)

❌ Environment-variable configuration only matters for advanced setups.
(`OLLAMA_HOST` in particular is directly relevant the moment you want
anything beyond localhost to reach Ollama — chapter 15 covers exactly
why that's a security decision, not just a convenience one.)

✔ The same `curl http://localhost:11434/api/tags` check from chapter
02 is the right way to verify a service setup actually worked — don't
trust "the install succeeded" as proof the service will actually be
there after a restart.

## Interview Questions

1.  How does Ollama typically run as a background service on Linux
    versus macOS?
2.  Name two environment variables used to configure Ollama's service
    behavior.
3.  Why would you run Ollama inside a container instead of installed
    directly on a host?
4.  What's the fastest way to confirm Ollama's service setup actually
    survives a restart?

## Summary

Ollama runs as a background service via `launchd` (macOS), a Windows
service, or `systemd` (Linux) — configured through environment
variables like `OLLAMA_HOST` and `OLLAMA_MODELS`, and verifiable with
the same `curl` check from chapter 02. Running it in a container
(`docker run ollama/ollama`) is a legitimate option for shared or
containerized environments, with the same GPU passthrough and model
persistence concerns as any other containerized service.

## Next Chapter

➡️ `15-Security-Exposing-Ollama-Beyond-Localhost.md`
