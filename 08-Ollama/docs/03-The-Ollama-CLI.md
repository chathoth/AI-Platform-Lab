# 03 - The Ollama CLI

## Introduction

The full set of CLI commands worth knowing, beyond `pull` and `run` —
verified directly against a real local instance rather than assumed
from the help text.

## Learning Objectives

After this chapter I should be able to:

-   Use `list`, `show`, `ps`, and `rm` confidently.
-   Read `ollama show`'s output to understand a model's real
    specifications.
-   Read `ollama ps` to see what's actually loaded in memory right
    now.

------------------------------------------------------------------------

# The Core Commands

``` bash
ollama pull <model>      # download a model
ollama run <model>       # interactive chat, or a one-off prompt
ollama list               # list every model pulled locally
ollama show <model>        # inspect a model's specs
ollama ps                   # list models currently LOADED IN MEMORY
ollama rm <model>            # delete a pulled model, freeing disk space
ollama stop <model>           # unload a model from memory without deleting it
```

## `ollama list`: What's on Disk

Verified output on this module's test machine:

``` text
NAME                       ID              SIZE      MODIFIED     
nomic-embed-text:latest    0a109f422b47    274 MB    42 hours ago    
llama3.2:3b                a80c4f17acd5    2.0 GB    42 hours ago    
phi3:3.8b                  4f2222927938    2.2 GB    7 months ago    
llama3.1:8b                46e0c10c039e    4.9 GB    7 months ago    
```

This is disk inventory — every model here is downloaded, but not
necessarily loaded into memory right now (that's `ollama ps`, next).

## `ollama ps`: What's Actually Loaded

``` text
NAME           ID              SIZE      PROCESSOR    CONTEXT    UNTIL              
llama3.1:8b    46e0c10c039e    5.3 GB    100% GPU     4096       2 minutes from now
```

This is the memory-resident view — a model only shows up here after
being called at least once, and it stays loaded until the `UNTIL`
time passes (controlled by `keep_alive`, chapter 16) or it's evicted to
make room for another model. `PROCESSOR` shows whether it's running on
GPU, CPU, or split (chapter 09 covers this decision in depth).

## `ollama show`: A Model's Real Specifications

Verified output for `llama3.1:8b`:

``` text
  Model
    architecture        llama     
    parameters          8.0B      
    context length      131072    
    embedding length    4096      
    quantization        Q4_K_M    

  Capabilities
    completion    
    tools         

  Parameters
    stop    "<|start_header_id|>"    
    stop    "<|end_header_id|>"      
    stop    "<|eot_id|>"             
```

This is the ground truth for exactly what a model supports —
`Capabilities: tools` is how you'd confirm a model actually supports
function calling (module 02 chapter 14) before trying to use it that
way, and `context length` is the real number behind module 01 chapter
09's context-window discussion, specific to this exact model.

``` bash
ollama show llama3.1:8b --modelfile   # see the Modelfile that produced it (chapter 06)
```

## `ollama rm` and `ollama stop`: Two Different Kinds of Cleanup

``` text
ollama stop <model>   - unloads from MEMORY only, frees RAM/VRAM,
                          model stays on disk, next call re-loads it
ollama rm <model>      - deletes from DISK entirely, frees storage,
                          next use requires re-pulling
```

**Platform analogy:** this is scaling a deployment to zero (`stop`,
frees memory, keeps the image around) versus actually deleting the
image (`rm`, frees disk, needs a fresh pull to use again) — the same
distinction module 04 chapter 11 drew between soft and hard delete,
applied to model lifecycle instead of database records.

## Hands-on: Run the Full Set Yourself

``` bash
ollama list
ollama show llama3.1:8b
ollama run llama3.1:8b "hi"   # loads it into memory
ollama ps                       # confirm it now shows up here
ollama stop llama3.1:8b          # unload it
ollama ps                         # confirm it's gone from this list
ollama list                        # confirm it's STILL here - disk, not memory
```

## Common Misconceptions

❌ `ollama list` and `ollama ps` show the same thing.
(`list` is disk inventory — everything ever pulled. `ps` is memory —
only what's currently loaded and ready to respond instantly.)

❌ `ollama rm` just frees up memory.
(It deletes from disk — for a memory-only cleanup, use `ollama stop`
instead, which is reversible with no re-download needed.)

✔ `ollama show <model>` is the ground truth for a model's real
capabilities and specs — check it before assuming a model supports
tool calling or has a particular context length.

## Interview Questions

1.  What's the difference between `ollama list` and `ollama ps`?
2.  What's the difference between `ollama stop` and `ollama rm`?
3.  How would you confirm a model actually supports tool calling
    before trying to use it that way?
4.  What does the `UNTIL` column in `ollama ps` represent?

## Summary

`ollama list` shows what's on disk, `ollama ps` shows what's currently
loaded in memory, `ollama show` gives a model's real specifications
(architecture, context length, capabilities), and `stop`/`rm` are two
genuinely different cleanup operations — memory versus disk. Together
these commands are the actual operational toolkit behind every
`ollama run` and API call this repository has used.

## Next Chapter

➡️ `04-The-Native-REST-API.md`
