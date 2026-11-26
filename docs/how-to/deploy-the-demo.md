---
type: how-to
status: active
tags: [how-to, demo, deployment]
---

# Deploy the demo as a container

Build and test the CPU demo locally, then run the same image on a virtual machine.
Run the local commands from the repository root in Bash. You need Docker, Python 3, Git,
curl, jq, and the [demo library](../../.assets/demo/README.md#the-demos-library).
Keep the same local shell open through the build, checks, and archive export.

## 1. Assemble and build

Choose an empty output directory outside the checkout. A second assembly with the same
inputs leaves the folder as it is. For a VM deployment, run `uname -m` on the VM first.
Use `linux/amd64` for `x86_64`, including when building on an ARM64 Mac. Use
`linux/arm64` for `aarch64` or for a native build on an ARM64 Mac.

```bash
work=$(mktemp -d "${TMPDIR:-/tmp}/layerwise-demo.XXXXXX")
image=layerwise-demo:local
python3 scripts/assemble_demo.py --out "$work/demo"
BUILDX_CONFIG="$work/buildx" docker build --platform linux/amd64 -t "$image" "$work/demo"
```

## 2. Start and measure

Start with two CPUs and a 7 GiB container limit. The local measurements used Docker
Desktop with about 7.7 GiB total.

```bash
url=http://127.0.0.1:17860
container=layerwise-demo-local
start_demo() {
  docker run -d --rm --name "$container" --cpus=2 --memory=7g \
    -p 127.0.0.1:17860:7860 "$image" || return
  for attempt in {1..120}; do
    if curl -fsS --max-time 2 "$url/" > "$work/page.html" 2>/dev/null &&
       curl -fsS --max-time 2 "$url/api/libraries" > "$work/libraries.json" 2>/dev/null; then
      return 0
    fi
    sleep 0.1
  done
  docker logs "$container"
  return 1
}
time start_demo
docker image inspect "$image" --format '{{.Size}} bytes ({{.Architecture}})'
jq -e 'length == 4 and all(.[]; .n_foregrounds == 7 and .n_backgrounds == 1)' "$work/libraries.json"
library=$(jq -r '.[] | select(.name == "da2-large") | .id' "$work/libraries.json")

for size in 512 1024; do
  curl -fsS --max-time 600 -o "$work/sequence-$size.json" \
    -w "$size px: %{time_total}s (%{http_code})\n" -H 'Content-Type: application/json' \
    -d "{\"library\":\"$library\",\"size\":$size,\"frames\":80,\"n_objects_min\":4,\"n_objects_max\":4}" \
    "$url/api/sequences"
  jq -e --argjson size "$size" \
    '.cached == false and .size == $size and .frames == 80 and (.streams | has("bokeh"))' \
    "$work/sequence-$size.json"
  docker exec "$container" cat /sys/fs/cgroup/memory.peak
done
```

In the earlier two-core test on an ARM64 Mac, the page and API were ready in 1.24 s.
The image was 1.83 GB on ARM64 and 2.01 GB on AMD64. With four objects and 80 frames,
generation took 39.3 s at 512 px and 119.4 s at 1024 px. Peak memory reached 5.7 GB,
including filesystem cache. Start a fresh container to measure an uncached run again.

## 3. Check playback and concurrent requests

Open `http://127.0.0.1:17860/`, click **Generate sequence**, and watch the progress bar.
While generation is active, send a second request. It should return HTTP 429.

```bash
curl -sS -w '\nHTTP %{http_code}\n' -H 'Content-Type: application/json' \
  -d "{\"library\":\"$library\",\"seed\":301,\"size\":512,\"frames\":80}" "$url/api/sequences"
```

When the first generation finishes, play the Bokeh pane and add Occlusion from the
stream picker. The demo keeps the six most recent sequence directories. Stop the
container when you finish.

```bash
docker stop "$container"
```

## Run it on a virtual machine

Use a VM with Docker and SSH access for an account with Docker rights. Put an HTTPS
reverse proxy in front of the container if visitors will use a public domain.

| Resource | Suggested size |
|---|---|
| CPU | 2 to 4 cores |
| RAM | 8 GB, or 16 GB if available |
| Disk | 20 GB |

1. Build for the VM's CPU architecture as shown in [Assemble and build](#1-assemble-and-build).
   To ship an archive, save it on the build host and copy it into your home directory
   on the VM over SSH. Load the archive in an SSH session. If you ship through a
   registry, pull the image on the VM instead.

   ```bash
   set -o pipefail
   docker save "$image" | gzip > "$work/layerwise-demo.tar.gz"
   ```

   ```bash
   docker load -i "$HOME/layerwise-demo.tar.gz"
   ```

2. Start or update the demo on port 7860 on the VM's loopback interface. For an
   update, repeat step 1 with the new image, then run this block in any SSH session.
   It replaces the previous container and clears its sequence cache. Docker restarts
   the container after a reboot unless it was explicitly stopped. Set `image` in the
   current session if the loaded or pulled tag differs from `layerwise-demo:local`.
   For a local rehearsal, set `host_port` to 17860 before running the block.

   ```bash
   if docker container inspect layerwise-demo >/dev/null 2>&1; then
     docker stop layerwise-demo && docker rm layerwise-demo || exit 1
   fi
   docker run -d --restart unless-stopped --name layerwise-demo \
     -p "127.0.0.1:${host_port:-7860}:7860" "${image:-layerwise-demo:local}"
   ```

3. Check the page and library list. The first request should succeed, and the second
   should list all four libraries.

   ```bash
   url="http://127.0.0.1:${host_port:-7860}"
   curl -fsS -o /dev/null -w 'Page HTTP %{http_code}\n' "$url/"
   curl -fsS "$url/api/libraries" | jq -e 'select(length == 4) | map(.name)'
   ```
