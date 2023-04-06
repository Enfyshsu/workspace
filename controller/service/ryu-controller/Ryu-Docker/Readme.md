# Ryu DockerFile

Just a dockerfile to run ryu controllers in a container.

Uses python 3.8 and alpine, as opposed to the ubuntu 16.04 base used in the official repo.

This leads to an image that is about half the size of the official image.

## Build

```bash
docker build --rm -f Dockerfile -t ryu-alpine:latest .
```
