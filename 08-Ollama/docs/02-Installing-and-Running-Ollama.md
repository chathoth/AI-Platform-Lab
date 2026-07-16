# 02 - Installing and Running Ollama

## Introduction

Every hands-on section in this repository has assumed Ollama is
already installed and running. This short chapter is the part that
came before all of that — install, confirm it's running, pull your
first model.

## Learning Objectives

After this chapter I should be able to:

-   Install Ollama on macOS, Linux, or Windows.
-   Confirm the server is running and reachable.
-   Pull and run a model from the command line.

------------------------------------------------------------------------

# Installing Ollama

``` bash
# macOS - download from ollama.com, or via Homebrew
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows - download the installer from ollama.com
```

On macOS and Windows, installing the app also sets up a background
service that starts automatically. On Linux, `ollama serve` runs the
server explicitly (often set up as a systemd service — chapter 14
covers this properly).

## Confirming It's Running

``` bash
ollama --version
```

``` bash
curl -s http://localhost:11434/api/tags
```

Verified output on this module's own test machine:

``` text
ollama version is 0.31.1
```

If `curl` fails to connect, the server isn't running — start it with
`ollama serve` (Linux) or open the Ollama app (macOS/Windows).

## Pulling and Running Your First Model

``` bash
ollama pull llama3.1:8b
```

This downloads the model's weights (a few GB, depending on size and
quantization — module 01 chapter 13) to local disk. Once pulled:

``` bash
ollama run llama3.1:8b "What is a Kubernetes readiness probe?"
```

`ollama run` is the interactive/quick-test path — chapter 04 covers
calling the same model programmatically via the REST API, which is
what every example script in this repository actually does.

## Where Models Actually Live on Disk

``` text
macOS:   ~/.ollama/models
Linux:    /usr/share/ollama/.ollama/models (or ~/.ollama/models)
Windows:   C:\Users\<name>\.ollama\models
```

Worth knowing before chapter 07's quantization/format discussion and
chapter 10's memory-planning chapter — this is where the actual GGUF
files (module 01 chapter 13) live, and where disk space gets consumed
as you pull more models.

## Hands-on: Confirm Your Own Setup End to End

``` bash
ollama --version
ollama pull llama3.2:3b   # a smaller model, faster to pull for a quick test
ollama run llama3.2:3b "Say OK if you're working."
ollama list
```

Confirm `ollama list` shows the model you just pulled — this is the
same verification loop every later chapter in this module builds on.

## Common Misconceptions

❌ `ollama run` is the only way to use a pulled model.
(It's the interactive CLI path — chapter 04's REST API and chapter
05's OpenAI-compatible endpoint are how every programmatic example in
this repository actually calls a model.)

❌ Installing Ollama also downloads every model.
(Installing sets up the runtime only — each model is pulled
separately and explicitly, and only takes up disk space once pulled.)

✔ `curl http://localhost:11434/api/tags` is the fastest way to confirm
Ollama is actually running and reachable — worth checking first before
debugging anything further upstream in your own code.

## Interview Questions

1.  What's the difference between installing Ollama and pulling a
    model?
2.  How would you confirm Ollama is running and reachable from the
    command line?
3.  Where do pulled models actually live on disk?
4.  What's the difference between `ollama run` and calling the REST
    API directly?

## Summary

Installing Ollama sets up the runtime and (on macOS/Windows) a
background service; pulling a model downloads its weights separately.
`curl http://localhost:11434/api/tags` is the fastest way to confirm
everything is working before moving on to the CLI (chapter 03) and the
REST API (chapter 04) that every other chapter in this module builds
on.

## Next Chapter

➡️ `03-The-Ollama-CLI.md`
